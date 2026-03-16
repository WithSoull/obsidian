# Rename Script

Скрипт для пакетного переименования папок и `.md`-заметок в Obsidian vault с обновлением ссылок.

## Файлы

- `99 - Meta/03 - Codex/rename_folders.py`
- `99 - Meta/03 - Codex/folder_renames.example.json`

## Формат map-файла

```json
[
  {
    "parent": "30 - Learning/10 - Foundation/40 - Algo",
    "old": "112 - Графы & Деревья",
    "new": "112 - Graphs & Trees",
    "kind": "dir"
  }
]
```

Поля:

- `parent` — родительская папка в текущем состоянии vault
- `old` — текущее имя папки или заметки
- `new` — новое имя
- `kind` — `dir` для папки, `note` для `.md`-заметки

`parent` всегда должен указывать на текущее имя пути до запуска скрипта.

Пример для заметки:

```json
[
  {
    "parent": "30 - Learning/DDIA/00 - Overview",
    "old": "Intro.md",
    "new": "Introduction.md",
    "kind": "note"
  }
]
```

## Как запускать

Сначала dry-run:

```bash
python3 '99 - Meta/03 - Codex/rename_folders.py' --root . --map '99 - Meta/03 - Codex/folder_renames.example.json'
```

`dry-run` = "пробный прогон без изменений". Скрипт только показывает, что он собирается переименовать и сколько файлов он бы переписал, но ничего не меняет на диске.

Потом применение:

```bash
python3 '99 - Meta/03 - Codex/rename_folders.py' --root . --map '99 - Meta/03 - Codex/folder_renames.example.json' --apply
```

## Что делает

- переименовывает папки и заметки по списку
- обновляет текстовые path-based ссылки в `.md`, `.canvas`, `.json`, `.yaml`, `.yml`, `.txt`
- обновляет простые wikilinks при переименовании заметок, например `[[Intro]] -> [[Introduction]]`
- умеет case-only rename на macOS, например `B-tree -> B-Tree`
- не трогает `.git`

## Что не делает

- не придумывает новые имена
- не проверяет broken links за тебя
- не коммитит автоматически

## Ограничения

- Простые wikilinks обновляются только для переименований заметок.
- Скрипт не пытается разрешать двусмысленные ссылки, если одинаковые названия заметок встречаются в разных местах vault.
- Для тестов используй содержимое `99 - Meta/03 - Codex/testdata/`.
