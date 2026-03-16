#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".canvas",
    ".json",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
}


@dataclass(frozen=True)
class RenameSpec:
    parent: Path
    old: str
    new: str

    @property
    def old_path(self) -> Path:
        return self.parent / self.old

    @property
    def new_path(self) -> Path:
        return self.parent / self.new


def load_specs(mapping_path: Path) -> list[RenameSpec]:
    data = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Mapping file must contain a JSON array.")

    specs: list[RenameSpec] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each mapping entry must be an object.")

        parent = item.get("parent")
        old = item.get("old")
        new = item.get("new")
        if not all(isinstance(v, str) and v for v in (parent, old, new)):
            raise ValueError("Each entry must define non-empty string fields: parent, old, new.")

        specs.append(RenameSpec(parent=Path(parent), old=old, new=new))

    return specs


def validate_specs(root: Path, specs: list[RenameSpec]) -> None:
    seen_targets: set[Path] = set()
    for spec in specs:
        old_path = root / spec.old_path
        new_path = root / spec.new_path

        if not old_path.exists():
            raise FileNotFoundError(f"Source folder does not exist: {spec.old_path}")
        if not old_path.is_dir():
            raise NotADirectoryError(f"Source path is not a directory: {spec.old_path}")
        if new_path.exists():
            raise FileExistsError(f"Target folder already exists: {spec.new_path}")
        if new_path in seen_targets:
            raise FileExistsError(f"Duplicate target folder in mapping: {spec.new_path}")

        seen_targets.add(new_path)


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            files.append(path)
    return files


def replace_references(root: Path, specs: list[RenameSpec], dry_run: bool) -> int:
    replacements = [
        (spec.old_path.as_posix(), spec.new_path.as_posix())
        for spec in sorted(specs, key=lambda s: len(s.old_path.parts), reverse=True)
    ]

    changed_files = 0
    for path in iter_text_files(root):
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in replacements:
            updated = updated.replace(old, new)

        if updated != original:
            changed_files += 1
            if not dry_run:
                path.write_text(updated, encoding="utf-8")

    return changed_files


def rename_folders(root: Path, specs: list[RenameSpec], dry_run: bool) -> None:
    ordered = sorted(specs, key=lambda s: len(s.old_path.parts), reverse=True)
    for spec in ordered:
        source = root / spec.old_path
        target = root / spec.new_path
        print(f"{spec.old_path.as_posix()} -> {spec.new_path.as_posix()}")
        if not dry_run:
            source.rename(target)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rename Obsidian folders from a JSON mapping and update path-based references."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Vault root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--map",
        required=True,
        dest="mapping_path",
        help="Path to a JSON file with entries: {\"parent\": \"...\", \"old\": \"...\", \"new\": \"...\"}.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes. Without this flag the script only prints a dry run.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.root).resolve()
    mapping_path = Path(args.mapping_path).resolve()
    dry_run = not args.apply

    specs = load_specs(mapping_path)
    validate_specs(root, specs)

    mode = "DRY RUN" if dry_run else "APPLY"
    print(f"[{mode}] {len(specs)} folder rename(s)")
    rename_folders(root, specs, dry_run=dry_run)
    changed_files = replace_references(root, specs, dry_run=dry_run)
    print(f"[{mode}] updated {changed_files} text file(s)")

    if dry_run:
        print("[DRY RUN] no files were modified")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
