---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Production Integration]]"
stage: 9
status: planned
hours_estimate: 24-40
---

# System Design and Code Reading

**Problem:** собрать primitives в архитектуру и находить их реальную реализацию в чужом коде.

## Build

- [ ] Решить четыре design case: object storage, messenger, ticket booking, feed/search.
- [ ] Для каждого провести 45-минутную защиту и failure review.
- [ ] В etcd, CockroachDB или RustFS проследить один invariant по code path.
- [ ] Написать report `hypothesis → evidence → unresolved questions`.

## Break

- [ ] Primary cache/database unavailable.
- [ ] Duplicate message после consumer crash.
- [ ] Конкурентная покупка последнего ресурса.
- [ ] Shard move, region partition и stale client.
- [ ] Traffic x10 при degraded dependency.

## Evidence and Done

- [ ] Requirements отделены от архитектуры.
- [ ] Capacity estimates имеют единицы.
- [ ] Каждый компонент оправдан invariant, load или failure requirement.
- [ ] Утверждения о production-коде подтверждены кодом/tests.
- [ ] Пройден [[40 - Projects/Distributed Systems Learning/00 - Roadmap#Gate C — после этапа 9|Gate C]].
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#9. System design и production-code reading — 24–40 часов|Roadmap]].
