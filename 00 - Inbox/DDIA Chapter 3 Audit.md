# DDIA Chapter 3 Audit

Аудит ветки `3 - Data Models and Query Languages` против `2.0 DDIA-original.pdf`.

Проверены:
- `00 - Overview/_MOC - Data Models and Query Languages`
- `01 - Data Models/01 - Relational/SQL`
- `01 - Data Models/02 - Document/*`
- `01 - Data Models/03 - Graph/*`
- `02 - Query Languages/*`
- `03 - Concepts and Performance/*`

## Итог по главе

Ветка уже покрывает значимую часть главы 3, но покрытие **неровное**:
- тема **document vs relational** покрыта широко, но местами с опасными упрощениями;
- тема **graph models / Cypher / SPARQL / Datalog** покрыта, но несколько заметок ушли в внешние детали, которые не помогают восстановить именно DDIA-модель;
- несколько важных блоков главы **вообще отсутствуют** как отдельные заметки: **stars/snowflakes**, **GraphQL**, **event sourcing + CQRS**, **DataFrames**;
- часть заметок смешивает:
  - точный тезис из DDIA,
  - личное обобщение,
  - и внешние современные сведения без явной границы.

Главный риск этой ветки сейчас не в том, что она "недостаточно полная", а в том, что отдельные формулировки могут закрепить **не ту инженерную модель**.

## Критичные фактические проблемы

### 1. Перепутаны `schema-on-read` и `schema-on-write`
Файл: `01 - Data Models/02 - Document/Schema On-Read vs On-Write.md`

Сейчас написано:
> "В случае document модели у нас есть схема на запись **schema-on-read**"

Это фактическая ошибка. Должно быть наоборот:
- **schema-on-read**: структура интерпретируется при чтении;
- **schema-on-write**: структура проверяется при записи.

Это один из центральных тезисов раздела `Schema flexibility in the document model`, поэтому ошибка высокоприоритетная.

### 2. Документная модель описана так, будто она хорошо подходит для `many-to-one`
Файл: `00 - Overview/_MOC - Data Models and Query Languages.md`

Сейчас в MOC есть формулировка, что document model хорошо подходит для `One-To-One` и несложных `Many-To-One`.

В DDIA акцент другой:
- document model естественна прежде всего для **tree-structured / one-to-many** данных;
- **many-to-one** и особенно **many-to-many** как раз тянут систему обратно к ссылкам, индексам и join-подобным операциям.

Именно это ограничение DDIA подчеркивает на стр. 75-76.

### 3. Формулировка "у MongoDB нет JOIN" уже вводит в заблуждение
Файл: `01 - Data Models/02 - Document/Document Data Model.md`

Сейчас там сказано примерно: joins либо нет (`MongoDB`), либо поддержка слабая.

Для ветки DDIA лучше формулировать так:
- исторически document DB ассоциировались со **слабой поддержкой joins**;
- многие document DB позже добавили join-подобные возможности;
- тезис DDIA не в "join невозможен", а в том, что **нормализация в document model менее удобна**.

Иначе заметка закрепляет устаревшее бинарное правило вместо trade-off.

### 4. В `SQL.md` impedance mismatch подан как "проблема уже решена"
Файл: `01 - Data Models/01 - Relational/SQL.md`

Формулировка:
> "У SQL есть серьезная проблема, но ее вполне можно уже считать решенной"

Это сильное и спорное утверждение, которого в DDIA нет. Более точная мысль:
- mismatch реален;
- ORM уменьшают boilerplate;
- но ORMs не устраняют различие моделей и сами создают ограничения, включая `N+1`.

Для DDIA это важно, потому что chapter не объявляет победителя, а раскладывает компромиссы.

### 5. Объяснение первого правила в `Datalog.md` некорректно
Файл: `02 - Query Languages/Datalog.md`

Сейчас rule 1 объясняется так, будто `predicate = Name` и будто правило ищет связь `subject -> object`.

Но в DDIA:
- `within_recursive(LocID, PlaceName) :- location(LocID, PlaceName, _)`
- это просто правило, которое говорит: *любой location уже входит в within_recursive со своим именем*;
- рекурсия появляется только во втором правиле через `within(...)`.

Сейчас объяснение ломает саму идею пошагового вывода virtual tables.

## Сильные, но опасные упрощения

### `Graph Data Model.md`
Полезная заметка, но есть два перегиба:
- "любые две вершины можно соединить" звучит слишком абсолютно; идея DDIA в **гибкости модели по сравнению с CODASYL**, а не в полном отсутствии ограничений в любой реализации;
- таблица `CODASYL vs Graph DB` местами слишком категорична по сложности разработки.

### `Data Locality.md`
Мысль верная, но заметка слишком короткая и теряет главный trade-off:
- locality помогает, если читаешь **большую часть документа целиком**;
- при частичных чтениях и частых мелких апдейтах locality может обернуться переписыванием всего документа.

### `MapReduce.md`
Заметка полезная, но сильно шире материала главы и заканчивается лозунгом:
> "NoSQL заново изобрел SQL"

