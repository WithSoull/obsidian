# Rename Script

Скрипт для пакетного переименования папок и заметок с обновлением ссылок по vault.

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

`parent` должен указывать на текущее имя папки до запуска скрипта.

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
- не трогает `.git`

## Что не делает

- не придумывает новые имена
- не проверяет broken links за тебя
- не коммитит автоматически
