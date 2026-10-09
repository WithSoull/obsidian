---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 6
status: planned
hours_estimate: 20-34
---

# Distributed Transactions

**Problem:** одна бизнес-операция изменяет несколько independently failing ресурсов.

## Build

- [ ] Реализовать mini-2PC coordinator с durable decision log.
- [ ] Реализовать outbox publisher и idempotent consumer на PostgreSQL.
- [ ] Описать bounded write workflow как state machine.
- [ ] Сравнить 2PC, outbox и compensation для одних и тех же boundaries.

## Break

- [ ] Participant crash after prepare.
- [ ] Coordinator crash до и после durable decision.
- [ ] Commit response lost.
- [ ] Duplicate publish и crash consumer после side effect.

## Evidence and Done

- [ ] In-doubt transaction не выдаётся за aborted.
- [ ] Coordinator после restart повторяет то же decision.
- [ ] Consumer restart не дублирует logical effect.
- [ ] Названы места, где нужна reconciliation.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#6. Distributed transactions — 20–34 часа|Roadmap]].
