# S3 Storage Landscape

## Зачем эта заметка

Здесь собран контекст по современным объектным хранилищам и S3-совместимым системам, который нужен для классификации аналогов OpenS3 и дальнейшего написания исследовательского раздела ВКР.

Главная мысль: **S3 — это не конкретная архитектура хранения**. Нужно различать:

- **Amazon S3** — managed-сервис AWS;
- **S3 API** — объектная модель и набор HTTP-операций (`PUT`, `GET`, multipart, versioning, lifecycle и т. д.);
- **S3-compatible storage** — система, реализующая достаточную часть S3 API для работы S3-клиентов и SDK.

Две S3-compatible системы могут иметь совершенно разную внутреннюю архитектуру: отдельный Metadata Service, metadata поверх общей распределённой storage-платформы или peer-to-peer metadata без центрального каталога.

---

# 1. Классификация рынка

| Класс | Примеры | Основная идея |
|---|---|---|
| Эталонный managed S3 | AWS S3 | Эталон API и пользовательской семантики S3; внутренняя реализация закрыта |
| Managed S3-compatible | Cloudflare R2, Backblaze B2, Wasabi, Yandex Object Storage, Selectel S3 | Провайдер управляет инфраструктурой, пользователь получает S3 endpoint |
| Self-hosted S3-first | MinIO/AIStor, Garage, RustFS | Основной продукт — собственное S3-совместимое хранилище |
| Распределённая storage-платформа + S3 frontend | Ceph RGW, Apache Ozone, SeaweedFS, OpenStack Swift | S3 реализован как один из интерфейсов над более общей storage-системой |
| Enterprise object storage | NetApp StorageGRID, Cloudian HyperStore, Dell ECS/ObjectScale, Scality | Крупные on-prem/private-cloud решения с богатыми placement/durability/lifecycle policy |
| Другие крупные object stores | Google Cloud Storage, Azure Blob | Не S3-native, но решают аналогичную задачу и особенно полезны для анализа tiering |

Для OpenS3 самые полезные аналоги по архитектуре и предмету ВКР: **AWS S3, Ceph RGW, MinIO/AIStor, SeaweedFS, Garage, RustFS, Apache Ozone**.

---

# 2. Что сравнивать у объектных хранилищ

Сравнивать аналоги только по наличию `versioning`, `multipart` и `lifecycle` недостаточно. Для ВКР полезнее смотреть по нескольким осям.

## 2.1. API layer

- насколько полон S3 API;
- strong или eventual semantics после записи;
- versioning;
- multipart;
- Object Lock;
- bucket policies/IAM;
- notifications/events.

## 2.2. Metadata plane

- есть ли отдельный metadata service;
- где хранится namespace `bucket/key`;
- где хранится информация о версиях;
- есть ли отдельный bucket index;
- как metadata шардируется;
- как согласуется metadata с физическим blob.

## 2.3. Data plane

- объект хранится единым blob или режется на chunks/shards;
- replication или erasure coding;
- как выбираются storage nodes;
- как выполняется repair/rebalance;
- могут ли разные данные жить в разных физических пулах.

## 2.4. Placement и storage classes

Важно не считать `storage class` синонимом типа диска. В разных системах storage class может означать:

1. **Физический pool** — например, один класс отображается на SSD pool, другой на HDD pool.
2. **Удалённый backend** — local primary + remote S3 tier.
3. **Экономический/service class** — разная цена, durability, availability или retention semantics.
4. **Почти только billing class** — технические характеристики могут оставаться одинаковыми.
5. **Protection policy** — разные replication/erasure coding параметры.

Для OpenS3 корректнее определять класс хранения так:

> **Класс хранения — логически выделенный набор ресурсов с заданными характеристиками ёмкости, производительности и, при наличии, стоимости.**

В экспериментальном стенде HOT и COLD уже могут быть реализованы конкретными физическими пулами, например SSD/NVMe и HDD.

---

# 3. AWS S3 — эталон S3 semantics

AWS S3 нужен прежде всего как эталон поведения API, а не как открытый архитектурный аналог.

## 3.1. Consistency

Современный Amazon S3 предоставляет strong read-after-write consistency для основных операций чтения и записи. Обновление одного key атомарно: клиент не должен видеть «полузаписанный» объект.

Это важно для OpenS3: успешный ответ клиенту не должен возникать раньше, чем система способна обеспечить заявленную видимость объекта.

Источник: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

## 3.2. Storage classes

Примеры классов AWS:

- S3 Standard;
- Standard-IA;
- One Zone-IA;
- Glacier Instant Retrieval;
- Glacier Flexible Retrieval;
- Glacier Deep Archive;
- Express One Zone;
- Intelligent-Tiering.

