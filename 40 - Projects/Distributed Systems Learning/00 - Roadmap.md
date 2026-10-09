# Distributed Systems Learning Plan

> Рабочий проект: [[40 - Projects/Distributed Systems Learning/_MOC - Distributed Systems Learning|Distributed Systems Learning]]. Здесь хранится полная спецификация; фактическая работа и evidence фиксируются в заметках этапов.

## Зачем нужен этот план

Цель — научиться проектировать и реализовывать надёжные backend- и storage-системы, а не «закрыть» DDIA, MIT, CMU и несколько видеокурсов.

Основная единица прогресса:

> **Problem → Explain → Predict → Build → Break → Transfer**

- **Problem:** сформулировать инженерную проблему и инвариант.
- **Explain:** объяснить механизм без конспекта.
- **Predict:** предсказать поведение в незнакомом failure scenario.
- **Build:** реализовать механизм и пройти adversarial tests.
- **Break:** воспроизвести отказы, гонки, перегрузку и восстановление.
- **Transfer:** применить тот же принцип в `in-memory-database`, OpenS3 либо production-коде.

Прочитанная глава, просмотренная лекция и созданная заметка сами по себе не являются результатом. Для ключевых тем **DONE = Build + Transfer**.

## Короткая карта

```text
Distributed Systems campaign
  RPC → local correctness → replication → Raft → replicated KV
      → distributed transactions → sharding → reliability
                              ↓
Интеграция
  system design drills → чтение production-кода
                              ↓
Второй campaign: Database Internals
  pages → buffer pool → indexes → execution → optimizer
      → MVCC → WAL/recovery → LSM
                              ↓
Capstone / небольшой OSS-вклад
```

Полный объём: **442–720 часов**. Это часы чтения, реализации, отладки, тестов, экспериментов и защиты результата. Календарь намеренно не фиксируется: фактическую скорость нужно пересчитывать после каждого gate.

## Роли материалов

| Материал | Роль | Правило использования |
|---|---|---|
| [DDIA 2e][ddia] | карта trade-offs и терминологии | читать фрагменты по текущей проблеме, не конспектировать подряд |
| MIT 6.5840 | основной практический backbone DS | [видео Spring 2020][mit-videos-2020] для объяснения; [syllabus, papers и labs Spring 2026][mit-schedule] для прохождения; не смешивать skeleton/tests разных лет |
| [Cambridge Concurrent and Distributed Systems][cambridge-current] | компактная формальная модель | использовать до или после сложной темы; публичные записи есть у [версии 2021–22][cambridge-materials] |
| Курс Влада Тена | русскоязычная инженерная карта | дополнительное объяснение; спорные детали проверять по DDIA, paper и официальным docs |
| [Курс Олега Козырева][kozyrev] | сборка знаний для system design interview | проходить после DS core, а не вместо него |
| [CMU 15-445 Spring 2026][cmu-schedule] | основной backbone DB internals | второй большой campaign; проекты идут последовательно |
| [OSTEP][ostep] | just-in-time OS gaps | брать concurrency/persistence главы по конкретной дыре; полный курс сейчас не нужен |
| [`in-memory-database`][in-memory-db] | основной личный KV-полигон | развивать существующие слои `storage/engine` вместо написания второго одноузлового KV с нуля |
| OpenS3 | один из возможных полигонов для production transfer | проверять ограниченный инвариант, а не превращать проект в учебную распределённую БД |

У Влада не найдена стабильная официальная публичная программа. Доступное публичное описание совпадает с порядком `storage → transactions/recovery → replication → consensus → sharding`, но оно используется только как ориентир, не как авторитетный источник.

## Как использовать `in-memory-database`

В текущем `main` уже есть TCP-сервер и текстовый протокол `SET/GET/DEL`, раздельные слои parser → storage → engine, in-memory `map` под `RWMutex`, лимит соединений, ограничение размера сообщения, idle timeout и тесты с race detector. Поэтому второй одноузловой KV с нуля в плане не нужен.

| Этап | Развитие проекта |
|---:|---|
| 1 | зафиксировать semantics и linearization points текущих операций; добавить versioned conditional write и concurrent tests |
| 2 | добавить durable append-only engine за существующим интерфейсом `Engine`, recovery и compaction |
| 3 | в отдельной учебной ветке/модуле проверить leader/follower replication, quorum ack, epoch и bootstrap из snapshot + log tail |
| 5 | сопоставить интерфейс engine с replicated state machine из MIT Lab 4; не переносить решение lab в основной проект |
| 8 | использовать TCP boundary для overload-экспериментов: connection limit, idle clients, oversized messages, queueing и p99 |
| 12–13 | довести recovery/LSM-эксперимент или выбрать проект основой итогового capstone |

