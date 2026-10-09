---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Database Internals]]"
stage: 12
status: planned
hours_estimate: 45-75
---

# MVCC, WAL and LSM

**Problem:** сохранить transactional correctness и восстановить состояние после crash.

## Build

- [ ] Пройти CMU Concurrency Control project.
- [ ] Завершить official Recovery homework.
- [ ] Добавить WAL/checkpoint recovery experiment в durable engine `in-memory-database`.
- [ ] Построить LSM prototype или compaction simulator.
- [ ] Измерить read/write/space amplification.

## Break

- [ ] Crash до и после WAL flush.
- [ ] Checkpoint пересекается с active transaction.
- [ ] Abort после partial update.
- [ ] Long snapshot удерживает garbage.
- [ ] Compaction crash и tombstone resurrection.

## Evidence and Done

- [ ] WAL-before-data показано тестом.
- [ ] Recovery идемпотентен.
- [ ] MVCC visibility проверяется для concurrent snapshots.
- [ ] LSM benchmark объясняет минимум два вида amplification.
- [ ] Пройден [[40 - Projects/Distributed Systems Learning/00 - Roadmap#Gate D — после этапа 12|Gate D]].
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#12. MVCC, WAL, recovery и LSM — 45–75 часов|Roadmap]].
