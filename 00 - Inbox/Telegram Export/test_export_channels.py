import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from telethon import functions, types

import export_channels as exporter


AT = datetime(2026, 10, 23, tzinfo=timezone.utc)


def channel(channel_id=101, **kwargs):
    return types.Channel(channel_id, "Тестовый канал", types.ChatPhotoEmpty(), AT,
                         broadcast=True, username="example", access_hash=987654321, **kwargs)


def folder(**kwargs):
    fields = dict(id=7, title=types.TextWithEntities("🌐", []),
                  pinned_peers=[], include_peers=[], exclude_peers=[])
    fields.update(kwargs)
    return types.DialogFilter(**fields)


def dialog(entity=None, **kwargs):
    fields = dict(folder_id=None, unread_mark=False, unread_mentions_count=0,
                  notify_settings=types.PeerNotifySettings())
    fields.update(kwargs)
    return SimpleNamespace(entity=entity or channel(), unread_count=0,
                           dialog=SimpleNamespace(**fields))


def message(message_id, **kwargs):
    return types.Message(id=message_id, peer_id=types.PeerChannel(101),
                         date=AT, message=kwargs.pop("message", f"Пост {message_id}"), **kwargs)


class FakeClient:
    def __init__(self, messages, selected_folder=None):
        self.messages = messages
        self.selected_folder = selected_folder
        self.calls = []
        self.disconnected = False

    async def connect(self):
        self.calls.append("connect")

    async def disconnect(self):
        self.disconnected = True

    async def is_user_authorized(self):
        return True

    async def __call__(self, request):
        self.calls.append(type(request).__name__)
        if isinstance(request, functions.messages.GetDialogFiltersRequest):
            return SimpleNamespace(filters=[self.selected_folder])
        raise AssertionError(f"Unexpected API request: {type(request).__name__}")

    async def get_entity(self, peer):
        self.calls.append("get_entity")
        return channel(peer.channel_id)

    async def iter_messages(self, entity, limit, **kwargs):
        self.calls.append("iter_messages")
        for msg in self.messages[:limit]:
            yield msg


class FolderTests(unittest.TestCase):
    def test_exact_title_and_emoji_variant(self):
        wanted = folder(title=types.TextWithEntities("🌐\ufe0f", []))
        self.assertIs(exporter.choose_folder([folder(id=1, title="other"), wanted], "🌐"), wanted)
        with self.assertRaises(ValueError):
            exporter.choose_folder([wanted, folder()], "🌐")
        self.assertIs(exporter.choose_folder([wanted, folder(id=8)], "unused", 7), wanted)

    def test_explicit_and_pinned_override_read_mute_archive_rules(self):
        peer = types.InputPeerChannel(101, 42)
        for field in ("include_peers", "pinned_peers"):
            with self.subTest(field=field):
                selected = folder(**{field: [peer]}, exclude_read=True, exclude_muted=True, exclude_archived=True)
                muted = dialog(folder_id=1, notify_settings=types.PeerNotifySettings(mute_until=AT + timedelta(days=1)))
                self.assertTrue(exporter.folder_contains_channel(selected, muted, at=AT))

    def test_explicit_exclusion_wins(self):
        peer = types.InputPeerChannel(101, 42)
        self.assertFalse(exporter.folder_contains_channel(folder(include_peers=[peer], exclude_peers=[peer], broadcasts=True), dialog(), at=AT))

    def test_dynamic_mute_defaults_unread_mentions_and_archive(self):
        selected = folder(broadcasts=True, exclude_muted=True, exclude_read=True)
        item = dialog()
        self.assertFalse(exporter.folder_contains_channel(selected, item, at=AT))
        item.unread_count = 3
        self.assertFalse(exporter.folder_contains_channel(selected, item, AT + timedelta(days=1), AT))
        item.dialog.unread_mentions_count = 1
        self.assertTrue(exporter.folder_contains_channel(selected, item, AT + timedelta(days=1), AT))
        item.dialog.folder_id = 1
        self.assertFalse(exporter.folder_contains_channel(selected, item, AT + timedelta(days=1), AT))
        item.dialog.notify_settings.mute_until = AT - timedelta(days=1)
        self.assertTrue(exporter.folder_contains_channel(selected, item, AT + timedelta(days=1), AT))

    def test_group_is_not_a_channel(self):
        group = types.Channel(101, "Группа", types.ChatPhotoEmpty(), AT, megagroup=True)
        self.assertFalse(exporter.folder_contains_channel(folder(broadcasts=True, include_peers=[types.InputPeerChannel(101, 42)]), dialog(group)))