MIT labs остаются отдельным репозиторием с официальными skeleton и tests. Рабочий ритм для пересекающихся тем: сначала закрыть lab, затем сделать один ограниченный transfer в `in-memory-database`, а не поддерживать две параллельные реализации одного механизма.

## Как использовать MIT 6.5840

Публичные видеозаписи Spring 2026 на официальной странице курса не опубликованы: ссылки `LEC` ведут на lecture notes/slides, papers и вопросы. Поэтому MIT-трек собирается из двух выпусков:

> **видео Spring 2020 для объяснения + syllabus, papers, skeleton и tests Spring 2026 для практики**

- смотреть [публичный YouTube-плейлист Spring 2020][mit-videos-2020];
- идти в порядке [расписания Spring 2026][mit-schedule];
- перед каждой темой читать назначенный в 2026 paper и вопрос;
- labs выполнять только из checkout `6.5840-golabs-2026` и по условиям 2026;
- не пытаться искать видео с тем же номером лекции: номера и часть тем между выпусками отличаются.

### Соответствие основных лекций

| Spring 2026 | Видео Spring 2020 |
|---|---|
| Introduction | Lecture 1 |
| RPC and Threads | Lecture 2 |
| GFS | Lecture 3 |
| Raft 1–2 | Lectures 6–7 |
| ZooKeeper | Lecture 8 |
| Distributed Transactions | Lecture 12 |
| Spanner | Lecture 13 |
| Optimistic Concurrency Control | Lecture 14 |
| Memcached at Facebook | Lecture 16 |
| SUNDR / Fork Consistency | Lecture 18 |
| Bitcoin | Lecture 19 |

Для Paxos, отдельной лекции по Linearizability, Chain Replication, Verification, AWS Lambda, Ray и Byzantine Fault Tolerance точного соответствия в плейлисте 2020 нет. Для них использовать lecture notes и paper из расписания 2026; при необходимости — соответствующую лекцию Cambridge как дополнительное объяснение.

## Правила прохождения

1. Одновременно активен **один основной implementation track**. `in-memory-database`, OpenS3, MIT lab и BusTub не должны конкурировать за глубокие сессии.
2. Перед чтением письменно ответить на контрольные вопросы этапа. После этапа ответить снова без источников.
3. Для каждой операции назвать:
   - safety-инвариант;
   - liveness-ожидание;
   - commit или linearization point;
   - поведение при timeout и retry;
   - метрики и способ восстановления.
4. Каждый build завершается happy-path, boundary, concurrent, randomized и failure-тестами, где они применимы.
5. Для active recall использовать короткий спарринг по одному вопросу за раз. Ошибки фиксировать, но не превращать vault в энциклопедию.
6. В Second Brain сохранять только опыт, который дорого восстановить: необычный failure, trace диагностики, отвергнутые варианты и итоговый trade-off. Обычно достаточно 5–10 минут.
7. Если lab застрял, сначала уменьшить сценарий, включить deterministic seed и получить trace. Чтение чужого решения не засчитывает Build.

## Карта этапов и часы

| № | Этап | Теория | Практика | Всего |
|---:|---|---:|---:|---:|
| 1 | RPC, MapReduce и single-node KV | 7–10 | 21–34 | 28–44 |
| 2 | Local storage, crash consistency и транзакции | 10–15 | 22–33 | 32–48 |
| 3 | Репликация, lag и quorum | 5–8 | 11–18 | 16–26 |
| 4 | Consensus и MIT Lab 3 Raft | 14–22 | 41–68 | 55–90 |
| 5 | Replicated KV и state machine | 7–11 | 21–34 | 28–45 |
| 6 | Distributed transactions | 7–11 | 13–23 | 20–34 |
| 7 | Sharding и reconfiguration | 9–14 | 26–46 | 35–60 |
| 8 | Kafka, overload и observability | 9–14 | 21–34 | 30–48 |
| 9 | System design и production-code reading | 7–12 | 17–28 | 24–40 |
| 10 | DB storage: pages, buffer pool, indexes | 14–22 | 36–58 | 50–80 |
| 11 | Query execution и optimization | 15–24 | 40–66 | 55–90 |
| 12 | MVCC, WAL, recovery и LSM | 13–21 | 32–54 | 45–75 |
| 13 | Capstone и OSS transfer | 4–7 | 20–33 | 24–40 |
|  | **Итого** | **121–191** | **321–529** | **442–720** |

# Campaign 1. Distributed Systems core

## 1. RPC, MapReduce и single-node KV — 28–44 часа

**Проблема:** несколько процессов общаются по ненадёжной сети; даже без replication результат операции может быть неизвестен.

### Теория

