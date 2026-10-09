---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Production Integration]]"
stage: 8
status: planned
hours_estimate: 30-48
---

# Overload and Observability

**Problem:** сохранить контролируемое поведение при duplicates, backlog, slow dependencies и retry storms.

## Build

- [ ] Нагрузить TCP boundary `in-memory-database`.
- [ ] Проверить connection limit, idle clients и oversized messages.
- [ ] Выбрать overload policy и измерить throughput, p95/p99, reject rate и memory growth.
- [ ] Реализовать idempotent Kafka consumer и poison-message policy.
- [ ] Построить dashboard RED/USE и Kafka lag.

## Break

- [ ] Dependency latency/loss.
- [ ] Kafka unavailable и consumer медленнее producer.
- [ ] Retries на нескольких слоях.
- [ ] Unbounded queue и рост памяти.
- [ ] Broken или out-of-order event.

## Evidence and Done

- [ ] Retry ограничен budget и выбранным слоем.
- [ ] Overload не создаёт unbounded backlog.
- [ ] Duplicate и poison event наблюдаемы.
- [ ] Измерен recovery time после снятия fault.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#8. Kafka, overload и observability — 30–48 часов|Roadmap]].
