# Контекст
Это аудит ветки `5 - Replication` против свежей главы 6 `Replication` из DDIA.

Цель заметки:
- Зафиксировать пробелы и спорные места до следующего перечитывания главы
- Не смешивать результаты аудита с правками основных учебных заметок
- Вернуться к списку позже и осознанно решить, что именно исправлять

---

# Что уже покрыто хорошо
## Single-Leader Replication
- Есть базовая модель `leader/follower`
- Есть поднятие новых реплик
- Есть failover и проблемы при отказе лидера
- Есть реализации replication logs

## Replication Lag
- Есть основная идея eventual consistency
- Есть 3 аномалии:
  - `Reading Your Own Writes`
  - `Monotonic Reads`
  - `Consistent Prefix Reads`
- Есть отдельная заметка про solutions

## Multi-Leader Replication
- Есть обзор модели
- Есть use cases для offline clients и collaborative editing
- Есть topologies
- Есть handling write conflicts

## Leaderless Replication
- Есть `W/R/N` и quorum
- Есть `sloppy quorum` и `hinted handoff`
- Есть `monitoring staleness`
- Есть `detecting concurrent writes`
- Есть multi-datacenter section

---

# Фактические или спорные места
## 1. Single-leader между датацентрами описан слишком категорично
Проблемные заметки:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/3 - Multi-Leader Replication/Overview of Multi-Leader Replication|Overview of Multi-Leader Replication]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/3 - Multi-Leader Replication/Single-Leader vs Multi-Leader Replication|Single-Leader vs Multi-Leader Replication]]

Проблема:
- Сейчас там звучит мысль, что `single-leader` между ДЦ "как правило синхронный"
- В главе DDIA акцент другой: все записи должны идти в регион лидера, поэтому межрегиональная сеть влияет на write path
- Это не то же самое, что "single-leader = обязательно sync между регионами"

Что проверить при перечитывании:
- Как именно книга формулирует проблему write latency в `single-leader`
- Где заканчивается конкретный deployment choice и начинается общий принцип

## 2. Синхронная репликация описана как ожидание всех реплик
Проблемная заметка:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Synchronous Replication|Synchronous Replication]]

Проблема:
- Сейчас заметка фактически приравнивает sync replication к ожиданию `всех` реплик
- В DDIA важна практическая картина: часто одна реплика synchronous, остальные asynchronous
- Иначе теряется разница между fully synchronous и semi-synchronous практикой

Что проверить:
- Какие именно варианты книга относит к synchronous и semisynchronous
- Что именно лидер ждёт перед `OK`

## 3. Semi-synchronous note сейчас противоречива
Проблемная заметка:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Semi-Synchronous Replication|Semi-Synchronous Replication]]

Проблема:
- В одном месте всё объяснено нормально: ждём одну реплику
- Ниже написано, что "все 3 реплики синхронные", но затем снова говорится, что ждём только одну, а остальные async
- Это ломает модель в голове

Что проверить:
- Нужна ли тут одна чистая формулировка без двусмысленности

## 4. Кворум описан как слишком сильная гарантия
Проблемные заметки:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/4 - Leaderless Replication/How Quorum Works|How Quorum Works]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/4 - Leaderless Replication/Limitations of Quorum Consistency|Limitations of Quorum Consistency]]

Проблема:
- В `How Quorum Works` формула `W + R > N` подана почти как абсолютная гарантия свежего чтения
- Но следующая заметка уже объясняет, почему это не абсолютная гарантия
- В DDIA это скорее полезная эвристика с рядом важных caveats

Что проверить:
- Как лучше переформулировать: "обычно позволяет", "ожидаем пересечение", "не гарантирует linearizable reads"

## 5. В сравнении single-leader и multi-leader выпал axis consistency
Проблемная заметка:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/3 - Multi-Leader Replication/Single-Leader vs Multi-Leader Replication|Single-Leader vs Multi-Leader Replication]]

Проблема:
- Есть comparison по:
  - latency
  - outage tolerance
  - network problems
- Но нет отдельного пункта про consistency
- А в книге это один из ключевых trade-off: multi-leader хуже подходит там, где нужно жестко enforce-ить глобальные constraints

