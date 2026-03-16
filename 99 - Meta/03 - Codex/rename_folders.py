#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import uuid
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
    kind: str = "dir"

    @property
    def old_path(self) -> Path:
        return self.parent / self.old

    @property
    def new_path(self) -> Path:
        return self.parent / self.new

    @property
    def old_stem(self) -> str:
        return Path(self.old).stem

    @property
    def new_stem(self) -> str:
        return Path(self.new).stem


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
        kind = item.get("kind", "dir")
        if not all(isinstance(v, str) and v for v in (parent, old, new, kind)):
            raise ValueError("Each entry must define non-empty string fields: parent, old, new, kind.")
        if kind not in {"dir", "note"}:
            raise ValueError("kind must be either 'dir' or 'note'.")

        specs.append(RenameSpec(parent=Path(parent), old=old, new=new, kind=kind))

    return specs


def validate_specs(root: Path, specs: list[RenameSpec]) -> None:
    seen_targets: set[Path] = set()
    for spec in specs:
        old_path = root / spec.old_path
        new_path = root / spec.new_path
        same_path = new_path.exists() and os.path.samefile(old_path, new_path)

        if not old_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {spec.old_path}")
        if spec.kind == "dir" and not old_path.is_dir():
            raise NotADirectoryError(f"Source path is not a directory: {spec.old_path}")
        if spec.kind == "note" and not old_path.is_file():
            raise FileNotFoundError(f"Source note does not exist: {spec.old_path}")
        if new_path.exists() and not same_path:
            raise FileExistsError(f"Target path already exists: {spec.new_path}")
        if new_path in seen_targets:
            raise FileExistsError(f"Duplicate target path in mapping: {spec.new_path}")

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
    path_replacements: list[tuple[str, str]] = []
    for spec in sorted(specs, key=lambda s: len(s.old_path.parts), reverse=True):
        path_replacements.append((spec.old_path.as_posix(), spec.new_path.as_posix()))
        if spec.kind == "note" and spec.old_path.suffix == ".md" and spec.new_path.suffix == ".md":
            path_replacements.append(
                (spec.old_path.with_suffix("").as_posix(), spec.new_path.with_suffix("").as_posix())
            )
    note_specs = [spec for spec in specs if spec.kind == "note"]

    changed_files = 0
    for path in iter_text_files(root):
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in path_replacements:
            updated = updated.replace(old, new)
        for spec in note_specs:
            updated = replace_note_wikilinks(updated, spec.old_stem, spec.new_stem)

        if updated != original:
            changed_files += 1
            if not dry_run:
                path.write_text(updated, encoding="utf-8")

    return changed_files


def replace_note_wikilinks(text: str, old_stem: str, new_stem: str) -> str:
    pattern = re.compile(r"(!?\[\[)([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?(\]\])")

    def repl(match: re.Match[str]) -> str:
        prefix, target, anchor, alias, suffix = match.groups()
        if "/" in target or Path(target).stem != old_stem:
            return match.group(0)
        new_target = new_stem
        if Path(target).suffix:
            new_target += Path(target).suffix
        return f"{prefix}{new_target}{anchor or ''}{alias or ''}{suffix}"

    return pattern.sub(repl, text)


def rename_paths(root: Path, specs: list[RenameSpec], dry_run: bool) -> None:
    ordered = sorted(specs, key=lambda s: len(s.old_path.parts), reverse=True)
    for spec in ordered:
        source = root / spec.old_path
        target = root / spec.new_path
        print(f"{spec.old_path.as_posix()} -> {spec.new_path.as_posix()}")
        if not dry_run:
            if target.exists() and os.path.samefile(source, target):
                temp = source.with_name(f".__rename_tmp__{uuid.uuid4().hex}")
                source.rename(temp)
                temp.rename(target)
            else:
                source.rename(target)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rename Obsidian folders and notes from a JSON mapping and update references."
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
        help="Path to a JSON file with entries: {\"parent\": \"...\", \"old\": \"...\", \"new\": \"...\", \"kind\": \"dir|note\"}.",
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
    print(f"[{mode}] {len(specs)} path rename(s)")
    rename_paths(root, specs, dry_run=dry_run)
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
