---
type: project-note
project: "[[_MOC - Job Search]]"
status: deferred
---

# Open Source Entry

**Статус:** отложено до сдачи тестового. Канал №5 в [[40 - Projects/Job Search/02 - Channels and Outreach|Channels and Outreach]].

## Идея

Один-два PR в проект компании, куда хочешь попасть, и сообщение мейнтейнеру — и тебя знают по имени ещё до собеса.

## Кандидаты

| Проект | Порог входа | Комментарий |
|---|---|---|
| `yandex/mysync` | — | **не брать** (2026-10-15): контакт с тимлидом уже есть, мест в команде нет — новый PR ничего не даёт |
| `ydb-platform/ydb-go-sdk` | средний | обычный Go-код: ретраи, таймауты, пулы соединений — близко к опыту Postbox |
| `tarantool/go-tarantool` | средний | Go-коннектор, без погружения в ядро СУБД |

## Подход

- Заходить с периферии: клиенты и SDK, а не ядро.
- Метки `good first issue` / `help wanted`, тесты, воспроизведение багов.
- 1–2 часа на выбор issue, неделя на реализацию. Не идёт за неделю — бросить без сожалений.
- Не больше 1–2 часов в день, пока идёт Фаза 1.

## Ресёрч (TODO)

- [x] Пройтись по открытым issue трёх проектов и выбрать 3–5 задач, реальных за неделю.
- [x] Для каждой: ссылка, что нужно сделать, оценка, кто мейнтейнер.

Срез на 2026-10-14. Отброшены issue с открытым PR или исполнителем (в `ydb-go-sdk` многие назначены на Copilot или `asmyasnikov`), а также задачи про ядро и большие фичи.