- Cambridge: RPC, network/crash faults, synchrony models, Two Generals;
- MIT Spring 2020 videos: Lectures 1–3; затем notes и papers соответствующих лекций Spring 2026;
- MapReduce paper;
- linearizability, at-most-once и application-level idempotency.

### Build

- пройти [MIT Lab 1 MapReduce][mit-lab1];
- пройти [MIT Lab 2 Key/Value Server][mit-lab2], включая lock;
- нарисовать state machine coordinator и назвать ownership общих данных;
- записать linearization point `Get`, `Put` и lock acquisition;
- в [`in-memory-database`][in-memory-db] описать текущие semantics `SET/GET/DEL` и их linearization points;
- добавить versioned conditional write (`CAS` или `SET ... IF_VERSION`) и детерминированные concurrent tests.

### Break

- worker crash и worker stall;
- duplicate task после timeout;
- потеря request и потеря response;
- concurrent PUT одного key;
- client crash с удерживаемым lock.

### Definition of Done

- официальные тесты проходят с race detector;
- повторный task не публикует частичный результат;
- объяснена разница `ErrVersion` и `ErrMaybe` из Lab 2;
- для lock названа проблема lease/fencing, которую lab намеренно не решает;
- race detector проходит и для новых тестов `in-memory-database`;
- неизвестная история операций разбирается на linearizable/non-linearizable.

### Контрольные вопросы

1. Почему coordinator не может отличить умершего worker от очень медленного?
2. Чем повтор RPC отличается от новой бизнес-команды?
3. Почему conditional write даёт at-most-once effect, но не всегда сообщает клиенту точный исход?

## 2. Local storage, crash consistency и транзакции — 32–48 часов

**Проблема:** до replication нужно понять, когда локальная запись стала durable и какие concurrent histories допустимы.

### Теория

- DDIA 2e: главы 4 и 8;
- OSTEP: persistence, files/directories, crash consistency и journaling — выборочно;
- page cache, `fsync`, atomic rename, checksum, record framing;
- Read Committed, Snapshot Isolation, Serializable, 2PL, OCC, MVCC;
- lost update, read/write skew, phantom, deadlock.

### Build

- добавить в [`in-memory-database`][in-memory-db] durable append-only engine за существующим интерфейсом `Engine`: framing, checksum, recovery scan и compaction;
- в PostgreSQL детерминированно воспроизвести lost update, write skew, phantom и deadlock;
- один инвариант защитить через `FOR UPDATE`, optimistic version и `SERIALIZABLE` + retry;
- сравнить корректность, contention и сложность трёх вариантов.

### Break

- kill процесса между append, sync и ack;
- truncate последней записи и bit flip;
- crash во время compaction/swap;
- serialization failure при внешнем side effect;
- две транзакции одновременно обновляют current version объекта.

### Definition of Done

- recovery не принимает повреждённую запись за корректную;
- durability promise отделён от process-crash behavior;
- каждая аномалия имеет воспроизводимый trace;
- retry повторяет всю транзакцию, но не дублирует внешний effect;
- можешь объяснить, почему Snapshot Isolation допускает write skew.

### Контрольные вопросы

1. Когда atomic rename недостаточен для durability?
2. Где commit point append-only записи?
3. Какой конкретный invariant нарушает write skew?

## 3. Репликация, lag и quorum — 16–26 часов

**Проблема:** определить, что означает acknowledged write и допустимое чтение при отстающих или изолированных replicas.

### Теория

- DDIA 2e, глава 6;
- Cambridge: replication, quorums, state machine replication;
- synchronous/asynchronous replication, leader/follower и leaderless;
- quorum intersection, read-your-writes, monotonic reads;
- split brain, epoch/fencing, failover, RPO и RTO.

### Build

- в отдельной учебной ветке или модуле расширить [`in-memory-database`][in-memory-db] одним leader и двумя followers;
- поддержать write modes `leader-only` и `quorum`;
- поддержать reads `leader`, `any replica`, `minimum sequence`;
- реализовать bootstrap follower из snapshot + log tail.

### Break

- медленный follower;
- потеря leader до и после quorum ack;
- изоляция старого leader;
- stale read после failover;
- follower восстанавливается с повреждённым tail.

### Definition of Done

- ack policy однозначно связана с возможной потерей данных;
- старый leader не подтверждает записи после смены epoch;
- lag измеряется временем и log distance;
- объяснено, почему `R + W > N` само по себе не делает произвольную систему linearizable;
- transfer в OpenS3 ограничен design note, без обязательной реализации replication.

### Контрольные вопросы

1. Какие acknowledged writes можно потерять при async replication?
2. Почему majority помогает safety, но не гарантирует availability?
3. Чем fencing token отличается от обычного distributed lock?

## 4. Consensus и MIT Lab 3 Raft — 55–90 часов

