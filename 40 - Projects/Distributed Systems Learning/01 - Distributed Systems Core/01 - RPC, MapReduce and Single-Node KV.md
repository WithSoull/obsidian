---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 1
status: planned
hours_estimate: 28-44
---

# RPC, MapReduce and Single-Node KV

**Problem:** сеть допускает delay, loss и неизвестный результат; даже одноузловый сервис должен иметь явные retry и concurrency semantics.

## Start Criteria

- [ ] Названы assumptions о crash и сети.
- [ ] Даны предварительные ответы на вопросы из [[40 - Projects/Distributed Systems Learning/00 - Roadmap#1. RPC, MapReduce и single-node KV — 28–44 часа|спецификации этапа]].

## Build

- [ ] Пройти MIT Lab 1 MapReduce.
- [ ] Пройти MIT Lab 2 Key/Value Server с lock.
- [ ] Зафиксировать linearization points `Get`, `Put` и lock acquisition.
- [ ] В `in-memory-database` описать semantics `SET/GET/DEL`.
- [ ] Добавить versioned conditional write и deterministic concurrent tests.

## Break

- [ ] Worker crash/stall и duplicate task после timeout.
- [ ] Потеря request и response.
- [ ] Concurrent writes одного key.
- [ ] Client crash с удерживаемым lock.

## Evidence and Done

- [ ] Официальные tests и race detector проходят сериями.
- [ ] Есть trace хотя бы одного ambiguous outcome.
- [ ] Объяснены `ErrVersion`, `ErrMaybe`, lease и fencing.
- [ ] Неизвестная history классифицируется как linearizable/non-linearizable.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и источники: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#1. RPC, MapReduce и single-node KV — 28–44 часа|Roadmap]].
