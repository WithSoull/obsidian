
## `buckets`

| Поле       | Тип         | Ограничения / Примечание |
| ---------- | ----------- | ------------------------ |
| id         | uuid        | PK                       |
| name       | text        | UNIQUE                   |
| owner_id   | uuid        |                          |
| created_at | timestamptz |                          |
## `objects`

> Логический объект = `(bucket + key)`

| Поле               | Тип         | Ограничения / Примечание       |
| ------------------ | ----------- | ------------------------------ |
| id                 | uuid        | PK                             |
| bucket_id          | uuid        | FK → buckets(id)               |
| key                | text        | нормализованный key            |
| current_version_id | uuid        | FK → object_versions(id), NULL |
| created_at         | timestamptz |                                |

**Ограничения:**
* UNIQUE `(bucket_id, key)`
## `object_versions`

> Неизменяемые версии объекта

| Поле           | Тип         | Ограничения / Примечание                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id             | uuid        | PK (version_id)                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| object_id      | uuid        | FK → objects(id)                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| version_number | bigint      | монотонный per object                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| status         | text        | enum: writing/failed/storing/deleting<br>writing -> объект в процессе записи, сейчас data plane его записывает<br>failed -> объект не удалось записать<br>storing -> объект был записан в data plane полностью<br>deleting -> по некоторым причинам (пользователь удалил версию файла) и мы можем ждать некоторое время перед физическим удалением.<br>Далее cron при соблюдении условий и таймаутов записывает версию в топик на удалении и наконец версия удаляется физически |
| size_bytes     | bigint      | NULL                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| content_type   | text        | Примеры: `application/pdf`, `image/png`, `text/plain; charset=utf-8`  `application/octet-stream` (дефолт). Берется из `Content-Type` в `http`                                                                                                                                                                                                                                                                                                                                   |
| created_at     | timestamptz |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| user_id        | uuid        | FK → users(id)                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

**Индексы:**
* `(object_id, created_at DESC)`

**UNIQUE:**
* `(object_id, version_number)`

**Принцип создания:**

Версия создаётся:
* либо на `InitiateMultipart` со статусом `creating`
* либо на `CompleteMultipart`

---

## `multipart_uploads`

> Сессии multipart-загрузки

| Поле              | Тип         | Ограничения / Примечание                              |            |           |         |         |
| ----------------- | ----------- | ----------------------------------------------------- | ---------- | --------- | ------- | ------- |
| upload_id         | uuid        | PK                                                    |            |           |         |         |
| object_id         | uuid        | FK → objects(id)                                      |            |           |         |         |
| target_version_id | uuid        | FK → object_versions(id) — версия, которая собирается |            |           |         |         |
| initiator_id      | uuid        | FK → users(id)                                        |            |           |         |         |
| part_size         | bigint      |                                                       |            |           |         |         |
| status            | text        | enum: uploading                                       | completing | completed | aborted | expired |
| created_at        | timestamptz |                                                       |            |           |         |         |
| expires_at        | timestamptz |                                                       |            |           |         |         |
| lock_token        | text        | опционально, для идемпотентности complete             |            |           |         |         |

---

## `upload_parts`

> Временные части во время загрузки

| Поле        | Тип         | Ограничения / Примечание          |
| ----------- | ----------- | --------------------------------- |
| upload_id   | uuid        | FK → multipart_uploads(upload_id) |
| part_number | int         | 1..N                              |
| blob_id     | uuid        | FK → blobs(blob_id)               |
| size_bytes  | bigint      |                                   |
| etag        | text        |                                   |
| created_at  | timestamptz |                                   |

**PK:**

* `(upload_id, part_number)`

**Индексы:**

* `(blob_id)` — для GC

---

## `version_parts`

> Финальный манифест версии

| Поле        | Тип    | Ограничения / Примечание |
| ----------- | ------ | ------------------------ |
| version_id  | uuid   | FK → object_versions(id) |
| part_number | int    |                          |
| blob_id     | uuid   | FK → blobs(blob_id)      |
| size_bytes  | bigint |                          |
| etag        | text   |                          |

**PK:**

* `(version_id, part_number)`

**Индексы:**

* `(blob_id)`

---

### Отличие `upload_parts` vs `version_parts`

| upload_parts                      | version_parts                 |
| --------------------------------- | ----------------------------- |
| Временные части                   | Закреплённые за версией       |
| Существуют только во время upload | Существуют до удаления версии |
| Используются для сборки           | Являются финальным манифестом |

---

## `blobs`

> Учёт физического контента

| Поле           | Тип         | Ограничения / Примечание                   |
| -------------- | ----------- | ------------------------------------------ |
| blob_id        | uuid        | PK                                         |
| state          | text        | enum: writing | ready | deleting | deleted |
| size_bytes     | bigint      | NULL                                       |
| sha256         | text        | NULL (опционально)                         |
| ref_count      | bigint      | default 0 (если делаете дедуп)             |
| created_at     | timestamptz |                                            |
| last_access_at | timestamptz | NULL (опционально)                         |

**Замечание по GC:**

Blob удаляется если:

* не используется ни в `upload_parts`
* ни в `version_parts`
* либо по `ref_count = 0` (если используется подсчёт ссылок)

---

## `gc_queue`

> Queue на удаление blob

| Поле       | Тип         | Ограничения / Примечание |
| ---------- | ----------- | ------------------------ |
| id         | bigserial   | PK                       |
| blob_id    | uuid        |                          |
| not_before | timestamptz | индексируется            |
| reason     | text        |                          |
| created_at | timestamptz |                          |

**Индексы:**

* `(not_before)`

