---
type: project-stage
project: "[[_MOC - Distributed Systems Learning]]"
campaign: "[[_MOC - Distributed Systems Core]]"
stage: 4
status: planned
hours_estimate: 55-90
---

# Raft Consensus

**Problem:** согласовать replicated log при crash, delay, reordering и partition.

## Build

- [ ] Пройти MIT Lab 3 Raft A–D.
- [ ] Вести invariant ledger.
- [ ] Для падающих tests строить timeline.
- [ ] Использовать reproducible seed и bounded logging.
- [ ] После прохождения tests объяснить code path без IDE.

## Break

- [ ] Split vote и delayed old RPC.
- [ ] Leader crash после локальной append и после majority replication.
- [ ] Conflicting suffix и term change.
- [ ] Crash/restart с persisted state.
- [ ] Snapshot рядом с concurrent AppendEntries.

## Evidence and Done

- [ ] Election и log tests проходят сериями с race detector.
- [ ] Election Safety и Log Matching привязаны к коду.
- [ ] Persisted state переживает restart.
- [ ] Различаются appended, committed, applied и responded.
- [ ] Результат записан в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]].

Полная теория и вопросы: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#4. Consensus и MIT Lab 3 Raft — 55–90 часов|Roadmap]].