**Проблема:** несколько узлов должны согласовать единый replicated log при crash, delay, reordering и partition.

### Теория

- [Raft extended paper][raft-paper];
- MIT Spring 2020 videos: Lectures 6–7 про Raft; Paxos и отдельную Linearizability проходить по notes/papers Spring 2026;
- DDIA 2e, главы 9 и 10;
- term, leader completeness, log matching, commit rule;
- safety vs liveness, majority, partial synchrony;
- snapshotting и persisted state.

### Build

- пройти [MIT Lab 3 Raft][mit-lab3] по частям A–D;
- вести отдельный invariant ledger;
- сделать timeline для каждого падающего теста;
- использовать reproducible random seed и bounded logging;
- после прохождения тестов объяснить код без IDE.

### Break

- simultaneous elections;
- reordered `AppendEntries`;
- old leader возвращается после partition;
- crash после persist, но до response;
- snapshot пересекается с replication;
- minority сохраняет более длинный, но не committed log.

### Definition of Done

- все официальные тесты проходят сериями, включая race detector;
- есть объяснение, почему запись предыдущего term нельзя commit только по текущему replication count;
- persisted и volatile state разделены корректно;
- goroutines/timers не растут после повторных elections;
- новая failure history разбирается через election safety, log matching и leader completeness.

### Контрольные вопросы

1. Почему Raft требует majority, а не просто «самый длинный log»?
2. Когда команда committed, applied и отвечена клиенту — три разных момента?
3. Почему timeout влияет на liveness, но не должен определять safety?

## 5. Replicated KV и state machine — 28–45 часов

**Проблема:** consensus log ещё не является готовым сервисом; нужно связать request, log entry, apply и client response.

### Теория

- MIT Spring 2020 video: Lecture 8 про ZooKeeper; Linearizability — по notes/paper Spring 2026;
- state machine replication;
- duplicate suppression, client sessions и sequence numbers;
- read semantics, stale leader и leadership change;
- snapshot/apply boundary.

### Build

- пройти [MIT Lab 4 Fault-tolerant KV][mit-lab4];
- зафиксировать mapping `client request → log index/term → applied result`;
- bounded dedup state и snapshot должны восстанавливаться вместе;
- добавить history-based или model-based randomized test;
- сопоставить state-machine contract Lab 4 с интерфейсом `Engine` в `in-memory-database` в коротком design note, не копируя lab implementation в проект.

### Break

- response lost after apply;
- leader changes while client waits;
- duplicate command arrives through a new leader;
- crash between snapshot creation and installation;
- partitioned leader принимает запрос, но не может commit.

### Definition of Done

- один logical request не применяется дважды;
- сервер не отвечает success до выбранного commit/linearization point;
- waiter не получает результат другой команды после index reuse;
- snapshot сохраняет application state и dedup metadata согласованно;
- можешь показать место каждого инварианта в коде.

### Контрольные вопросы

1. Почему совпадение log index недостаточно для ответа клиенту?
2. Какие данные deduplication обязаны попасть в snapshot?
3. Можно ли обслужить linearizable read без добавления записи в log?

## 6. Distributed transactions — 20–34 часа

**Проблема:** одна бизнес-операция меняет несколько independently failing ресурсов.

### Теория

- DDIA 2e, глава 8: distributed transactions и 2PC;
- MIT Spring 2020 videos: Lectures 12–14; papers и вопросы — из Spring 2026;
- atomic commit vs consensus;
- prepare/commit, coordinator recovery и in-doubt state;
- transactional outbox, inbox/dedup и saga compensation;
- exactly-once processing как end-to-end property.

### Build

- реализовать mini-2PC coordinator с durable decision log;
- реализовать outbox publisher и idempotent consumer на PostgreSQL;
- описать OpenS3 write workflow как state machine `pending → committed/aborted`;
- сравнить 2PC, outbox и compensation для metadata/blob/event boundaries.

### Break

- participant crash after prepare;
- coordinator crash before/after durable decision;
- commit response lost;
- outbox publish duplicate;
- consumer side effect committed, offset not advanced.

### Definition of Done

- in-doubt transaction не выдаётся за aborted;
- coordinator после restart воспроизводит то же решение;
- consumer restart не дублирует логический effect;
- явно указано, где atomicity невозможна и нужна reconciliation;
- выбранный OpenS3 workflow защищает named invariant, а не абстрактную «консистентность».

### Контрольные вопросы

1. Почему 2PC может блокироваться после prepare?
2. Чем durable decision отличается от сообщения `commit`?
3. Когда outbox решает atomicity, но не ordering между aggregates?

## 7. Sharding и reconfiguration — 35–60 часов

**Проблема:** увеличить throughput, не потеряв ключи и порядок операций во время переноса ownership.

