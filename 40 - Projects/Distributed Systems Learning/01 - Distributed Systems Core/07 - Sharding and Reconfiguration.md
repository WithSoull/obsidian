---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 7
status: planned
hours_estimate: 35-60
---

# Sharding and Reconfiguration

**Problem:** увеличить throughput без потери ownership, data и ordering во время shard transfer.

## Build

- [ ] Пройти MIT Lab 5 Sharded KV.
- [ ] Описать lifecycle shard transfer.
- [ ] Построить benchmark `1 → 2 → 4` shard groups.
- [ ] Измерить throughput, p95/p99 и rebalancing cost.

## Break

- [ ] Request со старой configuration.
- [ ] Duplicate ownership и unavailable gap.
- [ ] Crash во время transfer.
- [ ] Hot key ломает масштабирование.
- [ ] Retry старой команды после cutover.

## Evidence and Done

- [ ] В каждый момент определён authoritative owner.
- [ ] Переносятся data и dedup/session state.
- [ ] Stale configuration распознаётся.
- [ ] Benchmark показывает bottleneck и rebalancing cost.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#7. Sharding и reconfiguration — 35–60 часов|Roadmap]].