Что проверить:
- Примеры из главы: uniqueness, non-negative balance, global constraints

## 6. Решение read-your-writes местами сведено к эвристике "подождать минуту"
Проблемная заметка:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/2 - Replication Lag/Reading Your Own Writes|Reading Your Own Writes]]

Проблема:
- В книге важен causal marker: timestamp или log position, до которого replica должна догнаться
- В заметке это частично есть, но упор местами смещён в сторону тайм-окна "подождать минуту"
- Так можно упростить модель слишком сильно

Что проверить:
- Где книга предлагает heuristic
- Где предлагает именно проверку up-to-date replica

## 7. Solutions for Replication Lag пока слишком короткая
Проблемная заметка:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/2 - Replication Lag/Solutions for Replication Lag|Solutions for Replication Lag]]

Проблема:
- Сейчас заметка обрывается почти на общем рассуждении
- Из главы пропущен важный мостик:
  - application-level workarounds сложны
  - strong consistency + transactions упрощают programming model
  - NewSQL в новой редакции главы явно упомянут как ответ на старый тезис "eventual consistency неизбежна"

Что проверить:
- Насколько глубоко хочется тащить сюда NewSQL и contrast with NoSQL

---

# Темы, которых сейчас не хватает
## 1. Backups and Replication
В свежей главе есть отдельный подблок про разницу между replication и backups:
- replication не заменяет backup
- replication быстро переносит и полезные, и ошибочные изменения
- backup нужен, чтобы "вернуться во времени"

Сейчас в ветке отдельной заметки под это нет.

## 2. Sync Engines and Local-First Software
Это один из самых заметных новых блоков главы.

Сейчас в ветке есть:
- offline clients
- collaborative editing

Но нет отдельной сборки про:
- `sync engine`
- `offline-first`
- `local-first`
- почему это всё архитектурно multi-leader

## 3. Pros and Cons of Sync Engines
В книге это отдельный полезный практический кусок:
- быстрый локальный UI
- работа офлайн
- более декларативная модель для frontend
- реактивные обновления
- но плохая применимость к очень большим объёмам данных

Сейчас этого отдельным узлом нет.

## 4. Single-Leader Versus Leaderless Replication Performance
В оглавлении главы это отдельный раздел.

Сейчас в ветке нет отдельной заметки, где были бы собраны trade-offs:
- latency
- consistency expectations
- durability path
- поведение при network interruptions

## 5. Summary по всей главе
Сейчас summary главы размазан по дочерним заметкам, но нет отдельной завершающей note:
- когда брать single-leader
- когда нужен multi-leader
- когда leaderless действительно оправдан
- какие гарантии ослабевают при каждом выборе

---

# Что выходит за рамки главы, но полезно
Это не проблема, а наблюдение.

Ветка содержит материал, который шире самой главы DDIA:
- `Chain-Based Replication`
- `CRDT`
- `Operational Transformation`
- `Mergeable Persistent Data Structures`

Это хорошие расширения. Их не обязательно убирать.
Но при следующем проходе можно отделить:
- что относится именно к канону главы
- что является дополнительным углублением

---

# Приоритет на следующий проход
## Сначала исправить фактические формулировки
1. `single-leader` vs `multi-leader` между регионами
2. `synchronous` vs `semi-synchronous`
3. слишком сильную трактовку quorum guarantees

## Затем добавить реально отсутствующие темы
1. `Backups and Replication`
2. `Sync Engines and Local-First Software`
3. `Pros and Cons of Sync Engines`
4. `Single-Leader Versus Leaderless Replication Performance`

## После этого улучшить обзорные MOC
Особенно:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/_MOC - Replication|_MOC - Replication]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/3 - Multi-Leader Replication/_MOC - Multi-Leader Replication|_MOC - Multi-Leader Replication]]

---

# Вопросы к себе после повторного чтения главы
- Какие идеи из новой главы действительно хочется встроить в постоянные заметки, а какие достаточно оставить на уровне awareness?
- Нужно ли держать отдельный note про `NewSQL` в контексте replication lag, или это уже лучше связывать с главами про transactions/consistency?
- Хочется ли собрать одну meta-note `Choosing a Replication Strategy`, или лучше оставить сравнения распределёнными по веткам?