Storage class здесь не сводится к «SSD против HDD». Это логическая услуга со своей комбинацией latency, availability, redundancy, minimum retention и pricing semantics.

Источник: https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html

## 3.3. Lifecycle

S3 Lifecycle — заранее заданный rule engine. Правила могут использовать возраст/дату объекта, prefix, tags, size и отдельно управлять current/noncurrent versions.

Упрощённо:

```text
logs/*
  30 days  -> STANDARD_IA
  365 days -> GLACIER
```

Это **не predictive tiering**: система исполняет правило, заданное пользователем.

## 3.4. Intelligent-Tiering

S3 Intelligent-Tiering автоматически отслеживает отсутствие обращений и переводит данные между уровнями. При новом обращении объект может вернуться в frequent tier.

Ключевой вывод для ВКР:

> **AWS Intelligent-Tiering реагирует на историю доступа, но не прогнозирует будущий спрос.**

Поэтому AWS-like recency policy — обязательный baseline для OpenS3:

```text
if no_access_for >= N:
    move_to_cold()
```

против predictive подхода:

```text
expected_reads = model(features)
decision = optimizer(expected_reads, capacity, latency, migration_cost, ...)
```

Источники:

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-intelligent-tiering.html

---

# 4. Ceph RGW — зрелая self-hosted классика

Ceph — одна из самых важных систем для глубокого архитектурного сравнения с OpenS3.

Ceph не является только S3-хранилищем. Внизу находится распределённое объектное хранилище **RADOS**, а поверх него строятся разные интерфейсы:

```text
                    RADOS
               /      |      \
             RBD    CephFS    RGW
            block    file      |
                              S3/Swift
```

## 4.1. Разделение metadata и payload

У RGW полезно различать как минимум:

- metadata;
- bucket index;
- object payload.

Bucket index содержит сведения о ключах и объектах и может шардироваться. Payload объектов хранится отдельно в data pool.

Это полезная аналогия к OpenS3:

```text
OpenS3
Metadata Service -> namespace/version/placement
Storage Service  -> payload
```

Источник: https://docs.ceph.com/en/latest/radosgw/layout/

## 4.2. Versioning и logical head

Ceph не обязан сводить versioning к полю `current_version_id` в одной строке metadata.

У RGW версии могут иметь собственные head objects, а логическое имя объекта использует **Object Logical Head (OLH)** как indirection на текущую версию.

Упрощённо:

```text
cat.jpg
   |
   OLH
   |
   +----> version abc123
              |
            payload
```

Это полезная архитектурная идея для размышлений о current version, delete markers и конкурентных PUT.

Источник: https://docs.ceph.com/en/latest/dev/radosgw/bucket_index/

## 4.3. Согласование bucket index и object state

Payload/head и bucket index могут находиться в разных RADOS objects, поэтому общей атомарной транзакции между ними нет.

RGW использует протокол примерно вида:

```text
1. PREPARE в bucket index
2. запись object HEAD
3. COMMIT bucket index
```

При сбое могут оставаться pending entries, которые затем проверяются/восстанавливаются.

Это напрямую связано с проблемой OpenS3: нельзя получить metadata, указывающую на blob, который физически ещё не существует или не является доступным.

Источник: https://docs.ceph.com/en/latest/dev/radosgw/bucket_index/

## 4.4. Physical storage classes

В RGW storage class может быть сопоставлен конкретному physical data pool:

```text
STANDARD -> fast pool
COLD     -> capacity pool
```

Lifecycle затем может менять placement между storage classes.

Ceph также позволяет отдельно выбирать быстрые ресурсы для metadata/index и более дешёвый/ёмкий pool для payload.

Источник: https://docs.ceph.com/en/latest/radosgw/placement/

## 4.5. Сильные стороны

- зрелая распределённая архитектура;
- replication и erasure coding;
- versioning;
- lifecycle;
- storage classes;
- bucket policies;
- notifications;
- multisite;
- encryption;
- dynamic resharding;
- object/block/file interfaces.

## 4.6. Слабая сторона

Главная цена возможностей Ceph — **операционная сложность**. Это важный контраст с OpenS3: дипломный проект может быть гораздо уже, прозрачнее и сфокусирован именно на placement и СППР.

---

# 5. MinIO / AIStor — исторический de-facto self-hosted S3

MinIO долгие годы был одним из наиболее очевидных ответов на «нужен свой S3». Он был S3-first, хорошо контейнеризировался и имел развитую экосистему клиентов и инструментов.

