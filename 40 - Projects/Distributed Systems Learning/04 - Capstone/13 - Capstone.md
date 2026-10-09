---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Capstone]]"
stage: 13
status: planned
hours_estimate: 24-40
---

# Capstone

**Problem:** доказать перенос знаний на один bounded subsystem.

## Scope Decision

- [ ] Выбран только один кейс: `in-memory-database` или OpenS3.
- [ ] Названы invariants, workload и границы того, что результат не доказывает.
- [ ] Зафиксированы два отвергнутых решения.

## Build

- [ ] Написать design doc с contract, state machine и failure matrix.
- [ ] Реализовать узкий E2E path.
- [ ] Добавить fault injection и replay/reconciliation command.
- [ ] Провести воспроизводимый load experiment.
- [ ] Найти сходный механизм в production OSS.
- [ ] По возможности сделать небольшой test, issue или patch.

## Break

- [ ] Timeout на каждой commit/side-effect boundary.
- [ ] Duplicate и out-of-order delivery.
- [ ] Process crash на каждой границе состояния.
- [ ] Slow/unavailable dependency и recovery backlog.
- [ ] Concurrent writes одного key.

## Evidence and Done

- [ ] Есть E2E test и автоматизированные failure cases.
- [ ] Нарушения invariants предотвращаются, обнаруживаются или ремонтируются.
- [ ] Результаты нагрузки воспроизводимы.
- [ ] Design doc разделяет runtime, target design и ограничения.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная спецификация кейсов: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#13. Capstone и OSS transfer — 24–40 часов|Roadmap]].
