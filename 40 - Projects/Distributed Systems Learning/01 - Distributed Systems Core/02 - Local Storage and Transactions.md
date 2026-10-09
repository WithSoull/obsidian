---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 2
status: planned
hours_estimate: 32-48
---

# Local Storage and Transactions

**Problem:** определить durability локальной записи и допустимые concurrent histories до появления replication.

## Build

- [ ] Добавить в `in-memory-database` durable append-only engine за интерфейсом `Engine`.
- [ ] Реализовать framing, checksum, recovery scan и compaction.
- [ ] Воспроизвести в PostgreSQL lost update, write skew, phantom и deadlock.
- [ ] Защитить один invariant через `FOR UPDATE`, optimistic version и `SERIALIZABLE` + retry.
- [ ] Сравнить correctness, contention и сложность вариантов.

## Break

- [ ] Kill между append, sync и ack.
- [ ] Truncated tail и bit flip.
- [ ] Crash во время compaction/swap.
- [ ] Serialization failure рядом с внешним side effect.

## Evidence and Done

- [ ] Recovery не принимает повреждённую запись.
- [ ] У append определён commit point.
- [ ] Каждая anomaly имеет воспроизводимый trace.
- [ ] Retry не дублирует внешний effect.
- [ ] Пройден [[40 - Projects/Distributed Systems Learning/00 - Roadmap#Gate A — после этапа 2|Gate A]].
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#2. Local storage, crash consistency и транзакции — 32–48 часов|Roadmap]].