Важное изменение: GitHub-репозиторий `minio/minio` был архивирован 25 апреля 2026 года. Развитие продукта сместилось в сторону AIStor Free/Enterprise.

Источник: https://github.com/minio/minio

## 5.1. Erasure coding

MinIO/AIStor защищает payload, разбивая объект на data и parity shards.

```text
object
  |
  +--> data shards
  +--> parity shards
```

Источник: https://docs.min.io/aistor/operations/core-concepts/erasure-coding/

## 5.2. Storage class != physical tier

Исторические storage-class настройки MinIO могли влиять на parity/redundancy. Это хороший пример того, почему нельзя автоматически считать `StorageClass=STANDARD` эквивалентом SSD, а другой класс — HDD.

## 5.3. Object transition / tiering

AIStor поддерживает lifecycle transition на дополнительный remote tier, например:

```text
local NVMe/SSD
      |
      | lifecycle
      v
remote S3 / second AIStor / GCS / Azure
```

После transition основной сервис продолжает хранить metadata, позволяющую найти payload в удалённом tier. Клиент продолжает обращаться к исходному endpoint.

Это важная идея для OpenS3: metadata может описывать **логическое расположение**, а payload физически находиться в другом backend.

Источник: https://docs.min.io/aistor/administration/object-lifecycle-management/object-tiering/

## 5.4. Events

MinIO/AIStor имеет развитую модель bucket notifications и интеграций с Kafka, RabbitMQ, NATS, MQTT, PostgreSQL, Redis, Elasticsearch и webhook.

Это подтверждает, что event-driven storage pipeline и Kafka вокруг object lifecycle — нормальный промышленный паттерн.

Источник: https://docs.min.io/aistor/administration/bucket-notifications/

---

# 6. SeaweedFS — сильный современный open-source challenger

SeaweedFS — активно развивающаяся storage platform, которая предоставляет не только S3, но также blob storage, FUSE/POSIX-like filesystem, Hadoop/WebDAV и другие интерфейсы.

Источник: https://github.com/seaweedfs/seaweedfs

## 6.1. Главная идея: master управляет volumes, а не каждым файлом

Вместо хранения глобального отображения каждого файла на каждый chunk master в основном управляет volumes:

```text
Master
  |
  +-- Volume 12 -> node A
  +-- Volume 13 -> node B
  +-- Volume 14 -> node C
```

Это уменьшает metadata pressure на master и хорошо подходит для очень больших namespace.

## 6.2. Filer

Файловый namespace и metadata предоставляет **Filer**. Его metadata backend можно строить поверх PostgreSQL, MySQL, Cassandra, Redis, CockroachDB, etcd и других систем.

Упрощённо:

```text
S3 Gateway
     |
   Filer ------ metadata DB
     |
Volume Servers
     |
   payload
```

Это архитектурно очень близко к явному разделению metadata plane и data plane в OpenS3.

## 6.3. Stateless S3 Gateway

S3 gateway можно масштабировать независимо и ставить несколько экземпляров за load balancer:

```text
          Load Balancer
             /     \
           S3G     S3G
             \     /
              Filer
                |
         Volume Servers
```

Это хороший паттерн для OpenS3 Gateway.

## 6.4. Lifecycle через change log

У SeaweedFS есть дизайн, где lifecycle worker может обрабатывать persistent metadata change log, а не постоянно сканировать весь namespace.

```text
metadata events
      |
      v
persistent log
      |
      v
lifecycle worker
      |
      +--> delete
      +--> transition
```

Это очень интересная идея для event-driven lifecycle и будущего ML/telemetry pipeline OpenS3.

Источник: https://github.com/seaweedfs/seaweedfs/blob/master/weed/s3api/s3lifecycle/DESIGN.md

## 6.5. Позиционирование

SeaweedFS уже нельзя считать игрушечным newcomer. Это зрелый и активно развивающийся проект. При этом он решает гораздо более широкую задачу, чем OpenS3, поэтому архитектура сложнее и менее S3-specific.

---

# 7. Garage — lightweight geo-distributed подход

Garage от Deuxfleurs сознательно не пытается реализовать весь Amazon S3. Цель — относительно небольшой S3-compatible storage для self-hosted и geo-distributed deployments.

Источник: https://github.com/deuxfleurs-org/garage

## 7.1. Репликация и quorum

Типичная конфигурация использует replication factor 3. В consistent-режиме quorum чтения/записи обеспечивает read-after-write semantics.

У Garage можно явно ослаблять consistency ради availability, что делает CAP trade-off частью конфигурации.

Источник: https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/

## 7.2. Разделение metadata и data

