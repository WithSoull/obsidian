import argparse
import asyncio
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
TEST_ENV = {"TG_API_ID": "12345", "TG_API_HASH": "abcdef0123456789abcdef0123456789"}


def export_args(temp):
    return argparse.Namespace(output_dir=Path(temp) / "out", folder="🌐", folder_id=None,
                              expect_channels=1, limit=35)


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
        self.connected = False
        self.session = SimpleNamespace(auth_key=None)

    async def connect(self):
        self.calls.append("connect")
        self.connected = True
        self.session.auth_key = b"fake-auth-key"

    async def disconnect(self):
        self.disconnected = True
        self.connected = False

    def is_connected(self):
        return self.connected

    async def log_out(self):
        self.calls.append("log_out")
        await self.disconnect()
        self.session = None
        return True

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
            args = export_args(temp)
            with patch.object(exporter, "TelegramClient", return_value=fake) as factory, patch.dict("os.environ", TEST_ENV):
                await exporter.run(args)
            self.assertIsInstance(factory.call_args.args[0], exporter.MemorySession)
            self.assertEqual(list(Path(temp).rglob("*.session*")), [])
            result = json.loads(next(args.output_dir.glob("*.json")).read_text())
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["session_cleanup"], {"storage": "memory", "status": "revoked"})
            self.assertEqual(result["channels"][0]["publication_count"], 1)
            serialized = json.dumps(result)
            for secret in ("abcdef0123456789abcdef0123456789", "987654321", "access_hash", "api_hash", "account.session"):
                self.assertNotIn(secret, serialized)
            self.assertTrue(fake.disconnected)
            self.assertEqual(fake.calls, ["connect", "GetDialogFiltersRequest", "get_entity", "iter_messages", "log_out"])

    async def test_logout_runs_on_error_before_export_and_preserves_original_error(self):
        fake = FakeClient([])
        with TemporaryDirectory() as temp, patch.object(exporter, "TelegramClient", return_value=fake), patch.dict("os.environ", TEST_ENV), patch.object(exporter, "authorize", side_effect=ValueError("login failed")):
            with self.assertRaisesRegex(ValueError, "login failed"):
                await exporter.run(export_args(temp))
        self.assertIn("log_out", fake.calls)
        self.assertTrue(fake.disconnected)

    async def test_cancelled_export_still_revokes_and_keeps_partial_json(self):
        entered = asyncio.Event()

        class BlockingClient(FakeClient):
            async def iter_messages(self, *args, **kwargs):
                entered.set()
                await asyncio.Event().wait()
                yield message(10)

        selected = folder(include_peers=[types.InputPeerChannel(101, 42)])
        fake = BlockingClient([], selected)
        with TemporaryDirectory() as temp, patch.object(exporter, "TelegramClient", return_value=fake), patch.dict("os.environ", TEST_ENV):
            args = export_args(temp)
            task = asyncio.create_task(exporter.run(args))
            await entered.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
            result = json.loads(next(args.output_dir.glob("*.json")).read_text())
            self.assertEqual(result["status"], "in_progress")
            self.assertEqual(result["session_cleanup"]["status"], "revoked")
        self.assertTrue(fake.disconnected)

    async def test_cancel_during_logout_does_not_cancel_revocation(self):
        entered = asyncio.Event()
        release = asyncio.Event()

        class SlowLogoutClient(FakeClient):
            async def log_out(self):
                entered.set()
                await release.wait()
                return await super().log_out()

        selected = folder(include_peers=[types.InputPeerChannel(101, 42)])
        fake = SlowLogoutClient([message(10)], selected)
        with TemporaryDirectory() as temp, patch.object(exporter, "TelegramClient", return_value=fake), patch.dict("os.environ", TEST_ENV):
            args = export_args(temp)
            task = asyncio.create_task(exporter.run(args))
            await entered.wait()
            task.cancel()
            release.set()
            with self.assertRaises(asyncio.CancelledError):
                await task
            result = json.loads(next(args.output_dir.glob("*.json")).read_text())
            self.assertEqual(result["session_cleanup"]["status"], "revoked")
        self.assertTrue(fake.disconnected)

    async def test_rejected_logout_is_an_error_even_when_export_is_complete(self):
        class RejectedLogoutClient(FakeClient):
            async def log_out(self):
                return False

        selected = folder(include_peers=[types.InputPeerChannel(101, 42)])
        fake = RejectedLogoutClient([message(10)], selected)
        with TemporaryDirectory() as temp, patch.object(exporter, "TelegramClient", return_value=fake), patch.dict("os.environ", TEST_ENV):
            args = export_args(temp)
            with self.assertRaises(exporter.SessionCleanupError):
                await exporter.run(args)
            result = json.loads(next(args.output_dir.glob("*.json")).read_text())
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["session_cleanup"]["status"], "unconfirmed")
        self.assertTrue(fake.disconnected)

    async def test_logout_timeout_is_not_reported_as_success(self):
        class HungLogoutClient(FakeClient):
            async def log_out(self):
                await asyncio.Event().wait()

        fake = HungLogoutClient([])
        await fake.connect()
        result = await exporter.close_temporary_session(fake, timeout=0.01)
        self.assertEqual(result["status"], "unconfirmed")
        self.assertEqual(result["error_type"], "TimeoutError")
        self.assertTrue(fake.disconnected)

    async def test_logout_reconnects_if_export_lost_the_connection(self):
        fake = FakeClient([])
        await fake.connect()
        await fake.disconnect()
        result = await exporter.close_temporary_session(fake)
        self.assertEqual(result["status"], "revoked")
        self.assertEqual(fake.calls, ["connect", "connect", "log_out"])

    async def test_no_logout_request_when_connection_created_no_key(self):
        fake = FakeClient([])
        result = await exporter.close_temporary_session(fake)
        self.assertEqual(result["status"], "not_created")
        self.assertEqual(fake.calls, [])


if __name__ == "__main__":
    unittest.main()
