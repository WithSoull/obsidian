---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 3
status: planned
hours_estimate: 16-26
---

# Replication and Quorums

**Problem:** связать acknowledged write и read semantics с lag, partition и failover.

## Build

- [ ] В учебной ветке `in-memory-database` поднять leader и двух followers.
- [ ] Реализовать `leader-only` и `quorum` acknowledgements.
- [ ] Реализовать reads с leader, любой replica и minimum sequence.
- [ ] Реализовать bootstrap follower через snapshot + log tail.

## Break

- [ ] Slow follower.
- [ ] Потеря leader до и после quorum ack.
- [ ] Изоляция старого leader и stale read после failover.
- [ ] Corrupted follower tail.

## Evidence and Done

- [ ] Ack policy связана с конкретным RPO.
- [ ] Старый leader fenced новой epoch.
- [ ] Lag измеряется временем и log distance.
- [ ] Объяснены ограничения формулы `R + W > N`.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#3. Репликация, lag и quorum — 16–26 часов|Roadmap]].