Garage рекомендует размещать metadata на быстром SSD, а payload — на ёмких HDD:

```text
metadata_dir -> SSD
data_dir     -> HDD
```

Это хороший практический паттерн: **metadata и payload имеют разные профили нагрузки и не обязаны жить на одинаковом hardware**.

## 7.3. Ограниченная S3 compatibility

Garage поддерживает core S3 use cases, включая основные object operations, multipart, presigned URLs и SigV4, но не является полным клоном AWS S3. Некоторые возможности, включая полноценный S3 versioning/репликацию/Object Lock/notifications и сложный tier transition, отсутствуют или ограничены.

Источник: https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/

Главный урок:

> **S3-compatible не означает Amazon S3 clone.**

---

# 8. RustFS — главный новый хайп 2026

RustFS — быстро набравший популярность S3-compatible object store на Rust. На бумаге он объединяет S3 API, distributed storage, erasure coding, IAM, versioning, multipart, replication и web console.

Источник: https://github.com/rustfs/rustfs

## 8.1. Почему проект интересен

- современный Rust stack;
- большой интерес сообщества;
- агрессивное развитие;
- позиционирование как новая альтернатива MinIO/Ceph;
- focus на performance и S3 compatibility.

## 8.2. Почему его нельзя автоматически считать зрелой заменой Ceph/MinIO

Проект всё ещё находится на стадии быстрого maturation. Compatibility matrix описывает протестированный subset S3 API, а не полное совпадение с AWS S3.

Источник: https://github.com/rustfs/docs.rustfs.com/blob/main/content/en/reference/s3-compatibility.md

В 2026 году проект также проходил через заметный security/semantics churn: исправлялись проблемы в IAM, Object Lock, historical versions, service accounts и других механизмах.

Это не делает RustFS плохим проектом, но хорошо показывает разницу между:

- популярностью;
- скоростью разработки;
- production maturity.

**Классификация:** перспективный newcomer и главный hype-кандидат 2026, но пока не «boring storage infrastructure» уровня Ceph.

---

# 9. Apache Ozone — очень полезный архитектурный аналог

Apache Ozone возник в Hadoop ecosystem и ориентирован на огромные object namespaces.

Источник: https://ozone.apache.org/docs/core-concepts/architecture/

## 9.1. Разделение ролей

```text
                  S3 Gateway
                      |
            +---------+---------+
            |                   |
      metadata calls          payload
            |                   |
            v                   v
      Ozone Manager          Datanodes
            |
            v
 Storage Container Manager
```

**Ozone Manager** управляет namespace: volumes, buckets, keys и metadata.

**Storage Container Manager** управляет datanodes, containers, blocks, replicas и placement.

**Datanodes** физически хранят data blocks.

**S3 Gateway** — stateless protocol adapter.

Источник: https://ozone.apache.org/docs/core-concepts/architecture/s3-gateway/

## 9.2. Почему это важно для OpenS3

Ozone показывает очень чистое разделение:

```text
Gateway != Metadata manager != Placement manager != Storage nodes
```

Это один из самых полезных референсов для service decomposition OpenS3.

---

# 10. OpenStack Swift — историческая классика

Swift появился до того, как S3 compatibility стала фактически обязательным требованием для object storage.

Native API Swift — не S3. S3 реализуется через middleware:

```text
S3 client
   |
s3api middleware
   |
Swift proxy
   |
Swift storage
```

Источник: https://docs.openstack.org/swift/latest/middleware.html

## 10.1. Rings

Swift использует ring для отображения partition на storage nodes/devices.

```text
object
  |
 hash
  |
partition
  |
 ring
  |
storage nodes
```

## 10.2. Storage Policies

Разные storage policies могут использовать разные object rings, device sets и durability schemes, включая replication и erasure coding.

Источник: https://docs.openstack.org/swift/latest/overview_policies

Swift полезен как исторически важный архитектурный представитель object storage, но для OpenS3 это скорее reference design, чем главный современный конкурент.

---

# 11. Enterprise object storage

Enterprise-системы полезны не как прямые конкуренты дипломного проекта, а как источник зрелых идей по placement, lifecycle, durability и multi-site эксплуатации.

## 11.1. NetApp StorageGRID

StorageGRID имеет развитый **Information Lifecycle Management (ILM)**. Policy может определять:

- какие объекты подходят под правило;
- где они должны храниться;
- replication или erasure coding;
- сколько копий нужно;
- как placement меняется со временем;
- требуется ли перенос в Cloud Storage Pool.

Пример:

```text
backup objects
  0-30d    -> 3 replicas across sites
  30-365d  -> erasure coding
  >365d    -> cloud pool
```

