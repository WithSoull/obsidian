---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 5
status: planned
hours_estimate: 28-45
---

# Replicated KV

**Problem:** связать client request, consensus log, state-machine apply и response без duplicate effect.

## Build

- [ ] Пройти MIT Lab 4 Fault-tolerant KV.
- [ ] Зафиксировать mapping request → index/term → applied result.
- [ ] Восстанавливать application state и bounded dedup state одним snapshot.
- [ ] Добавить history- или model-based randomized test.
- [ ] Сопоставить state-machine contract lab с `in-memory-database.Engine` в design note.

## Break

- [ ] Response lost after apply.
- [ ] Leader change while client waits.
- [ ] Duplicate через нового leader.
- [ ] Crash между созданием и установкой snapshot.
- [ ] Partitioned leader не может commit.

## Evidence and Done

- [ ] Один logical request не применяется дважды.
- [ ] Waiter защищён от index reuse.
- [ ] Snapshot согласованно хранит state и dedup metadata.
- [ ] Пройден [[40 - Projects/Distributed Systems Learning/00 - Roadmap#Gate B — после этапа 5|Gate B]].
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#5. Replicated KV и state machine — 28–45 часов|Roadmap]].
