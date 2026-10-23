#!/usr/bin/env python3
"""Read a Telegram folder and export channel posts; never send or mark read."""

import argparse
import asyncio
import getpass
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
from uuid import uuid4

from telethon import TelegramClient, errors, functions, types, utils


ROOT = Path(__file__).resolve().parent
UTC = timezone.utc


def now():
    return datetime.now(UTC)


def iso(value):
    return value.isoformat() if value else None


def normalized_title(value):
    return str(value).replace("\ufe0f", "").replace("\ufe0e", "").strip()


def folder_title(folder):
    title = getattr(folder, "title", "")
    return getattr(title, "text", title)


def choose_folder(filters, title, folder_id=None):
    matches = [f for f in filters if getattr(f, "id", None) == folder_id] if folder_id is not None else [
        f for f in filters if normalized_title(folder_title(f)) == normalized_title(title)
    ]
    if len(matches) != 1:
        available = ", ".join(f"{getattr(f, 'id', '?')}: {folder_title(f)}" for f in filters)
        raise ValueError(f"Нужна ровно одна папка {title!r}. Найдено: {len(matches)}. Папки: {available}. Используйте --folder-id при совпадении имён.")
    if isinstance(matches[0], types.DialogFilterDefault):
        raise ValueError("Общую папку всех чатов экспортировать нельзя; выберите отдельную папку.")
    return matches[0]


def peer_ids(peers):
    return {utils.get_peer_id(p) for p in peers}


def broadcast(entity):
    return isinstance(entity, (types.Channel, types.ChannelForbidden)) and bool(getattr(entity, "broadcast", False))


def folder_contains_channel(folder, dialog, default_mute_until=None, at=None):
    """Match server-side rules. Explicit includes override dynamic exclusions."""
    if not broadcast(dialog.entity):
        return False
    channel_id = utils.get_peer_id(dialog.entity)
    if channel_id in peer_ids(getattr(folder, "exclude_peers", [])):
        return False
    explicit = peer_ids(folder.include_peers) | peer_ids(folder.pinned_peers)
    if channel_id in explicit:
        return True
    if not getattr(folder, "broadcasts", False):
        return False
    archived = getattr(dialog.dialog, "folder_id", None) == 1
    if getattr(folder, "exclude_archived", False) and archived:
        return False
    mentions = getattr(dialog.dialog, "unread_mentions_count", 0) or 0
    unread = bool(dialog.unread_count or getattr(dialog.dialog, "unread_mark", False) or mentions)
    if getattr(folder, "exclude_read", False) and not unread:
        return False
    settings = getattr(dialog.dialog, "notify_settings", None)
    mute_until = getattr(settings, "mute_until", None)
    if mute_until is None:
        mute_until = default_mute_until
    muted = bool(mute_until and mute_until > (at or now()))
    if getattr(folder, "exclude_muted", False) and muted and not (mentions and not archived):
        return False
    return True


def post_link(entity, message_id):
    username = getattr(entity, "username", None)
    return f"https://t.me/{username}/{message_id}" if username else f"https://t.me/c/{entity.id}/{message_id}"


def entity_slice(text, offset, length):
    # Telegram offsets count UTF-16 code units, not Python code points.
    return text.encode("utf-16-le")[offset * 2:(offset + length) * 2].decode("utf-16-le")


def extract_urls(message):
    urls = []
    for entity in message.entities or []:
        if isinstance(entity, types.MessageEntityTextUrl):
            urls.append(entity.url)
        elif isinstance(entity, types.MessageEntityUrl):
            urls.append(entity_slice(message.message or "", entity.offset, entity.length))
    preview = getattr(getattr(message, "media", None), "webpage", None)
    if getattr(preview, "url", None):
        urls.append(preview.url)
    for row in getattr(getattr(message, "reply_markup", None), "rows", []):
        for button in row.buttons:
            url = getattr(button, "url", None) or getattr(getattr(button, "type", None), "url", None)
            if url:
                urls.append(url)
    return list(dict.fromkeys(urls))