Это хороший пример generalized placement policy, близкой по роли к будущему decision engine OpenS3, только решения задаются правилами администратора.

Источники:

- https://docs.netapp.com/us-en/storagegrid/ilm/
- https://docs.netapp.com/us-en/storagegrid/ilm/what-erasure-coding-is.html

StorageGRID также позволяет выбирать consistency level, то есть явно экспонирует trade-off между consistency и availability.

Источник: https://docs.netapp.com/us-en/storagegrid/s3/consistency.html

## 11.2. Cloudian HyperStore

Cloudian использует shared-nothing peer-to-peer подход без одного центрального metadata/head controller. Узлы участвуют в I/O и хранении распределённого состояния.

Поддерживаются replication и erasure coding, multi-site deployment и lifecycle/tiering.

Источник: https://cloudian.com/products/hyperstore/

Это контрпример архитектуре с выделенным Metadata Service.

## 11.3. Dell ECS / ObjectScale

Dell ECS/ObjectScale интересен тем, что durability scheme сама является частью economics storage tier.

Используются Reed-Solomon erasure-coding layouts, причём разные профили могут применяться к различным классам данных.

У больших и маленьких объектов может отличаться write path: некоторые данные сначала защищаются репликацией, после чего агрегируются и переводятся в erasure-coded representation.

Источники:

- https://www.dell.com/support/manuals/en-us/ecs-appliance-/ecs_p_adminguide_3_5_0_1/ecs-data-protection
- https://infohub.delltechnologies.com/en-us/l/dell-objectscale-overview-and-architecture-1/overview-7112/
- https://infohub.delltechnologies.com/en-us/p/dell-ecs-data-protection-and-data-path-overview-part-ii/

## 11.4. Scality RING / ARTESCA

Scality RING ориентирован на очень крупные private/sovereign object-storage deployments.

ARTESCA сфокусирован на S3 workloads, backup, Object Lock и ransomware protection. Поддерживает S3 endpoints, versioning, replication, lifecycle и IAM-compatible модель.

Источники:

- https://www.scality.com/products/ring/
- https://downloads.scality.com/artesca-ova/doc/general_introduction.html

---

# 12. Managed S3-compatible сервисы

## 12.1. Cloudflare R2

Cloudflare публично описывает архитектуру как сочетание R2 Gateway и distributed Metadata Service.

Упрощённо:

```text
R2 Gateway
    |
distributed Metadata Service
    |
storage infrastructure
```

Metadata Service использует Durable Objects и обеспечивает strong consistency.

Источник: https://developers.cloudflare.com/r2/how-r2-works/

R2 публикует собственную S3 compatibility matrix, что ещё раз показывает: даже крупный S3-compatible продукт не обязан реализовывать абсолютно каждый AWS API.

Источник: https://developers.cloudflare.com/r2/api/s3/api/

Главная рыночная дифференциация R2 — economics и отсутствие egress fee, а не принципиально новый object-storage abstraction.

## 12.2. Backblaze B2

B2 имеет собственный native API и S3-compatible API поверх той же storage system.

```text
storage
  +--> B2 Native API
  +--> S3-compatible API
```

Источник: https://www.backblaze.com/docs/cloud-storage-s3-compatible-api

Интересная особенность: B2 сохраняет file versions и позволяет управлять ими lifecycle rules.

Источник: https://www.backblaze.com/docs/cloud-storage-s3-compatible-api-bucket-versions

## 12.3. Wasabi

Wasabi — managed S3-compatible storage, ориентированный в том числе на backup/archive workloads.

Поддерживает versioning, lifecycle и Object Lock. Lifecycle применяется асинхронно и не обязан исполняться мгновенно.

Источник: https://docs.wasabi.com/docs/lifecycle-1

Для ВКР Wasabi важнее как рыночный managed-аналог, чем как источник уникальной архитектуры.

---

# 13. Yandex Object Storage

Yandex Object Storage полезен для понимания того, что storage class не обязан означать другой тип physical storage.

Классы включают STANDARD, COLD, ICE и INTELLIGENT_TIERING.

Документация подчёркивает, что STANDARD и COLD могут иметь одинаковые технические характеристики и схему репликации, а различаться прежде всего экономикой операций и хранения.

Источник: https://yandex.cloud/en/docs/storage/concepts/storage-class

## Intelligent Tiering

Упрощённая схема:

```text
FREQUENT
   |
   | low access
   v
INFREQUENT
   |
   | longer low access
   v
ARCHIVE

new access -> FREQUENT
```

Это reactive access-aware tiering, а не ML forecast.

