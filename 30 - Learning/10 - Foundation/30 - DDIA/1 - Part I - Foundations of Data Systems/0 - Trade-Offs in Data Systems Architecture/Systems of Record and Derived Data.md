# Systems of Record and Derived Data

## Что это
Эта рамка помогает понять, **где находится каноническая версия данных**, а где лежат только производные представления.

- **System of record** (`source of truth`) хранит **авторитетное** значение. Новый факт сначала записывается сюда.
- **Derived data system** получает данные **из другого источника** и перерабатывает их под чтение, поиск, аналитику или другой workload.

Важно: различие определяется **не типом базы**, а **ролью системы в приложении**. Один и тот же PostgreSQL может быть и `system of record`, и derived system в зависимости от того, откуда в него попадают данные.

## Примеры
- primary OLTP database пользователя или заказа обычно является `system of record`;
- cache, search index, materialized view, feature store, DWH, recommendation model обычно являются `derived data`;
- денормализованная read-модель в сервисе тоже derived data, даже если хранится в "нормальной" БД.

## Почему это важно
- Если данные в derived system потерялись, их обычно можно **пересобрать** из источника.
- Если расходятся значения между derived system и `system of record`, то истинным считается значение из `source of truth`.
- Такая модель помогает понять, **какие данные надо обновлять первыми**, а какие можно синхронизировать асинхронно.

## Практический смысл
Эта граница полезна при проектировании dataflow:
- сначала определить, **куда пишется исходный факт**;
- потом перечислить, какие derived representations нужны для чтения;
- отдельно продумать, **как обновления будут распространяться** в индексы, кеши, витрины и аналитические системы.

Если этого не сделать, архитектура быстро превращается в набор "равноправных" БД, где уже непонятно, где истина, а где удобная копия.

## Типичная ошибка
Считать, что cache, materialized view или аналитическая витрина содержат "те же самые данные", что и primary store.

На практике это **производные данные с другим SLA и другими инвариантами**:
- они могут обновляться с лагом;
- могут временно отставать;
- могут быть пересчитаны заново;
- часто оптимизированы под конкретный read pattern.

## Связанные заметки
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Operational Versus Analytical Systems|Operational Versus Analytical Systems]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/3 - Storage and Retrieval/03 - OLAP/Aggregation, Data Cubes & Materialized Views|Aggregation, Data Cubes & Materialized Views]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/2 - Dataflow/Dataflow via Databases|Dataflow via Databases]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Data Systems, Law, and Society|Data Systems, Law, and Society]]
