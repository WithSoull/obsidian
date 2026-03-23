# Repository Guidelines

## Core Rules

- Communicate with the author in Russian.
- Write notes in Russian unless the naming rules below require English titles.
- Keep notes concise, structured, and useful for quick context recovery.
- Prefer practical backend examples, especially around Go, storage, networking, concurrency, and distributed systems.

## Vault Map

- `30 - Learning`: main technical knowledge base; default starting point for technical topics.
- `10 - Work`: job-specific context; search only for work tasks or company-specific notes.
- `20 - Mentorship`: mentee-specific materials; search by person or mentorship topic.
- `99 - Meta`: vault maintenance, scripts, templates, and Codex workflow files.
- `.obsidian`: configuration only; avoid editing plugin files under `.obsidian/plugins/`.
- `../private`: out of scope for this repository workflow; do not open files there, run search there, or use it as fallback context even if the environment technically allows access.

## How To Search

Treat the vault as a graph, not a flat file tree.

1. Start from the folder or note explicitly named by the user.
2. In `30 - Learning`, open the nearest `_MOC - ...` note first when it exists.
3. Follow direct wikilinks from that note and go one level deeper if needed.
4. Only then use targeted `rg` inside that branch.
5. Search the whole vault only for cross-cutting tasks or when bounded search fails.

Additional retrieval rules:

- Multi-level MOC structure is intentional. An incomplete MOC usually means the topic is not studied yet, not that the structure is broken.
- For review or expansion tasks: inspect the target note first, then direct links, then the nearest MOC.
- For new notes: find the target branch, inspect sibling notes, then the nearest MOC to match local style and linking.

## DDIA PDF Workflow

- The canonical DDIA source is `30 - Learning/10 - Foundation/30 - DDIA/0 - Book PDFs/2.0 DDIA-original.pdf`.
- When the user asks about DDIA and the answer may benefit from the source text, prefer checking the PDF before relying on memory.
- Use `pdfinfo` to inspect the file and `pdftotext` to search or extract text from the PDF.
- For focused DDIA tasks, prefer this order:
  1. identify the relevant chapter or pages,
  2. extract only the needed page range,
  3. compare it with the target note and nearest `_MOC - ...` note,
  4. then write or revise the note.
- Do not extract the whole book unless full-book search is actually needed.
- For note generation from DDIA, keep the note in Russian, but preserve canonical English technical terms in titles when appropriate.

## DDIA Note Philosophy

- Treat the `30 - DDIA` branch as a personal knowledge base about data-intensive applications, not as a verbatim or section-by-section rewrite of the book.
- Do not assume every subsection of the book must exist as a separate note. Missing notes may simply mean the topic has not yet been internalized or is intentionally deferred.
- Preserve and respect the author's own examples, hypotheses, comparisons, and conclusions even when they go beyond the book, as long as they are clearly useful and not factually wrong.
- Prefer helping the author think, compare, and sharpen ideas over maximizing coverage of the source text.
- When auditing DDIA notes against the book, distinguish clearly between:
  - factual mistakes or misleading statements,
  - genuinely missing concepts that would improve the note set,
  - and deliberate omissions or author-added material that is outside the book but still valuable.
- Avoid framing gaps as problems just because a topic from the book is absent. Coverage is not the goal by itself; understanding and retrieval are.
- When extending DDIA notes, prefer adding material only where it improves the author's mental model, cross-links, or practical recall.

## Note Quality

- Good notes should be concrete, technically correct, and reusable.
- Prefer operational insight over generic theory.
- Add Obsidian links only when they improve retrieval or show a real dependency between concepts.
- Put new notes in the most specific relevant folder unless the user asks otherwise.

## Naming

- Ordered folders must use `NN - Title`.
- Technical note names should be in English when the meaning is unambiguous.
- Regular note names should use concise `Title Case`.
- MOC notes must use `_MOC - Topic`.
- Comparison notes should use `A vs B`.
- Avoid placeholder names like `Untitled` or `Без названия`.
- Avoid mixed-language names unless there is a strong reason.

## Rename And Link Safety

- After renaming, moving, or deleting notes, run a broken-link check and fix any breakages introduced by the current task.
- Do not keep renaming purely for polish once retrieval is already good enough.

## Git Workflow

- Use `.codex/bin/safe-commit "<message>"` for normal commits.
- Do not run `git add` before `safe-commit`.
- `safe-commit` stages all current changes. If unrelated changes exist, say they will be included.
- Commit at the end of each completed user request.
- Commit messages must be short plain-English descriptions.
- Work in a single branch.
- Do not rewrite history and do not undo or revert commits unless the user explicitly asks.
- Only 1 author of commits: withsoull