Lifecycle отдельно поддерживает rule-based transitions и expiration.

Источник: https://yandex.cloud/en/docs/storage/concepts/lifecycles

---

# 14. Selectel S3 — storage class как billing model

Selectel — очень полезный контрпример для определения `storage class`.

В документации классы `standard`, `infrequent`, `glacier` различаются прежде всего тарифной моделью, а техническая производительность может оставаться одинаковой.

Источник: https://docs.selectel.ru/en/s3/quickstart/

Следствие для ВКР:

> Понятие класса хранения зависит от реализации и может обозначать физический pool, уровень доступности, схему резервирования либо исключительно тарифную модель.

---

# 15. Google Cloud Storage

Хотя GCS не является self-hosted S3 clone, он важен для сравнения именно с интеллектуальным tiering.

Классы:

- Standard;
- Nearline;
- Coldline;
- Archive.

## 15.1. Object Lifecycle Management

Rule-based механизм: пользователь задаёт условия, система выполняет transition/delete.

Источник: https://docs.cloud.google.com/storage/docs/lifecycle

## 15.2. Autoclass

Autoclass автоматически анализирует access pattern и меняет storage class.

Типовая логика:

```text
new/read -> STANDARD
no access -> Nearline -> Coldline -> Archive
new access -> hotter class
```

Это ещё один сильный baseline против predictive ML tiering.

Источник: https://docs.cloud.google.com/storage/docs/autoclass

---

# 16. Azure Blob Storage

Azure Blob имеет Hot, Cool, Cold и Archive tiers.

Ключевой нюанс: Hot/Cool/Cold являются online tiers и могут иметь близкие latency/throughput characteristics. Archive уже требует rehydration и имеет другую latency model.

Источник: https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview

Azure Lifecycle Management позволяет rule-based менять tier объектов.

Источник: https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview

Главный вывод: **COLD не является универсальным синонимом «медленный HDD»**.

---

# 17. Кто классика, кто niche, кто hype

| Система | Категория на 2026 год | Почему |
|---|---|---|
| AWS S3 | эталон | определяет S3 ecosystem и ожидаемую semantics |
| Ceph RGW | вечная self-hosted классика | зрелая distributed architecture и огромный набор возможностей |
| OpenStack Swift | историческая классика | важный object-store design, но S3 не native |
| Apache Ozone | зрелый niche | серьёзный big-data object store, но не простой standalone S3 server |
| MinIO | исторический de-facto стандарт | сильно повлиял на self-hosted S3 рынок; OSS repo теперь archived |
| SeaweedFS | активно растущий зрелый challenger | давно существует, активно развивается, широкая storage-platform архитектура |
| Garage | зрелый lightweight niche | небольшой scope, geo-distribution, понятные trade-offs |
| RustFS | главный hype/newcomer | быстрый рост и современный stack, но maturity/security churn ещё высокий |
| StorageGRID / Cloudian / Dell / Scality | enterprise classics | богатая policy/durability модель и долгий production history |
| R2 / B2 / Wasabi | managed alternatives | конкурируют economics/ecosystem, а не self-host deployment |

Важно: GitHub stars почти ничего не говорят о зрелости storage software.

Для storage maturity критичны годы эксплуатации в ситуациях:

- disk failure;
- node failure;
- network partition;
- crash в середине записи;
- cluster upgrade;
- metadata corruption;
- rebalance;
- конкурентные PUT одного key;
- versioning + lifecycle race;
- partial multipart upload.

Поэтому быстро растущий newcomer нельзя автоматически считать более зрелым, чем старый Ceph.

---

# 18. Классификация по архитектуре

## 18.1. Где живёт metadata

### Явный metadata service

- OpenS3;
- Apache Ozone;
- Cloudflare R2;
- SeaweedFS Filer.

### Metadata поверх общей distributed storage substrate

- Ceph RGW.

### Peer-to-peer / distributed metadata

- Garage;
- Cloudian.

## 18.2. Защита payload

### Replication

- Garage;
- часть StorageGRID policies.

### Erasure coding

- Ceph;
- MinIO/AIStor;
- Apache Ozone;
- Dell ECS/ObjectScale;
- StorageGRID;
- SeaweedFS;
- Scality.

### Policy-dependent combination

Enterprise и крупные distributed stores часто позволяют выбирать replication или EC в зависимости от workload/policy.

## 18.3. Смысл storage class

```text
A. Physical pool
   Ceph
   STANDARD -> fast pool
   COLD     -> capacity pool

B. Remote backend
   MinIO/AIStor
   primary -> remote tier

C. Service/economic class
   AWS / Azure / GCS / Yandex

D. Почти billing class
   Selectel

E. Protection-policy distinction
   enterprise systems
```

