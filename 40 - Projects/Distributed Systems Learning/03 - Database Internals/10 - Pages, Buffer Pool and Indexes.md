---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Database Internals]]"
stage: 10
status: planned
hours_estimate: 50-80
---

# Pages, Buffer Pool and Indexes

**Problem:** связать disk layout, page lifetime, cache policy и index invariants.

## Build

- [ ] Пройти C++ Primer при необходимости.
- [ ] Пройти CMU Buffer Pool Manager project.
- [ ] Пройти CMU Database Index project.
- [ ] Добавить invariant checker и randomized oracle.
- [ ] Измерить hit ratio и write amplification.

## Break

- [ ] Все frames pinned.
- [ ] Dirty victim и I/O error.
- [ ] Concurrent split/merge.
- [ ] Duplicate/boundary key и corrupted page.
- [ ] Crash между modification и flush.

## Evidence and Done

- [ ] Page lifecycle объясняется от fetch до eviction.
- [ ] Pin leak и lost dirty page ловятся tests.
- [ ] Index сохраняет ordering/reachability invariants.
- [ ] Latch coupling привязан к code path.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#10. Pages, buffer pool и indexes — 50–80 часов|Roadmap]].
