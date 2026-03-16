# Repository Guidelines

## Purpose

This repository is a personal Obsidian vault and knowledge base. Its purpose is to help a Go developer who is interested in distributed systems structure technical knowledge, reduce context switching, and keep important ideas easy to revisit later. Notes should optimize for clarity, recall, and practical use in real engineering work.

## Vault Structure

Top-level folders are organized by intent: `00 - Inbox` for quick capture, `10 - Work` for job-related material, `20 - Mentorship` for teaching and coaching notes, `30 - Learning` for study topics, `40 - Projects` for active initiatives, `90 - Archive` for inactive material, and `99 - Meta` for templates and vault management. Obsidian configuration, snippets, plugins, and scripts live in `.obsidian/`.

## Writing Principles

Write notes in Russian and communicate with the author in Russian. Use Markdown and keep notes concise, structured, and reusable. Prefer clear headings, short paragraphs, bullet lists, and examples from backend engineering. Default to explanations that are useful for Go, backend services, networking, storage, concurrency, and distributed systems. Notes should help the author quickly restore context after a break.

## Agent Responsibilities

The assistant should support the vault in these ways:

- Generate new notes from excerpts of technical books and adapt them into clean study material.
- Review existing notes for factual mistakes, weak explanations, ambiguity, or missing engineering nuance.
- Enrich notes with practical details: examples, tradeoffs, production cases, failure modes, and debugging advice.
- Connect theory to real backend practice, especially around Go and distributed systems.
- Help with revision by asking targeted questions, evaluating answers, and pointing to the note where the topic is explained in detail.
- Look for non-obvious but useful connections between notes and suggest or add Obsidian links when the relation improves navigation or understanding.

## Note Quality Standard

Good notes are concrete and technically correct. They should include definitions, why the idea matters, where it is used, common mistakes, and at least one practical example when relevant. When reviewing or expanding a note, prefer adding operational insight over generic theory.

Links between notes should be meaningful, not mechanical. If one note mentions a concept that already has its own note, add an Obsidian wikilink when it improves retrieval or shows a real conceptual dependency. Example: a note about the Go scheduler may link to `[[Goroutines]]` if goroutines are part of the explanation.

## Editing Guidance

Preserve the existing folder naming style with numeric prefixes. Put new notes in the most specific relevant folder instead of the inbox unless the user asks otherwise. Avoid editing vendored plugin files under `.obsidian/plugins/`. Focus changes on notes, templates, snippets, and local scripts only when needed.

- After renaming, moving, or deleting notes, the assistant must run a broken-link check for Obsidian wikilinks and fix any breakages introduced by the current task before finishing.

## Naming Standard

- Folder names with ordering must use the format `NN - Title`.
- Do not mix `NN. Title` and `NN - Title` in the real vault. Use `NN - Title` consistently.
- Technical note names should be in English when the meaning is unambiguous.
- Regular note names should use concise `Title Case`.
- MOC notes must use the format `_MOC - Topic` so they stay near the top of folder listings without using numeric prefixes.
- Comparison notes should use the format `A vs B`.
- Chapter or book-structure notes may use `Chapter N - Title` or `Part N - Title` only when the note is actually about that chapter or part.
- Avoid placeholder names such as `Untitled` or `Без названия`.
- Avoid service prefixes such as `0MOC.` in note names. Use `_MOC - Topic` instead.
- Avoid mixed-language note names unless there is a strong reason to preserve a well-known original term.
- Avoid extra punctuation and duplicated whitespace in note and folder names.
- Prefer canonical engineering terms over literal translation when renaming technical notes.

## Git Workflow

Git is used in this vault for local history and rollback points before larger changes.

- The assistant must use `.codex/bin/safe-commit "<message>"` for normal commits.
- The `safe-commit` script is the default and preferred path for staging and committing changes in this repository.
- The assistant must not run `git add` before `safe-commit`. For normal commits, call `safe-commit` directly.
- The assistant may fall back to direct `git add` / `git commit` only if the script is missing or broken.
- Work happens in a single branch. Do not create feature branches or use PR-based workflows unless the user explicitly asks for them.
- Commit messages must be plain English descriptions of the change.
- At the end of each completed user request, the assistant should create a commit automatically.
- For simplicity, the assistant should rely on `safe-commit`, which stages all current changes with `git add -A` before committing.
- If unrelated or unwanted changes are present in the working tree, the assistant must not try to work around that by manually staging files before `safe-commit`. In that case, the assistant should tell the user that the tree must be cleaned first or that those changes will be included.
- The assistant does not need to inspect the full diff before committing when working under this rule; the commit message should be inferred from the task context when possible.
- The assistant does not need to ask for confirmation before making such commits.
- The assistant may create commits, but must not rewrite history and must not undo or revert existing commits.
- The assistant must never use destructive history-editing commands such as `git reset`, `git rebase --interactive`, `git commit --amend`, or `git revert` unless the user explicitly requests it.
- Only 1 author of commits: withsoull