---

# 19. Где находится OpenS3 относительно аналогов

Текущая модель OpenS3 ближе всего к системам с явным разделением metadata plane и data plane.

Упрощённо целевая архитектура:

```text
                         Gateway
                            |
                       Metadata
                      PostgreSQL
                    /           \
                  HOT           COLD
               Storage        Storage
                    \           /
                     Decision Engine
                           ^
                           |
                      ML forecast
```

По архитектурной родственности полезно изучать примерно в таком порядке:

1. **Apache Ozone** — очень чистое разделение Gateway / Metadata / Placement / Datanodes.
2. **SeaweedFS** — S3 Gateway + Filer + отдельный data plane.
3. **Ceph RGW** — зрелый metadata/index/payload design и physical storage classes.
4. **MinIO/AIStor** — S3-first system и lifecycle/remote tiering.
5. **Garage** — минималистичный distributed подход.
6. **AWS S3** — дальше по внутренней архитектуре, но главный reference по API semantics.

---

# 20. Идеи, которые полезно перенять в OpenS3

## Из Ceph

1. Явное отображение `storage_class -> physical data pool`.
2. Разделение metadata, bucket index и payload.
3. Отдельная модель current version через indirection/logical head.
4. Продуманный commit/recovery protocol между metadata/index и physical object state.

## Из Apache Ozone

Жёсткое разделение ролей:

```text
Gateway
Metadata manager
Placement manager
Storage nodes
```

Это хороший референс для service decomposition.

## Из SeaweedFS

1. Stateless S3 Gateway.
2. Persistent metadata change log.
3. Использование change log для lifecycle/analytics вместо полного постоянного сканирования namespace.

## Из MinIO/AIStor

Transparent remote tier:

```text
metadata остаётся локально
payload может находиться в другом backend
```

## Из Garage

1. Простая явная quorum/consistency model.
2. Размещение metadata на SSD, payload на HDD.

## Из StorageGRID

Decision engine как generalized placement policy:

```text
conditions/features
       |
       v
decision
       |
       v
placement + protection
```

## Из AWS / GCS / Yandex

Обязательный baseline:

```text
no access for N days -> colder tier
new access           -> hotter tier
```

И уже поверх этого проверять полезность predictive ML.

---

# 21. Что сравнивать глубоко в ВКР

Не стоит подробно описывать 15 продуктов одинаковым объёмом. Для основной части исследования достаточно глубоко разобрать 6–7 систем.

| Аналог | Зачем нужен в ВКР |
|---|---|
| Amazon S3 | reference API + Lifecycle + Intelligent-Tiering |
| Ceph RGW | зрелый self-hosted distributed S3 + physical storage classes |
| MinIO/AIStor | исторически самый узнаваемый self-hosted S3 + lifecycle/remote tiering |
| SeaweedFS | современный OSS storage + явное разделение metadata/data plane |
| Garage | lightweight противоположность тяжёлым storage platforms |
| RustFS | актуальный newcomer и тренд 2026 |
| Apache Ozone | архитектурный reference для service decomposition |

В обзорной таблице можно дополнительно привести:

- OpenStack Swift;
- StorageGRID;
- Cloudian;
- Dell ECS/ObjectScale;
- Scality;
- Cloudflare R2;
- Backblaze B2;
- Wasabi;
- Google Cloud Storage;
- Azure Blob Storage;
- Yandex Object Storage;
- Selectel S3.

---

# 22. Эволюция tiering-подходов

Полезная классификация именно для темы ВКР.

## Поколение 1. Manual placement

```text
PUT object
StorageClass = X
```

Пользователь сам выбирает класс.

## Поколение 2. Static lifecycle rules

```text
if age >= 30d:
    move_to_cold()
```

Примеры: AWS Lifecycle, Ceph Lifecycle, MinIO Lifecycle.

## Поколение 3. Reactive access-aware tiering

```text
if no GET for N days:
    colder()

if GET:
    hotter()
```

Примеры: AWS Intelligent-Tiering, GCS Autoclass, Yandex Intelligent Tiering.

## Поколение 4. Predictive tiering

```text
history + metadata
       |
       v
     model
       |
       v
expected future demand
       |
       v
 decision engine
       |
       v
   placement
```

Это область OpenS3 ВКР.

Но сама идея ML-driven tiering уже существует в исследованиях, поэтому защищаемый вклад не должен формулироваться как «мы впервые применили ML для HOT/COLD».

---

# 23. Исследования по intelligent tiering