def media_info(message):
    media = message.media
    if not media:
        return None
    result = {"type": type(media).__name__, "downloaded": False}
    doc = getattr(media, "document", None)
    if doc:
        result.update(mime_type=getattr(doc, "mime_type", None), size_bytes=getattr(doc, "size", None))
        for attr in getattr(doc, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                result["file_name"] = attr.file_name
            elif isinstance(attr, (types.DocumentAttributeAudio, types.DocumentAttributeVideo)):
                result["duration_seconds"] = attr.duration
                for key in ("title", "performer", "voice", "round_message"):
                    value = getattr(attr, key, None)
                    if value is not None:
                        result[key] = value
    webpage = getattr(media, "webpage", None)
    if isinstance(webpage, types.WebPage):
        result["link_preview"] = {
            key: getattr(webpage, key, None)
            for key in ("url", "display_url", "site_name", "title", "description", "duration")
        }
    poll = getattr(media, "poll", None)
    if poll:
        question = poll.question
        result["question"] = getattr(question, "text", question)
        result["answers"] = [getattr(a.text, "text", a.text) for a in poll.answers]
    return result


def serialize_message(message, entity):
    forwarded = message.fwd_from
    source = getattr(forwarded, "from_id", None)
    forward_channel = source.channel_id if isinstance(source, types.PeerChannel) else None
    return {
        "id": message.id,
        "date": iso(message.date),
        "edit_date": iso(message.edit_date),
        "text": message.message or "",
        "telegram_url": post_link(entity, message.id),
        "urls": extract_urls(message),
        "media": media_info(message),
        "grouped_id": str(message.grouped_id) if message.grouped_id else None,
        "forwarded": forwarded is not None,
        "forward_channel_id": forward_channel,
        "forward_post_id": getattr(forwarded, "channel_post", None),
        "reply_to_message_id": getattr(message.reply_to, "reply_to_msg_id", None),
    }


async def collect_posts(client, entity, limit):
    """Count an album as one publication and finish its boundary group."""
    posts = []
    scanned = 0
    scan_limit = max(200, limit * 20)
    exhausted = True
    async for message in client.iter_messages(entity, limit=scan_limit, wait_time=1):
        scanned += 1
        if not isinstance(message, types.Message):
            continue
        key = f"album:{message.grouped_id}" if message.grouped_id else f"post:{message.id}"
        if posts and posts[-1]["key"] == key:
            posts[-1]["messages"].append(serialize_message(message, entity))
        elif len(posts) < limit:
            posts.append({"key": key, "messages": [serialize_message(message, entity)]})
        else:
            exhausted = False
            break
    for position, post in enumerate(posts, 1):
        post["messages"].sort(key=lambda m: m["id"])
        post["rank_newest_first"] = position
        post["telegram_url"] = post["messages"][0]["telegram_url"]
        post["date"] = post["messages"][0]["date"]
        post["text"] = "\n\n".join(m["text"] for m in post["messages"] if m["text"])
        post["urls"] = list(dict.fromkeys(u for m in post["messages"] for u in m["urls"]))
    return {
        "posts": posts,
        "publication_count": len(posts),
        "message_count": sum(len(p["messages"]) for p in posts),
        "history_exhausted": exhausted and scanned < scan_limit,
        "scan_limit_reached": scanned == scan_limit,
        "scan_limit": scan_limit,
    }


async def folder_channels(client, folder):
    # Manual/shared folders need no scan of other dialogs at all.
    channels = {}
    issues = []
    excluded = peer_ids(getattr(folder, "exclude_peers", []))
    explicit = list(folder.pinned_peers) + list(folder.include_peers)
    seen = set()
    skipped = 0
    for peer in explicit:
        marked_id = utils.get_peer_id(peer)
        if marked_id in seen or marked_id in excluded:
            continue
        seen.add(marked_id)
        if not isinstance(peer, types.InputPeerChannel):
            skipped += 1
            continue
        try:
            entity = await client.get_entity(peer)
            if broadcast(entity):
                channels[marked_id] = entity
            else:
                skipped += 1
        except (errors.RPCError, ValueError) as error:
            issues.append({"channel_id": marked_id, "stage": "resolve_explicit_channel", "error_type": type(error).__name__})
    dynamic = bool(getattr(folder, "broadcasts", False))
    if dynamic:
        default_mute_until = None
        if getattr(folder, "exclude_muted", False):
            settings = await client(functions.account.GetNotifySettingsRequest(types.InputNotifyBroadcasts()))
            default_mute_until = settings.mute_until
        at = now()
        async for dialog in client.iter_dialogs(ignore_migrated=True):
            if folder_contains_channel(folder, dialog, default_mute_until, at):
                channels[utils.get_peer_id(dialog.entity)] = dialog.entity
    return list(channels.values()), issues, skipped, dynamic


def write_export(path, data):
    temp = path.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(temp, path)


async def authorize(client):
    if await client.is_user_authorized():
        return
    phone = input("Номер Telegram нужного аккаунта (с +): ").strip()
    await client.send_code_request(phone)
    for attempt in range(3):
        try:
            code = getpass.getpass("Код входа из Telegram (ввод скрыт): ").strip().replace(" ", "")
            await client.sign_in(phone=phone, code=code)
            return
        except errors.SessionPasswordNeededError:
            for password_attempt in range(3):
                try:
                    await client.sign_in(password=getpass.getpass("Пароль 2FA (ввод скрыт): "))
                    return
                except errors.PasswordHashInvalidError:
                    print("Неверный пароль 2FA.", file=sys.stderr)
            raise ValueError("Не удалось подтвердить пароль 2FA. Запустите снова.")
        except errors.PhoneCodeInvalidError:
            print("Неверный код входа.", file=sys.stderr)
    raise ValueError("Не удалось подтвердить код входа. Запустите снова.")


async def run(args):
    api_id_text = os.environ.get("TG_API_ID") or input("api_id: ").strip()
    api_hash = os.environ.get("TG_API_HASH") or getpass.getpass("api_hash (ввод скрыт): ").strip()
    if not api_id_text.isdigit() or not re.fullmatch(r"[0-9a-fA-F]{32}", api_hash):
        raise ValueError("Проверьте api_id (число) и api_hash (32 шестнадцатеричных символа).")
    state = args.state_dir.expanduser().resolve()
    state.mkdir(mode=0o700, parents=True, exist_ok=True)
    state.chmod(0o700)
    client = TelegramClient(str(state / "account"), int(api_id_text), api_hash,
                            receive_updates=False, flood_sleep_threshold=30,
                            device_model="Telegram Reading Export")
    data = None
    output = None
    try:
        await client.connect()
        await authorize(client)
        result = await client(functions.messages.GetDialogFiltersRequest())
        folder = choose_folder(getattr(result, "filters", result), args.folder, args.folder_id)
        print(f"Папка подтверждена: {folder_title(folder)} (id={folder.id})", flush=True)
        channels, issues, skipped, dynamic = await folder_channels(client, folder)
        print(f"Каналов: {len(channels)}. Пропущено явно включённых групп/ботов/личных чатов: {skipped}.", flush=True)
        for number, channel in enumerate(channels, 1):
            username = getattr(channel, "username", None)
            print(f"  {number:2}. {channel.title}" + (f" (@{username})" if username else " (закрытый канал)"), flush=True)
        if args.expect_channels is not None and len(channels) != args.expect_channels:
            print(f"Внимание: ожидалось {args.expect_channels} каналов; найдено {len(channels)}. Состав сохранён для сверки.", flush=True)
        args.output_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        output = args.output_dir / f"telegram-reading-{now():%Y%m%d-%H%M%S}-{uuid4().hex[:6]}.json"
        data = {
            "schema_version": 1,
            "exported_at": iso(now()),
            "finished_at": None,
            "status": "in_progress",
            "folder": {"id": folder.id, "title": folder_title(folder),
                       "dynamic_channels_rule": dynamic,
                       "membership_snapshot_at": iso(now()),
                       "membership_complete": not issues},
            "requested_publications_per_channel": args.limit,
            "analysis_rule": "Read newest five first; inspect the previous thirty only if the first five justify it. Exporting is not reading or verifying sources.",
            "limitations": ["Media files and external sources have not been downloaded or verified.",
                             "Link previews are Telegram metadata, not a verification of the source.",
                             "Private post URLs require membership in the channel.",
                             "Dynamic unread/mute rules reflect a server snapshot, not another client's transient UI state."],
            "issues": issues,
            "channels": [{"id": ch.id, "title": ch.title, "username": getattr(ch, "username", None),
                          "url": f"https://t.me/{ch.username}" if getattr(ch, "username", None) else None,
                          "status": "pending", "posts": []} for ch in channels],
        }
        write_export(output, data)
        for index, (entity, channel) in enumerate(zip(channels, data["channels"]), 1):
            print(f"[{index}/{len(channels)}] {entity.title}", flush=True)
            try:
                channel.update(await collect_posts(client, entity, args.limit))
                channel["status"] = "scan_limit_reached" if channel["scan_limit_reached"] else "ok"
                print(f"  {channel['publication_count']} публикаций / {channel['message_count']} сообщений", flush=True)
            except (errors.RPCError, ValueError, OSError) as error:
                channel["status"] = "error"
                channel["error_type"] = type(error).__name__
                print(f"  Не удалось выгрузить: {type(error).__name__}", flush=True)
            write_export(output, data)
            if index < len(channels):
                await asyncio.sleep(0.5)
        data["status"] = "complete" if not issues and all(c["status"] == "ok" for c in data["channels"]) else "partial"
        data["finished_at"] = iso(now())
        write_export(output, data)
        print(f"\nРезультат ({data['status']}): {output.resolve()}", flush=True)
        print("Передайте только этот JSON или его путь. Файл сессии остаётся локально.", flush=True)
    finally:
        await client.disconnect()
        if output and data and data["status"] == "in_progress":
            print(f"Незавершённая выгрузка сохранена: {output.resolve()}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Выгрузить каналы из папки Telegram в JSON без изменения чатов и настроек.")
    parser.add_argument("--folder", default="🌐", help="Точное имя папки (по умолчанию 🌐)")
    parser.add_argument("--folder-id", type=int, help="ID папки, если имена совпадают")
    parser.add_argument("--limit", type=int, default=35, help="Публикаций на канал; альбом считается одной (по умолчанию 35)")
    parser.add_argument("--expect-channels", type=int, help="Предупредить при другом количестве каналов")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "exports")
    parser.add_argument("--state-dir", type=Path, default=Path.home() / ".local/state/telegram-reading-export")
    args = parser.parse_args()
    if not 1 <= args.limit <= 1000:
        parser.error("--limit должен быть от 1 до 1000")
    os.umask(0o077)
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\nОстановлено. Уже записанные результаты сохранены.", file=sys.stderr)
        return 130
    except errors.FloodWaitError as error:
        print(f"Telegram просит паузу {error.seconds} сек. Повторите запуск позже.", file=sys.stderr)
        return 1
    except (errors.RPCError, ValueError, OSError, RuntimeError, EOFError) as error:
        # Never print raw RPC requests, credentials, account objects or session data.
        detail = str(error) if isinstance(error, ValueError) else type(error).__name__
        print(f"Ошибка: {detail}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
