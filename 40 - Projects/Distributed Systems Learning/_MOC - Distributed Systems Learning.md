---
type: project
status: planned
area: distributed-systems
hours_estimate: 442-720
---

# Distributed Systems Learning

## Результат проекта

Научиться проектировать, реализовывать и защищать backend-, storage- и distributed-системы через цикл:

> **Problem → Explain → Predict → Build → Break → Transfer**

Полная программа и проверенные источники: [[40 - Projects/Distributed Systems Learning/00 - Roadmap|Roadmap]].

## Сейчас

- **Статус:** запланирован.
- **Следующий этап:** [[40 - Projects/Distributed Systems Learning/01 - Distributed Systems Core/01 - RPC, MapReduce and Single-Node KV|01 — RPC, MapReduce and Single-Node KV]].
- **Активный implementation track:** выбрать при старте этапа; одновременно только один.
- **Ближайший gate:** Gate A после этапа 2.

## Campaigns

1. [[40 - Projects/Distributed Systems Learning/01 - Distributed Systems Core/_MOC - Distributed Systems Core|Distributed Systems Core]] — этапы 1–7, **214–347 часов**.
2. [[40 - Projects/Distributed Systems Learning/02 - Production Integration/_MOC - Production Integration|Production Integration]] — этапы 8–9, **54–88 часов**.
3. [[40 - Projects/Distributed Systems Learning/03 - Database Internals/_MOC - Database Internals|Database Internals]] — этапы 10–12, **150–245 часов**.
4. [[40 - Projects/Distributed Systems Learning/04 - Capstone/_MOC - Capstone|Capstone]] — этап 13, **24–40 часов**.

## Gates

| Gate | После | Проверка |
|---|---:|---|
| A | 2 | timeout after commit, linearization points, transaction anomalies, KV recovery |
| B | 5 | устойчивые Raft/KV tests, retry/dedup, application + snapshot state |
| C | 9 | system design, benchmark, failure review, production-code invariant |
| D | 12 | DB read/write/recovery path, bad plan, MVCC anomaly, B+tree vs LSM |

Подробные условия: [[40 - Projects/Distributed Systems Learning/00 - Roadmap#Gates|Gates в roadmap]].

## Как работать с проектом

1. Открыть только заметку текущего этапа и выставить `status: active`.
2. До чтения заполнить **Problem**, **Invariant**, assumptions и ответы на контрольные вопросы.
3. Делать один основной implementation track: MIT lab, `in-memory-database`, OpenS3 или BusTub.
4. Сохранять evidence: ссылку на код, команду теста, failure trace и измерения.
5. Закрыть Definition of Done и соответствующий gate.
6. Записать факт в [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]] и выбрать следующий этап.

## Рабочие правила

- Не создавать заметку на каждую лекцию или главу.
- Внутри проекта хранить временный research, ссылки и evidence.
- В долговременные знания переносить только дорогой опыт: найденный failure, диагностический trace, выбранный trade-off и границы решения.
- MIT labs выполнять в официальном репозитории; перенос в `in-memory-database` делать отдельным ограниченным шагом.
- `in-memory-database`, OpenS3, MIT lab и BusTub не вести параллельно как глубокие реализации.

## Журналы и шаблоны

- [[40 - Projects/Distributed Systems Learning/Progress Log|Progress Log]]
- [[40 - Projects/Distributed Systems Learning/90 - Templates/Stage Log Template|Stage Log Template]]
- [[40 - Projects/Distributed Systems Learning/90 - Templates/Failure Experiment Template|Failure Experiment Template]]