### Теория

- DDIA 2e, глава 7;
- MIT: Lab 5 and reconfiguration model;
- range/hash/directory partitioning;
- hot keys, skew и secondary indexes;
- shard epoch/config version;
- cutover, handoff, duplicate ownership и unavailable gap.

### Build

- пройти [MIT Lab 5 Sharded KV][mit-lab5];
- отдельно описать lifecycle shard transfer;
- построить benchmark `1 → 2 → 4 shard groups`;
- измерить throughput, p95/p99 и rebalancing cost;
- для OpenS3 делать только prototype/design experiment, если sharding не нужен самому проекту.

### Break

- request приходит по старой конфигурации;
- donor и receiver считают shard своим;
- оба считают shard чужим;
- crash во время transfer;
- hot key ломает ожидаемое масштабирование;
- retry старой команды после cutover.

### Definition of Done

- в каждый момент определён authoritative owner;
- перенос сохраняет data и dedup/session state;
- stale configuration распознаётся, а не молча обслуживается;
- benchmark показывает bottleneck, а не только «RPS вырос»;
- объяснено, почему больше shards может ухудшить latency и операции.

### Контрольные вопросы

1. Как fencing предотвращает writes старого owner?
2. Когда consistent hashing не решает hot-key problem?
3. Какие данные кроме values нужно переносить вместе с shard?

# Campaign 2. Production integration

## 8. Kafka, overload и observability — 30–48 часов

**Проблема:** система должна сохранять контролируемое поведение при duplicates, backlog, slow dependencies и retry storms.

### Теория

- DDIA 2e, главы 2, 12 и 13;
- [Apache Kafka documentation][kafka-docs]: records, topics, partitions, producers и consumers;
- delivery/processing semantics, consumer groups, offset lifecycle;
- backpressure, admission control, bounded queues;
- [AWS guidance on bounded retries][aws-retries];
- RED/USE signals, logs, traces, p50/p95/p99 и recovery time.

### Build

- нагрузить TCP boundary [`in-memory-database`][in-memory-db]: `SET/GET`, исчерпание connection limit, idle clients и oversized messages;
- определить для него overload policy и измерить throughput, p95/p99, reject rate и memory growth;
- довести OpenS3 access-event pipeline до воспроизводимого сценария;
- сделать idempotent consumer и явную poison-message policy;
- нагрузить OpenS3 PUT/GET и consumer независимо;
- построить dashboard: rate, errors, latency, saturation, Kafka lag;
- записать overload policy: reject, queue, degrade или shed load.

### Break

- 200 ms latency и 1/10% loss на dependency;
- Kafka unavailable;
- consumer в 10 раз медленнее producer;
- retry на нескольких слоях;
- unbounded queue и slow memory growth;
- broken/out-of-order event.

### Definition of Done

- retries ограничены budget и выполняются на выбранном слое;
- overload не превращается в неограниченный backlog;
- duplicate и poison event имеют наблюдаемую судьбу;
- метрики позволяют отличить latency dependency от queueing внутри сервиса;
- после снятия fault измерен recovery time.

### Контрольные вопросы

1. Почему retry улучшает availability при редких transient faults, но усугубляет overload?
2. Что означает lag без знания producer rate и processing time?
3. Где exactly-once Kafka заканчивается и начинается end-to-end idempotency приложения?

## 9. System design и production-code reading — 24–40 часов

**Проблема:** собрать изученные primitives в решение и быстро находить их реализацию в чужом коде.

### Теория

- курс Козырева: requirements, capacity estimate, architecture, bottlenecks, deep dive;
- выбранные кейсы Влада — как русскоязычный bridge;
- MIT papers как examples of trade-offs;
- repository archaeology: entrypoints, data model, write/read/recovery path.

### Build

- решить минимум четыре design case: object storage, messenger, ticket booking и feed/search;
- на каждый дать 45-минутную защиту и отдельную failure matrix;
- в etcd/CockroachDB/RustFS найти один знакомый invariant и проследить его через code path;
- сделать один небольшой code-reading report: hypothesis → evidence → unresolved questions.

### Break

- primary cache/database недоступен;
- duplicate message после consumer crash;
- последнее место покупают два клиента;
- shard move без downtime;
- region partition и stale client;
- traffic x10 при деградации dependency.

### Definition of Done

- требования отделены от выбранной архитектуры;
- оценки capacity имеют единицы и порядок величины;
- каждый компонент оправдан invariant/load/failure requirement;
- можешь углубиться в write path без перечисления buzzwords;
- в чужом репозитории утверждения подтверждены строками кода или тестами.

### Контрольные вопросы

1. Какое требование действительно заставляет вводить Kafka или sharding?
2. Как проверить, что cache не стал новым source of truth?
3. Как отличить реализованную гарантию от комментария или target design?

