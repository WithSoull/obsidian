#!/usr/bin/env python3
"""Собрать новую версию диплома, сохранив предыдущие сборки."""

import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "Диплом_ГришинИД_v"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md2gost", default=str(Path.home() / "md2gost/.venv/bin/md2gost"))
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build")
    args = parser.parse_args()
    source = ROOT / "Диплом.md"
    if not source.is_file():
        parser.error(f"Не найден исходник: {source}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(re.escape(PREFIX) + r"(\d+)\.docx")
    versions = [int(m[1]) for p in args.output_dir.iterdir() if (m := pattern.fullmatch(p.name))]
    version = max(versions, default=0) + 1
    # Резервируем имя: два одновременных запуска не перезапишут друг друга.
    while True:
        output = args.output_dir / f"{PREFIX}{version:03d}.docx"
        try:
            with output.open("xb"):
                pass
            break
        except FileExistsError:
            version += 1
    try:
        subprocess.run(
            [args.md2gost, "convert", str(source), "--no-title-page", "-o", str(output)],
            check=True,
        )
    except (OSError, subprocess.CalledProcessError, KeyboardInterrupt) as exc:
        output.unlink(missing_ok=True)
        print(f"Не удалось собрать диплом: {exc}", file=sys.stderr)
        return 1
    print(f"Диплом сохранён: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
