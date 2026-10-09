---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Database Internals]]"
stage: 11
status: planned
hours_estimate: 55-90
---

# Query Execution and Optimization

**Problem:** связать logical plan, physical operators, statistics и cost-based choice.

## Build

- [ ] Пройти CMU Query Execution project.
- [ ] Сравнить два join algorithms на одном benchmark.
- [ ] Сделать toy optimizer для 3–5 relations или официальные exercises.
- [ ] Сравнить estimated/actual rows на skewed/correlated data.
- [ ] Исследовать `EXPLAIN (ANALYZE, BUFFERS)` в PostgreSQL.

## Break

- [ ] Missing/stale statistics и correlated predicates.
- [ ] Memory limit вызывает spill.
- [ ] Bad join order и skewed hash partition.
- [ ] Cold vs warm cache.

## Evidence and Done

- [ ] Logical и physical plan не смешиваются.
- [ ] Operators имеют contract и tests.
- [ ] Benchmark фиксирует dataset, cache state и memory budget.
- [ ] Misestimation связана с bad plan и двумя вариантами исправления.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#11. Query execution и optimization — 55–90 часов|Roadmap]].