# Campaign 3. Database Internals

CMU 15-445 — отдельный campaign после DS core. Проекты Spring 2026 идут последовательно: C++ Primer → Buffer Pool Manager → Database Index → Query Execution → Concurrency Control. Recovery в этом выпуске проверяется homework/лекциями, а не отдельным coding project; поэтому ниже добавлен собственный bounded recovery experiment.

## 10. Pages, buffer pool и indexes — 50–80 часов

**Проблема:** связать disk layout, page lifetime, cache policy и index invariants.

### Теория

- CMU lectures/homework: storage, memory management, hash tables, indexes;
- DDIA 2e, глава 4;
- page/header/slot layout, RID и free-space management;
- pin/unpin, dirty page, eviction и writeback;
- extendible hash и B+tree invariants;
- latch vs transaction lock.

### Build

- пройти C++ Primer при необходимости;
- пройти CMU Buffer Pool Manager project;
- пройти CMU Database Index project;
- добавить invariant checker и randomized oracle для структуры;
- измерить hit ratio и write amplification на разных workloads.

### Break

- все frames pinned;
- dirty victim и I/O error;
- concurrent split/merge;
- duplicate key и boundary key;
- corrupted page/header;
- crash между page modification и flush.

### Definition of Done

- lifecycle page объясняется от fetch до eviction;
- pin leak и lost dirty page ловятся тестами;
- index сохраняет ordering/reachability invariants после randomized operations;
- latch coupling объяснён по конкретному code path;
- disk I/O и logical operation не смешиваются в метриках.

### Контрольные вопросы

1. Почему buffer-pool latch не заменяет transaction lock?
2. Что случится, если evict dirty page без корректного writeback?
3. Какие invariants должен проверить B+tree checker после split?

## 11. Query execution и optimization — 55–90 часов

**Проблема:** понять путь SQL-запроса от logical plan до физических операторов и cost-based choice.

### Теория

- CMU: sorting, joins, execution, planning и optimization;
- iterator/vectorized execution;
- hash join, sort-merge join, nested loop;
- cardinality estimation, selectivity и statistics;
- access path, join order и cost model;
- pipeline breakers, spill и memory budget.

### Build

- пройти CMU Query Execution project;
- реализовать два join algorithms в маленьком benchmark;
- сделать toy optimizer для 3–5 relations или закончить официальные exercises;
- сравнить estimate vs actual rows на skewed/correlated data;
- исследовать `EXPLAIN (ANALYZE, BUFFERS)` в PostgreSQL.

### Break

- missing/stale statistics;
- correlated predicates;
- memory limit вызывает spill;
- bad join order;
- skewed hash partition;
- same query с cold и warm cache.

### Definition of Done

- logical и physical plan не смешиваются;
- каждый operator имеет contract и test;
- benchmark фиксирует dataset, cache state и memory budget;
- misestimation связывается с конкретным bad plan;
- можешь предложить минимум два исправления и их цену.

### Контрольные вопросы

1. Почему хороший cardinality estimate важнее «умного» join algorithm?
2. Как pipeline breaker влияет на latency до первой строки?
3. Почему warm-cache benchmark не описывает disk-bound workload?

## 12. MVCC, WAL, recovery и LSM — 45–75 часов

**Проблема:** сохранить transactional correctness при concurrency и восстановить состояние после crash.

### Теория

- CMU: concurrency-control lectures/project, logging и recovery homework;
- DDIA 2e, главы 4 и 8;
- 2PL, timestamp ordering, MVCC, visibility и vacuum;
- WAL rule, LSN, checkpoint, redo и undo;
- physiological logging и idempotent recovery;
- memtable, SSTable, Bloom filter и compaction;
- leveled vs size-tiered trade-offs.

### Build

- пройти CMU Concurrency Control project;
- завершить official Recovery homework;
- развить durable engine [`in-memory-database`][in-memory-db] из этапа 2: добавить WAL/checkpoint recovery experiment;
- построить маленький LSM prototype или использовать симулятор compaction;
- измерить read/write/space amplification.

### Break

- crash до и после WAL flush;
- checkpoint пересекается с active transaction;
- abort после частичного update;
- long-running snapshot удерживает garbage;
- compaction crash;
- tombstone resurrection после неверного merge.

### Definition of Done

- WAL-before-data rule показано тестом, а не только объяснено;
- recovery повторный запуск идемпотентен;
- MVCC visibility проверяется для нескольких concurrent snapshots;
- bounded redo/undo experiment закрывает отсутствие отдельного recovery coding project в CMU 2026;
- LSM benchmark объясняет минимум два вида amplification.

### Контрольные вопросы