class ContentTests(unittest.TestCase):
    def test_full_text_utf16_hidden_and_button_urls(self):
        url = "https://example.org/article"
        text = "🧠 " + url + " подробности " + "а" * 6000
        msg = message(5, message=text, entities=[types.MessageEntityUrl(3, len(url)), types.MessageEntityTextUrl(0, 2, "https://example.org/hidden")],
                      reply_markup=types.ReplyInlineMarkup([types.KeyboardInlineButtonRow([types.KeyboardInlineButton("Читать", types.InlineButtonTypeUrl("https://example.org/button"))])]))
        result = exporter.serialize_message(msg, channel())
        self.assertEqual(result["text"], text)
        self.assertEqual(result["urls"], [url, "https://example.org/hidden", "https://example.org/button"])
        self.assertEqual(result["telegram_url"], "https://t.me/example/5")

    def test_known_video_duration_preview_and_private_post_url(self):
        doc = types.Document(id=1, access_hash=2, file_reference=b"private-reference", date=AT,
                             mime_type="video/mp4", size=500,
                             dc_id=2, attributes=[types.DocumentAttributeVideo(duration=321.5, w=640, h=360)])
        info = exporter.media_info(message(1, media=types.MessageMediaDocument(document=doc)))
        self.assertEqual(info["duration_seconds"], 321.5)
        self.assertNotIn("file_reference", info)
        private = channel()
        private.username = None
        self.assertEqual(exporter.post_link(private, 7), "https://t.me/c/101/7")
        preview = types.WebPage(1, "https://example.org", "example.org", 2, description="Описание")
        data = exporter.serialize_message(message(2, media=types.MessageMediaWebPage(preview)), channel())
        self.assertEqual(data["media"]["link_preview"]["description"], "Описание")


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_album_at_boundary_is_whole_and_service_messages_are_skipped(self):
        service = types.MessageService(10, types.PeerChannel(101), AT, types.MessageActionHistoryClear())
        fake = FakeClient([service, message(9), message(8, grouped_id=100), message(7, grouped_id=100), message(6)])
        result = await exporter.collect_posts(fake, channel(), 2)
        self.assertEqual(result["publication_count"], 2)
        self.assertEqual(result["message_count"], 3)
        self.assertEqual([m["id"] for m in result["posts"][1]["messages"]], [7, 8])
        self.assertFalse(result["history_exhausted"])
        self.assertEqual(result["posts"][0]["rank_newest_first"], 1)

    async def test_short_channel_and_textless_media_are_preserved(self):
        fake = FakeClient([message(3, message="", media=types.MessageMediaPhoto(photo=types.PhotoEmpty(3)))])
        result = await exporter.collect_posts(fake, channel(), 35)
        self.assertTrue(result["history_exhausted"])
        self.assertEqual(result["publication_count"], 1)
        self.assertEqual(result["posts"][0]["text"], "")

    async def test_manual_folder_does_not_read_personal_dialogs(self):
        selected = folder(pinned_peers=[types.InputPeerChannel(101, 42)],
                          include_peers=[types.InputPeerChannel(101, 42), types.InputPeerUser(20, 21), types.InputPeerChat(3)])
        fake = FakeClient([])
        channels, issues, skipped, dynamic = await exporter.folder_channels(fake, selected)
        self.assertEqual(len(channels), 1)
        self.assertEqual(fake.calls, ["get_entity"])
        self.assertEqual(skipped, 2)
        self.assertEqual(issues, [])
        self.assertFalse(dynamic)

    async def test_end_to_end_output_has_no_credentials_or_access_hashes(self):
        selected = folder(include_peers=[types.InputPeerChannel(101, 42)])
        fake = FakeClient([message(10, message="Канал, статья и механизм")], selected)
        with TemporaryDirectory() as temp:
            args = argparse.Namespace(state_dir=Path(temp) / "state", output_dir=Path(temp) / "out",
                                      folder="🌐", folder_id=None, expect_channels=1, limit=35)
            with patch.object(exporter, "TelegramClient", return_value=fake), patch.dict("os.environ", {"TG_API_ID": "12345", "TG_API_HASH": "abcdef0123456789abcdef0123456789"}):
                await exporter.run(args)
            result = json.loads(next(args.output_dir.glob("*.json")).read_text())
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["channels"][0]["publication_count"], 1)
            serialized = json.dumps(result)
            for secret in ("abcdef0123456789abcdef0123456789", "987654321", "access_hash", "api_hash", "account.session"):
                self.assertNotIn(secret, serialized)
            self.assertTrue(fake.disconnected)
            self.assertEqual(fake.calls, ["connect", "GetDialogFiltersRequest", "get_entity", "iter_messages"])


if __name__ == "__main__":
    unittest.main()