| Задача | Что сделать | Оценка | Живость проекта | Мейнтейнер / ревьюер | Почему подходит |
|---|---|---|---|---|---|
| [mysync#144: не стартует при битом DNS ZooKeeper](https://github.com/yandex/mysync/issues/144) | Баг уже исправлен в `RandomHostProvider` (`internal/dcs/zk_host_provider.go`), но тестов на него нет. Написать unit-тесты на `Init`: смесь резолвящихся и нерезолвящихся хостов, все хосты битые, нет коннекта. В PR сослаться на issue и предложить его закрыть | 4–6 ч | последний мёрдж 2026-10-13, 2–3 мёрджа в неделю, внешние PR мёржат за 1–3 дня | `teem0n` (мёржит почти всё), также `secwall`, `dodokek` | код ZooKeeper и failover уже знаком, ревьюеры знают по прошлым PR. Самый короткий путь к новому мёрджу и поводу написать команде MDB |
| [ydb-go-sdk#2317: гонка с Rollback в тесте ретраев](https://github.com/ydb-platform/ydb-go-sdk/issues/2317) | В `retry/sql_test.go` убрать `time.Sleep(10ms)`: добавить в `mockConn` сигнал о завершении `Rollback` и дожидаться его в обоих сабтестах. Прогнать с `-race -count=1000` | 2–4 ч | очень живой: мёрджи каждый день, внешние PR мёржат за 1–5 дней | автор issue `kprokopenko`, мёржат `kprokopenko`, `asmyasnikov` | готовый план фикса, пакет `retry` — ровно периферия. Быстрый первый PR для знакомства |
| [ydb-go-sdk#2299: ретрай не-ретраибельного OUT_OF_RANGE](https://github.com/ydb-platform/ydb-go-sdk/issues/2299) | В `internal/conn/conn.go` (`Invoke` и `NewStream`) ошибка оборачивается в `xerrors.Retryable` всякий раз, когда запрос ещё не отправлен, и теряет исходную классификацию. Оборачивать только транзиентные коды, добавить интеграционный тест из issue (есть готовый) | 10–16 ч | то же | `kprokopenko` (автор), `asmyasnikov` | ретраи и классификация gRPC-ошибок — прямое продолжение опыта Postbox, хорошая тема для разговора на собесе. Риск: пересекается с рефакторингом [ydb-go-sdk#2301](https://github.com/ydb-platform/ydb-go-sdk/issues/2301), поэтому сначала спросить в issue, ждут ли точечный фикс |
| [go-tarantool#591: флапающий TestHandlerUpdateError на macOS](https://github.com/tarantool/go-tarantool/issues/591) | В `pool/pool_test.go` у `require.Eventuallyf` заменить общий таймаут 2,5 с на собственный (около 10 с). Воспроизвести локально на macOS с `-race`, показать результат до и после в PR | 2–4 ч | последний мёрдж 2026-10-07, мёрджи волнами, внешний PR (#611) смёржен за 7 дней | мёржит `oleg-jukovec`, ревьюит `bigbes` (автор issue) | работаю на macOS, то есть могу честно воспроизвести. Маленький, но полезный PR про пул соединений |
| [go-tarantool#486: мок для интерфейса Watcher](https://github.com/tarantool/go-tarantool/issues/486) | Сделать переиспользуемый мок `Watcher` с ручной отправкой событий (`Send`), как советует issue, плюс тесты и пример. Сначала согласовать API и пакет в комментарии к issue | 8–12 ч | то же | `bigbes` (автор), `oleg-jukovec` | самостоятельная задача без ядра СУБД: интерфейсы, конкурентность, тесты. Сразу видно, умею ли проектировать API |

**Порядок:** ~~mysync#144~~ (снято 2026-10-15, см. выше), начать с ydb-go-sdk#2317; взять ydb-go-sdk#2317 как быстрый вход в YDB. Если идёт хорошо — ydb-go-sdk#2299 как содержательный PR. Tarantool держать запасным каналом.

**Запас, если основные заберут:**
- [go-tarantool#499: ошибка сервера видна только после Decode](https://github.com/tarantool/go-tarantool/issues/499) — мейнтейнер просит доработать документацию `GetResponse` и добавить пример, 2–3 ч.
- [ydb-go-sdk#1880: опция WithUnsafeStreamResult](https://github.com/ydb-platform/ydb-go-sdk/issues/1880) — метка good first issue. Год назад её взял другой контрибьютор, но PR так и нет: надо спросить в issue, 10–15 ч.
- [ydb-go-sdk#1635: sync.Pool для декодеров в топиках](https://github.com/ydb-platform/ydb-go-sdk/issues/1635) — good first issue. PR [ydb-go-sdk#1650](https://github.com/ydb-platform/ydb-go-sdk/pull/1650) от прошлого исполнителя закрыт без мёрджа, 6–10 ч.

**Не брать:** [ydb-go-sdk#1477](https://github.com/ydb-platform/ydb-go-sdk/issues/1477) (судя по комментарию, уже исправлен), [mysync#122](https://github.com/yandex/mysync/issues/122) (переполнение счётчика бинлогов — нужен дизайн, за неделю не сделать), линтерные issue `student-projects` (по ним висят старые PR).

## Расширенный ресёрч (2026-10-15)

Цель — расширить выбор для первого контрибьютинга. Оценены 36 Go-проектов.

**Как считалось:**
- **Живость** — дата последнего мёрджа и число мёрджей за 30 дней. Считались по 60 последним смёрженным PR, поэтому «60+» означает «не меньше 60».
- **Ревью** — медиана в днях от открытия до мёрджа PR, которые GitHub пометил как внешние. Оценка грубая: в некоторых репозиториях так помечены и сотрудники.
- **GFI/HW** — открытые issue с метками good first issue / help wanted без исполнителя и без открытого PR. Записаны как «свободных / всего с меткой».

### Шорт-лист

| Проект | Связь с резюме | Компания | Последний мёрдж | Мёрджей за 30 дн | Ревью, дн | GFI/HW | Вердикт |
|---|---|---|---|---|---|---|---|
| [wal-g/wal-g](https://github.com/wal-g/wal-g) | бэкапы MySQL/PG в S3, PITR, бинлоги | вырос из Yandex MDB | 2026-10-14 | 60+ | 0,4 | 3/8 | **брать** |
| [pg-sharding/spqr](https://github.com/pg-sharding/spqr) | шардирование PG, роутер, координатор | вырос из Яндекса | 2026-10-09 | 58 | 6,1 | 5/10 (часть уже заняли) | **брать** |
| [ozontech/seq-db](https://github.com/ozontech/seq-db) | хранилище логов, fsync, фракции | Ozon | 2026-10-14 | 39 | 19,8 | 1/2 | **брать** (ревью медленное) |
| [go-mysql-org/go-mysql](https://github.com/go-mysql-org/go-mysql) | протокол MySQL, бинлог, репликация | — | 2026-10-11 | 4 | 2,0 | меток нет, свежие баги | **брать** |
| [ozontech/file.d](https://github.com/ozontech/file.d) | доставка логов, observability | Ozon | 2026-10-14 | 15 | 14,3 | 0/1 | запас |
| [VKCOM/statshouse](https://github.com/VKCOM/statshouse) | метрики, observability | VK | 2026-10-14 | 4 | — | меток нет | запас: PR в основном от команды |
| [avito-tech/go-transaction-manager](https://github.com/avito-tech/go-transaction-manager) | транзакции поверх SQL-драйверов | Авито | 2026-09-26 | 7 | 12,2 | 0 | запас |
| [moira-alert/moira](https://github.com/moira-alert/moira) | алертинг, observability | Контур | 2026-09-30 | 3 | 0,7 | 5/5, но issue 2020–2022 годов | запас |
| [deckhouse/deckhouse](https://github.com/deckhouse/deckhouse) | Kubernetes-платформа, HA | Флант | 2026-09-25 | 60+ | 1,1 | 40/40 | запас: в основном Helm и инфраструктура, мало Go |
| [ClickHouse/clickhouse-go](https://github.com/ClickHouse/clickhouse-go) | пул соединений, таймауты, драйвер | ClickHouse Inc (не РФ) | 2026-10-07 | 8 | 4,2 | 0/1 | запас: на свежие баги PR появляются за дни |
| [VictoriaMetrics/VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics) | TSDB, observability | не РФ | 2026-10-14 | 60+ | 3,1 | 16/17, в основном старые фичи | запас |
| [etcd-io/etcd](https://github.com/etcd-io/etcd) | Raft, консенсус, ретраи | — | 2026-10-14 | 49 | 2,6 | 1/7 | запас: новые баги разбирают за часы |
| [cockroachdb/pebble](https://github.com/cockroachdb/pebble) | LSM-движок хранения | — | 2026-10-13 | 10 | 1,0 | 1/1 (E-starter, но это прототип) | запас |
| [seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) | объектное хранилище | — | 2026-10-12 | 60+ | 0,9 | 2/2, обе крупные | запас |
| [vitessio/vitess](https://github.com/vitessio/vitess) | шардирование MySQL | — | 2026-10-14 | 60+ | 0,3 | 0 | запас |
| [temporalio/temporal](https://github.com/temporalio/temporal) | ретраи, распределённые воркфлоу | — | 2026-10-14 | 60+ | 4,1 | 7/14, но это ядро сервера | запас |
| [prometheus/prometheus](https://github.com/prometheus/prometheus) | observability, TSDB | — | 2026-10-14 | 60+ | 8,6 | 52/100 | запас |
| [thanos-io/thanos](https://github.com/thanos-io/thanos) | observability, объектное хранилище | — | 2026-10-10 | 23 | 1,5 | 63/90 | запас |
| [juicedata/juicefs](https://github.com/juicedata/juicefs) | файловая система поверх S3 | — | 2026-10-14 | 51 | 2,7 | 0 | запас |
| [VictoriaMetrics/VictoriaLogs](https://github.com/VictoriaMetrics/VictoriaLogs) | хранилище логов | не РФ | 2026-10-09 | 31 | 9,9 | 0 | нет |
| [tarantool/tt](https://github.com/tarantool/tt) | CLI для Tarantool | VK Tech | 2026-10-05 | 14 | 138 | 1/1 | нет: внешние PR висят месяцами |
| [ClickHouse/ch-go](https://github.com/ClickHouse/ch-go) | нативный протокол ClickHouse | ClickHouse Inc | 2026-10-07 | 3 | 0,5 | 0/1 | нет |
| [etcd-io/raft](https://github.com/etcd-io/raft) | Raft | — | 2026-10-09 | 4 | 0,0 | 1/1, сложная | нет |
| [hashicorp/raft](https://github.com/hashicorp/raft) | Raft | — | 2026-10-12 | 3 | 7,1 | 0 | нет |
| [jackc/pgx](https://github.com/jackc/pgx) | драйвер PG, пул | — | 2026-10-11 | 11 | 4,7 | 0 | нет |
| [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql) | драйвер MySQL | — | 2026-10-12 | 10 | 1,1 | меток нет, мелочь уже с PR | нет |
| [nats-io/nats-server](https://github.com/nats-io/nats-server) | брокер, JetStream | — | 2026-10-09 | 60+ | 0,9 | 0 | нет |
| [pressly/goose](https://github.com/pressly/goose) | миграции | — | 2026-10-13 | 6 | 9,0 | меток нет | нет |
| [minio/minio](https://github.com/minio/minio) | объектное хранилище | — | 2025-11-06 | 0 | — | — | нет: репозиторий фактически заморожен |
| [yandex/pandora](https://github.com/yandex/pandora) | нагрузочное тестирование | Яндекс | 2024-09-05 | 0 | — | 2/2 | нет: мёрджей нет два года |
| [yandex-cloud/terraform-provider-yandex](https://github.com/yandex-cloud/terraform-provider-yandex) | Terraform | Yandex Cloud | 2025-03-31 | 0 | — | 0 | нет: публичный репозиторий не мёржит |
| [yandex-cloud/go-sdk](https://github.com/yandex-cloud/go-sdk) | SDK облака | Yandex Cloud | 2025-05-16 | 0 | — | 0 | нет |
| [ydb-platform/fq-connector-go](https://github.com/ydb-platform/fq-connector-go) | коннекторы YDB | Яндекс | 2026-02-24 | 0 | — | 0 | нет |
| [ydb-platform/ydb-kubernetes-operator](https://github.com/ydb-platform/ydb-kubernetes-operator) | оператор YDB | Яндекс | 2026-03-13 | 0 | — | 0 | нет |
| [ozontech/allure-go](https://github.com/ozontech/allure-go) | тестовый фреймворк | Ozon | 2026-03-13 | 0 | — | 0 | нет |
| [avito-tech/go-mutesting](https://github.com/avito-tech/go-mutesting) | мутационное тестирование | Авито | 2026-10-02 | 1 | — | 0 | нет |

**Выводы по шорт-листу:**
- Самые выгодные новые проекты — **wal-g** и **spqr**. Оба выросли из той же экосистемы Yandex MDB, что и mysync, поэтому PR туда усиливает уже существующий контакт.
- Из Ozon стоит брать только **seq-db**, но там ревью медленное, около трёх недель.
- Большие международные проекты (etcd, Prometheus, Thanos, Temporal) годятся только как запас. Простые задачи там разбирают за часы, часто AI-агенты, а работодателя из РФ за ними нет.
- Публичные репозитории Yandex Cloud и часть репозиториев ydb-platform не мёржат месяцами, туда не идти.

### Конкретные задачи (новые проекты)

Все issue проверены на 2026-10-15: исполнителя нет, открытого PR нет.

| Задача | Что сделать | Оценка | Мейнтейнер / ревьюер | Почему подходит |
|---|---|---|---|---|
| [wal-g#894: полный бэкап MySQL при выключенном binlog](https://github.com/wal-g/wal-g/issues/894) | Ошибку, судя по ответу мейнтейнера, убрали ещё в [wal-g#1229](https://github.com/wal-g/wal-g/pull/1229). Нужен регрессионный тест: в `docker/mysql_tests/scripts/base_tests` добавить сценарий backup-push и restore с `log_bin=OFF` на отдельном бакете в MinIO. В июне 2025 задачу взял другой человек и пропал, поэтому сначала спросить в issue | 6–10 ч | `ostinru` (MySQL в wal-g, Yandex MDB), мёржат `serprex`, `chipitsine`, `debebantur` | MySQL, бинлоги, S3 и docker-тесты — прямое продолжение mysync и та же команда MDB |
| [spqr#1050: тесты перезагрузки конфига роутера](https://github.com/pg-sharding/spqr/issues/1050) | Написать feature-тесты на перечитывание конфига по SIGHUP. Взять 4–6 настроек (`log_level`, `show_notice_messages`, `frontend_rules`, `backend_rules`, `query_routing`) и задокументировать, какие из них реально перезагружаются | 8–12 ч | `Denchick` (автор), `reshke`, мёржит также `EinKrebs` | тесты и эксплуатационное поведение без ядра; знакомство со шардированием PG |
| [spqr#1657: тип timestamptz для ключа шардирования](https://github.com/pg-sharding/spqr/issues/1657) | Добавить тип `timestamp with timezone` в `CREATE DISTRIBUTION`: парсинг, сравнение границ key range, тесты | 12–16 ч | `Denchick` | осмысленная фича про time-series. Брать вторым PR в spqr, после тестов |
| [seq-db#199: fsync через конфиг фракции](https://github.com/ozontech/seq-db/issues/199) | Позволить отключать `fsync` через конфиг фракции и ускорить с его помощью тесты. Прошлый PR [seq-db#417](https://github.com/ozontech/seq-db/pull/417) закрыт без мёрджа 2026-09-27: сначала прочитать его ревью и спросить, чего ждут | 4–6 ч | `cheb0` (автор), мёржат `dkharms`, `forshev`, `eqimd` | fsync и долговечность записи — тема из DDIA, метка good-first-issue, контакт с Ozon |
| [seq-db#49: send on closed channel при маленькой фракции](https://github.com/ozontech/seq-db/issues/49) | Воспроизвести панику на текущем `main` с `--total-size=64KB --frac-size=32KB`. Если воспроизводится — найти гонку между appender и закрытием фракции, исправить и добавить тест. Если нет — показать это в issue и предложить закрыть | 6–10 ч | `dkharms` | воспроизведение бага и конкурентность в настоящем хранилище |
| [go-mysql#1198: пустая строка пишется как NULL](https://github.com/go-mysql-org/go-mysql/issues/1198) | В `BuildSimpleTextResultset` решать, что значение NULL, по исходному значению, а не по отформатированным байтам. Плюс тест на `""` и `[]byte{}`. Мейнтейнер прямо зовёт присылать PR, но может предложить другой подход, поэтому коротко описать план в issue | 2–4 ч | `lance6716`, также `dveeden` | протокол MySQL; быстрый и понятный PR в известную библиотеку |

**Отброшены, потому что уже есть PR или исполнитель:**
- wal-g: [#2552](https://github.com/wal-g/wal-g/issues/2552), [#1108](https://github.com/wal-g/wal-g/issues/1108);
- clickhouse-go: [#1990](https://github.com/ClickHouse/clickhouse-go/issues/1990) (дедлок пула), [#2040](https://github.com/ClickHouse/clickhouse-go/issues/2040), [#2016](https://github.com/ClickHouse/clickhouse-go/issues/2016);
- go-mysql: [#1195](https://github.com/go-mysql-org/go-mysql/issues/1195);
- seq-db: [#37](https://github.com/ozontech/seq-db/issues/37);
- file.d: [#912](https://github.com/ozontech/file.d/issues/912);
- spqr: [#1321](https://github.com/pg-sharding/spqr/issues/1321) (занят);
- etcd: [#22526](https://github.com/etcd-io/etcd/issues/22526), [#22574](https://github.com/etcd-io/etcd/issues/22574).

### Обновлённая рекомендация на 2–3 недели

Правило: не больше двух открытых PR одновременно. На задачи, где был прошлый исполнитель или закрытый PR, заранее оставить комментарий «можно взять?», чтобы ответ пришёл к началу следующей недели.

> 2026-10-15: mysync из плана убран — контакт с тимлидом уже есть, мест в команде нет. Основной проект — wal-g.

1. **Неделя 1.** [ydb-go-sdk#2317](https://github.com/ydb-platform/ydb-go-sdk/issues/2317) и [go-mysql#1198](https://github.com/go-mysql-org/go-mysql/issues/1198) — два коротких PR (по 2–4 ч). В первый же день оставить комментарий «можно взять?» в [wal-g#894](https://github.com/wal-g/wal-g/issues/894) и [seq-db#199](https://github.com/ozontech/seq-db/issues/199).
2. **Неделя 2.** [wal-g#894](https://github.com/wal-g/wal-g/issues/894) — основной проект: бэкапы и PITR MySQL/PG в S3 на Go, продолжение mysync и OpenS3 в портфолио. Если в issue не ответили — другая задача в wal-g или [spqr#1050](https://github.com/pg-sharding/spqr/issues/1050).
3. **Неделя 3.** Один содержательный PR на выбор: [ydb-go-sdk#2299](https://github.com/ydb-platform/ydb-go-sdk/issues/2299) (ретраи, YDB) или [seq-db#199](https://github.com/ozontech/seq-db/issues/199) (контакт с Ozon; ревью долгое, поэтому открыть пораньше).

Tarantool ([go-tarantool#591](https://github.com/tarantool/go-tarantool/issues/591)) и spqr#1657 остаются в запасе, если какой-то канал замолчит.