1. Почему checkpoint не обязательно означает отсутствие redo?
2. Что удерживает старую версию живой в MVCC?
3. Как compaction может воскресить удалённое значение?

# Campaign 4. Итоговая интеграция

## 13. Capstone и OSS transfer — 24–40 часов

**Проблема:** доказать перенос знаний на реальный bounded subsystem.

### Теория

- перечитать только те разделы DDIA/papers, которые нужны для выбранных инвариантов;
- проверить API и failure semantics используемых gRPC, PostgreSQL и Kafka компонентов по официальной документации;
- изучить один сходный production design и подтвердить ключевые утверждения кодом или тестами;
- заранее определить scope, нагрузочную модель и границы того, что capstone не доказывает.

### Выбор кейса

Выбрать **один**, исходя из того, какой проект хочется довести до законченного инженерного результата.

#### Вариант A — `in-memory-database`

Собрать надёжный KV-путь поверх уже существующего TCP API:

```text
client request
  → parse/validate
  → version/dedup check
  → durable append / WAL
  → apply to engine
  → optional replication ack
  → response
```

Минимальная цель — не «production-ready Redis», а доказанные crash/retry semantics, восстановление, bounded dedup state, нагрузочные метрики и честно описанные ограничения.

#### Вариант B — OpenS3

Надёжный object write + access event:

```text
client PUT
  → Gateway
  → blob write
  → metadata transition
  → outbox/access event
  → Kafka
  → idempotent consumer
  → access history / recommendation input
```

### Build

- написать design doc с контрактом, state machine и failure matrix;
- реализовать самый узкий E2E path;
- добавить fault injection и replay/reconciliation command;
- провести нагрузочный эксперимент;
- найти один сходный механизм в production OSS;
- по возможности сделать небольшой test, issue или patch, не пытаясь переписать subsystem.

### Break

- timeout после каждого commit/side-effect boundary;
- duplicate и out-of-order delivery;
- process crash на каждой границе состояния;
- зависимость медленная/недоступна;
- backlog после восстановления;
- concurrent writes одного key/object key.

### Definition of Done

- есть исполняемый E2E test и автоматизированные failure cases;
- named invariants сохраняются или нарушение обнаруживается и ремонтируется;
- результаты нагрузки воспроизводимы;
- design doc честно разделяет implemented runtime, target design и ограничения;
- можешь защитить два отвергнутых решения и назвать условия, при которых выбрал бы их.

### Контрольные вопросы

1. Какой один failure оставляет состояние частично применённым или результат операции неизвестным, и как система это обнаруживает?
2. Где достигается atomicity, а где используется reconciliation?
3. Какая гарантия подтверждена тестом, а какая пока существует только в design?

# Gates

## Gate A — после этапа 2

Без конспекта:

- разобрать timeout после commit;
- назвать linearization point трёх операций;
- воспроизвести две transaction anomalies;
- восстановить KV после kill/corruption.

Если Predict слабее Explain, не переходить к replication: добавить failure scenarios, а не ещё одну книгу.

## Gate B — после этапа 5

- Raft и KV tests стабильно проходят сериями;
- неизвестная election/log history разбирается без запуска кода;
- client retry не дублирует effect после leader change;
- snapshot восстанавливает application и dedup state.

Если test проходит только «иногда», этап не закрыт.

## Gate C — после этапа 9

- спроектировать object storage за 45 минут;
- назвать bottleneck и проверить его benchmark-ом;
- провести failure review своего решения;
- проследить один invariant в production repository.

## Gate D — после этапа 12

- объяснить read/write/recovery path учебной DB;
- найти причину bad query plan по `EXPLAIN ANALYZE`;
- воспроизвести MVCC anomaly и recovery boundary;
- защитить B+tree vs LSM для двух разных workloads.

# Недельный ритм без жёсткого календаря

Использовать rolling capacity, а не обещание «каждый день по два часа»:

- **минимум:** 6–8 часов в неделю — одна theory + две build/debug сессии;
- **рабочий режим:** 10–12 часов — две theory/review + три build/debug сессии;
- **интенсив:** 14–16 часов — только когда остальные обязательства и сон это реально позволяют.

Распределение внутри этапа:

- 20–30% — чтение/лекции/papers;
- 55–65% — реализация и debugging;
- 10–20% — failure experiments, защита и короткий отчёт.

После каждого этапа записывать `плановые часы / фактические часы / главный источник перерасхода` и пересчитывать следующие диапазоны.

# Что сознательно не входит в критический путь

- полный MIT 6.S081 до начала DS;
- полный nand2tetris;
- математика без конкретной потребности;
- security как отдельный большой campaign;
- CMU 15-721 до завершения 15-445 core;
- одновременное прохождение MIT и CMU;
- production-grade replication/sharding в OpenS3 только ради закрытия учебного этапа;
- заметка на каждую главу или лекцию;
- чтение всего etcd/CockroachDB/RustFS repository.