Это эффектно, но упрощает мысль DDIA. Лучше фиксировать:
- MapReduce проигрывает декларативным языкам в оптимизации и удобстве;
- document DB со временем действительно добавляли более декларативные query-механизмы.

## Заметки, которые ушли слишком далеко от DDIA

### `Semantic Web & RDF.md`
Тут много внешних утверждений про `2024-2025`, индустрии, adoption и современный рынок.

Проблема не обязательно в ложности, а в том, что для ветки DDIA это:
- слабо связано с учебной задачей главы;
- не отделено от материала книги;
- быстро устаревает;
- перегружает восстановление базовой модели.

### `Triple-Store Model.md`
Заметка полезна как расширение, но сейчас в ней слишком много внешнего:
- таблицы по продуктам;
- цифры по масштабируемости;
- benchmark-подобные сравнения;
- рекомендации по выбору технологий.

Для DDIA-ветки это лучше держать отдельно от базовой заметки про **triple store model**.

## Что в главе покрыто слабо или отсутствует

### Почти отсутствует как отдельный блок
- **Stars and Snowflakes: Schemas for Analytics**
- **GraphQL**
- **Event Sourcing and CQRS**
- **DataFrames, Matrices, and Arrays**

### Покрыто фрагментарно
- `When to Use Which Model`
- `Convergence of document and relational databases`
- `Query languages for documents`
- `Trade-offs of normalization`
- кейс про social timelines и selective denormalization

## Что перечитать в книге

Ниже список не "на всякий случай", а именно тех страниц/подразделов, которые дадут максимальный возврат для выравнивания ветки.

### Приоритет 1
- **pp. 80-82**: `When to Use Which Model` и `Schema flexibility in the document model`
  - зачем: здесь исправляется путаница вокруг `schema-on-read`, heterogeneous data и границ document model.
- **pp. 82-84**: `Data locality for reads and writes`, `Query languages for documents`, `Convergence of document and relational databases`
  - зачем: здесь DDIA аккуратно формулирует trade-off, а не лозунг "documents быстрее / SQL медленнее".
- **pp. 75-76**: `Many-to-One and Many-to-Many Relationships`
  - зачем: это ключевой участок, где видно, почему document model начинает буксовать на ссылках и индексах.
- **pp. 96-98**: `Datalog: Recursive Relational Queries`
  - зачем: надо заново собрать модель virtual tables, rules и recursion.

### Приоритет 2
- **pp. 77-79**: `Stars and Snowflakes: Schemas for Analytics`
  - зачем: это отдельный важный кусок главы, а в ветке его практически нет.
- **pp. 98-100**: `GraphQL`
  - зачем: раздел совсем отсутствует, хотя он хорошо дополняет тему "graph-like response shape vs underlying storage".
- **pp. 101-104**: `Event Sourcing and CQRS`
  - зачем: раздел отсутствует полностью, хотя это один из самых ценных концептуальных блоков главы.
- **pp. 105-106**: `DataFrames, Matrices, and Arrays`
  - зачем: раздел короткий, но закрывает важный выход главы за пределы OLTP-моделей.

### Приоритет 3
- **pp. 72-74**: `Normalization, Denormalization, and Joins` + `Trade-offs of normalization`
  - зачем: чтобы точнее формулировать write/read trade-offs и не сводить все к "joins плохо".
- **pp. 74-75**: `Denormalization in the social networking case study`
  - зачем: очень полезный anti-simplification пример, почему денормализуют не всё подряд.
- **pp. 92-96**: `Triple Stores and SPARQL`, `The RDF data model`, `The SPARQL query language`
  - зачем: чтобы отделить базовую модель DDIA от внешних vendor/details.

## Короткий план доработки ветки

1. Сначала исправить фактические ошибки:
   - `Schema On-Read vs On-Write`
   - кусок про `many-to-one` в MOC
   - объяснение `Datalog`
   - формулировку про ORM в `SQL.md`
2. Затем сжать или вынести внешние расширения из:
   - `Semantic Web & RDF`
   - `Triple-Store Model`
3. Потом добавить недостающие заметки:
   - `Stars and Snowflakes`
   - `GraphQL`
   - `Event Sourcing and CQRS`
   - `DataFrames, Matrices, and Arrays`

## Быстрый чек-лист чтения

- [ ] стр. 75-76: `Many-to-One and Many-to-Many Relationships`
- [ ] стр. 77-79: `Stars and Snowflakes: Schemas for Analytics`
- [ ] стр. 80-82: `When to Use Which Model` + `Schema flexibility in the document model`
- [ ] стр. 82-84: `Data locality for reads and writes` + `Query languages for documents` + `Convergence of document and relational databases`
- [ ] стр. 96-98: `Datalog: Recursive Relational Queries`
- [ ] стр. 98-100: `GraphQL`
- [ ] стр. 101-104: `Event Sourcing and CQRS`
- [ ] стр. 105-106: `DataFrames, Matrices, and Arrays`