## Herodotou & Kakoulli, 2019

Работа по автоматизации tiered storage уже использует ML/XGBoost, историю обращений, признаки объектов и решение о перемещении между уровнями.

Источник: https://arxiv.org/abs/1907.02394

Следствие: **сам факт использования boosting/ML для прогнозирования обращения не является новизной OpenS3**.

## Khan et al., 2024

Рассматривается перераспределение между несколькими storage tiers и сравниваются rule-based и более сложные стратегии.

Источник: https://link.springer.com/article/10.1007/s00607-024-01281-2

Следствие: сильные эвристики могут быть конкурентоспособны; ML должен сравниваться не с заведомо слабым baseline.

## Baleen, FAST 2024

Baleen использует ML для admission/prefetch в flash cache, но оценивает конечный системный эффект на backend load.

Источник: https://www.microsoft.com/en-us/research/publication/baleen-ml-admission-prefetching-for-flash-caches/

Главный методологический урок:

> **Качество ML-модели не равно качеству storage system.**

Для OpenS3 `RMSE`, `MAE` или classification metrics недостаточно. Нужно измерять конечный результат СППР:

- необходимую HOT capacity;
- количество миграций;
- число обращений к COLD;
- latency;
- стоимость по принятой модели;
- ошибочные переносы востребованных объектов;
- migration load.

---

# 24. Ментальная модель object storage

```text
                           OBJECT STORAGE
                                |
             +------------------+------------------+
             |                  |                  |
          API layer        Metadata plane       Data plane
             |                  |                  |
       S3 semantics        key/version         blob/chunks
       auth/policy         index/placement     replica/EC
       multipart           lifecycle state     SSD/HDD/cloud
             |                  |                  |
             +------------------+------------------+
                                |
                         Placement policy
                                |
                 +--------------+--------------+
                 |              |              |
               manual         rules          adaptive
                                |              |
                           lifecycle      recency / ML
```

OpenS3 ВКР находится прежде всего в нижней части этой схемы:

```text
Object storage platform
        |
collect telemetry
        |
predict future demand
        |
decision engine
        |
recommend placement
        |
administrator confirms
        |
safe migration
```

Главная исследовательская ценность не в создании «ещё одного S3», а в **воспроизводимой оценке predictive placement policy поверх собственного S3-compatible storage**.

---

# 25. Основные выводы для ВКР

1. **Не отождествлять HOT/COLD с SSD/HDD.** Это лишь возможная реализация классов в экспериментальном стенде.
2. **Не отождествлять S3 compatibility с полной реализацией AWS S3.** У Garage, R2, B2 и других систем разное покрытие API.
3. **Разделять API semantics и внутреннюю архитектуру.** AWS — эталон semantics, Ceph/Ozone/SeaweedFS — более полезные архитектурные аналоги.
4. **Metadata и payload имеют разные workload-профили.** Многие зрелые системы физически и логически разделяют их.
5. **Lifecycle и intelligent tiering — разные классы решений.** Static rule-based, reactive access-aware и predictive подходы нужно анализировать отдельно.
6. **ML tiering уже исследовался.** Новизна OpenS3 должна быть в конкретной постановке decision engine, интеграции, объяснимых рекомендациях и экспериментальном определении условий, где ML полезен.
7. **Baseline должен быть сильным.** Минимум: age-based, recency-based и frequency-based policies; особенно важен AWS Intelligent-Tiering-like recency baseline.
8. **Оценивать нужно систему, а не только модель.** Нужны storage-level метрики, migration cost/load и поведение при ошибочном placement.
9. **Ceph, Ozone и SeaweedFS стоит читать глубже всего** именно ради архитектуры metadata/data/placement.
10. **RustFS нужно рассматривать как важный текущий тренд, но отдельно отмечать уровень зрелости.**

---

# 26. Куда это пойдёт в дипломе

Для исследовательского раздела разумная структура может быть такой:

1. Классификация систем объектного хранения по deployment model.
2. S3 API как интерфейс, а не архитектура хранения.
3. Классификация metadata/data plane архитектур.
4. Подходы к защите данных: replication и erasure coding.
5. Понятие storage class и его разные реализации.
6. Lifecycle, reactive tiering и predictive tiering.
7. Детальный анализ AWS S3, Ceph RGW, MinIO/AIStor, SeaweedFS, Garage, RustFS и Apache Ozone.
8. Сравнительная таблица аналогов.
9. Выводы и позиционирование OpenS3.

Такой подход лучше каталога «продукт → список фич», потому что позволяет сначала построить **классификацию решений**, а затем показать конкретные системы как представителей этих классов.