Алгоритмы для интервью — отдельный параллельный maintenance track с ограниченным бюджетом. Они не должны вытеснять основной implementation stage.

# Журнал этапа

Для каждого этапа достаточно одного файла в учебном репозитории:

```markdown
# <Тема>

## Problem and invariant

## Model and assumptions

## Commit / linearization point

## Implementation

## Failure matrix

| Fault | Injection point | Expected | Observed | Recovery |
|---|---|---|---|---|

## Measurements

## Rejected alternatives

## Explain / Predict / Build / Transfer

## Hours: planned / actual
```

# Источники и статус проверки

Проверено 2026-09-15. Для меняющихся курсов при старте campaign нужно ещё раз проверить актуальный выпуск и не смешивать assignments разных cohorts.

- [DDIA 2nd Edition, официальная страница O’Reilly][ddia] — опубликована в феврале 2026; оглавление подтверждает главы 4–13, использованные в плане.
- [MIT 6.824 Spring 2020 video playlist][mit-videos-2020] — публичные записи для основной теории; [MIT 6.5840 Spring 2026: home][mit-home] и [schedule][mit-schedule] — актуальные syllabus, papers и labs. Публичные записи Spring 2026 на странице курса не размещены.
- Официальные условия labs: [Lab 1][mit-lab1], [Lab 2][mit-lab2], [Lab 3][mit-lab3], [Lab 4][mit-lab4], [Lab 5][mit-lab5].
- [Cambridge course 2026–27][cambridge-current] — подтверждает темы RPC/fault models, time, replication, consensus, transactions и DDIA 2e в recommended reading; [официальные материалы 2021–22][cambridge-materials] содержат публичные записи восьми DS lectures.
- [CMU 15-445 Spring 2026 assignments][cmu-assignments], [schedule][cmu-schedule] и [syllabus][cmu-syllabus] — подтверждены четыре последовательных coding projects после primer и отдельное Recovery homework.
- [OSTEP][ostep] — официальный бесплатный источник по virtualization, concurrency и persistence.
- [Raft paper][raft-paper] — extended paper Ongaro/Ousterhout.
- [gRPC deadlines][grpc-deadlines] и [cancellation][grpc-cancellation] — официальная документация; cancellation не откатывает уже выполненные изменения.
- [Apache Kafka documentation][kafka-docs] — официальная документация по topics, partitions, producers и consumers.
- [AWS retry guidance][aws-retries] — retries должны быть bounded, с backoff/jitter и только для корректно обрабатываемых повторов.
- [System Design: от паники к алгоритму][kozyrev] — официальная страница подтверждает interview-oriented порядок от requirements к bottlenecks и кейсам.
- [`WithSoull/in-memory-database`][in-memory-db] — проверены текущие README и код: TCP `SET/GET/DEL`, слои storage/engine, `RWMutex`, сетевые лимиты и тестовый контур.

[ddia]: https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/
[mit-home]: https://pdos.csail.mit.edu/6.824/
[mit-schedule]: https://pdos.csail.mit.edu/6.824/schedule.html
[mit-videos-2020]: https://www.youtube.com/playlist?list=PLrw6a1wE39_tb2fErI4-WkMbsvGQk9_UB
[mit-lab1]: https://pdos.csail.mit.edu/6.824/labs/lab-mr.html
[mit-lab2]: https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html
[mit-lab3]: https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html
[mit-lab4]: https://pdos.csail.mit.edu/6.824/labs/lab-kvraft1.html
[mit-lab5]: https://pdos.csail.mit.edu/6.824/labs/lab-shard1.html
[cambridge-current]: https://www.cl.cam.ac.uk/teaching/2627/ConcDisSys/
[cambridge-materials]: https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/materials.html
[cmu-assignments]: https://15445.courses.cs.cmu.edu/spring2026/assignments.html
[cmu-schedule]: https://15445.courses.cs.cmu.edu/spring2026/schedule.html
[cmu-syllabus]: https://15445.courses.cs.cmu.edu/spring2026/syllabus.html
[ostep]: https://pages.cs.wisc.edu/~remzi/OSTEP/
[raft-paper]: https://raft.github.io/raft.pdf
[grpc-deadlines]: https://grpc.io/docs/guides/deadlines/
[grpc-cancellation]: https://grpc.io/docs/guides/cancellation/
[kafka-docs]: https://kafka.apache.org/documentation.html
[aws-retries]: https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_limit_retries.html
[kozyrev]: https://guide.olezhek28.courses/system_design/
[in-memory-db]: https://github.com/WithSoull/in-memory-database
