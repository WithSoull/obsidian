# Defining Nonfunctional Requirements Audit

Аудит сделан по главе 2 `Defining Nonfunctional Requirements` из [[30 - Learning/10 - Foundation/30 - DDIA/0 - Book PDFs/2.0 DDIA-original.pdf]].

Сравнивались заметки в папке:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/_MOC - Data-Intensive Applications]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Fault vs Failure]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Percentile]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Service Level Objective]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Service Level Agreement]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/SLO vs SLA]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Head-of-Line Blocking]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Tail latency amplification]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Maintainability]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Operability]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Simplicity]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Evolvability]]

## Общая оценка

По структуре глава покрыта правильно: есть отдельные ветки `Reliability`, `Scalability`, `Maintainability`.

Основные проблемы:
- есть несколько фактических ошибок в ключевых местах;
- почти выпал блок `Describing Performance`;
- часть заметок смешивает материал DDIA с более поздним production/SRE-контекстом без явной границы между ними.

Формат замечаний ниже:
- `Как у тебя` содержит прямую цитату из текущих заметок;
- `Как в DDIA` содержит точный пересказ позиции книги с указанием раздела и страниц.

Явные длинные дословные цитаты из книги не вставляю, чтобы не тащить в заметку куски текста DDIA; вместо этого даю максимально близкий пересказ с привязкой к разделу.

## Критичные замечания

### 1. Перепутана логика кейса про Twitter timeline

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling]] перепутан основной вывод кейса.

Как у тебя:
> Если пользоваться вторым подходом, один пост знаменитости будет стоить слишком дорого. Поэтому сейчас твиттер комбинирует оба этих подхода. Посты знаменитостей отдельно вписываются в ленты их подписчиков. А для обычных пользователей работает первый подход.

Как в DDIA:
- Раздел `Materializing and Updating Timelines`, стр. 35-36.
- Для большинства пользователей выгодно заранее поддерживать materialized home timeline и платить fan-out on write.
- Для celebrity-аккаунтов массовая запись в миллионы лент слишком дорогая, поэтому их посты разумно хранить отдельно и подмешивать при чтении.

Сейчас в заметке записано наоборот. Это не просто огрубление, а инверсия идеи раздела.

### 2. Неверно определена `latency`

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability]] `latency` описана как время чистой обработки запроса без сети и очередей.

Как у тебя:
> Latency (это время на чистую обработку запроса, без всяких сетевых задержек или очередей)

Как в DDIA:
- Раздел `Latency and Response Time`, стр. 38-39.
- `Response time` это полный путь, который видит клиент.
- `Service time` это время активной обработки запроса сервисом.
- `Queueing delay` и `network latency` не входят в service time, но входят в response time.
- `Latency` в этой части книги не равна "чистой обработке"; это более общий термин про время, когда запрос не обрабатывается активно.

Это противоречит DDIA. В книге различаются:
- `response time` = все, что видит клиент;
- `service time` = время активной обработки;
- `queueing delay` = ожидание в очередях;
- `network latency` = сетевые задержки;
- `latency` = общий термин для времени, когда запрос не обрабатывается активно.

Тут нужен пересмотр формулировок, иначе начнет путаться весь словарь производительности.

### 3. `fault` и `failure` разведены слишком грубо

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Fault vs Failure]] написано:

Как у тебя:
> *Fault* - когда из строя выходит один компонент, а *failure* - когда система целиком

Как в DDIA:
- Раздел `Reliability and Fault Tolerance`, стр. 43-44.
- `Fault` это ситуация, когда один компонент системы отклоняется от ожидаемого поведения.
- `Failure` это уже невыполнение системой в целом того сервиса, который ожидает пользователь.
- Failure может возникнуть и без полного "падения всей системы".

Это слишком грубо. В терминах DDIA:
- `fault` это дефект или отказ компонента;
- `failure` это ситуация, в которой система в целом перестает предоставлять пользователю требуемый сервис корректно.

`Failure` не требует полного падения всей системы.

### 4. `P999` подан как почти универсальная норма

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Percentile]] практический блок местами звучит слишком категорично:
- `P999` как основной полезный индикатор;
- `P9999` как бессмысленная или вредная метрика.

Как у тебя:
> P999 — отличный инструмент для наблюдения за качеством обслуживания
>
> Почему P9999 — бессмысленно (или вредно)

Как в DDIA:
- Разделы `Average, Median, and Percentiles` и `Use of Response Time Metrics`, стр. 40-42.
- Книга говорит, что высокие percentiles важны, потому что они отражают tail latencies и пользовательский опыт.
- Пример с Amazon иллюстрирует, почему `p999` может быть полезен в некоторых системах.
- Замечание про `p9999` относится к конкретному компромиссу стоимости и пользы, а не к универсальному запрету.

У DDIA утверждение уже:
- высокие percentiles важны;
- `p999` полезен в некоторых контекстах, например у Amazon;
- `p9999` для их задач оказался слишком дорогим относительно пользы.

Это контекстная инженерная эвристика, а не универсальный закон.

### 5. SLO/SLA сведены только к performance

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability]], [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Service Level Objective]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Service Level Agreement]] SLO/SLA описаны в основном как цели производительности.

Как у тебя:
> SLO - внутренняя цель производительности сервиса
>
> SLA - внешняя цель производительности сервиса перед клиентом

Как в DDIA:
- Раздел `Use of Response Time Metrics`, стр. 41-42.
- SLO и SLA используются для формализации ожидаемой производительности и доступности сервиса.
- DDIA приводит пример, где в SLO одновременно фигурируют и latency percentiles, и доля non-error responses.

В DDIA они привязаны и к производительности, и к доступности. Для главы это важная часть формулировки нефункциональных требований.

## Средние замечания и пробелы

### 1. Почти отсутствует блок `Describing Performance`

Это сейчас главный пробел ветки. По главе 2 там важные идеи:
- `response time` и `throughput` как два базовых типа метрик;
- связь throughput и response time через queueing;
- retry storm;
- metastable failure;
- backpressure и load shedding;
- мерить response time лучше на стороне клиента;
- percentiles важнее среднего для user-facing оценки.

Как у тебя:
> Важные цифры:
> - Пропуская способность (throughput)
> - Response time
> - Latency

Как в DDIA:
- Разделы `Describing Performance`, `When an Overloaded System Won’t Recover`, `Latency and Response Time`, `Average, Median, and Percentiles`, стр. 37-42.
- В этой части главы не просто словарь, а цельная модель поведения системы под нагрузкой: очереди, retries, metastability, load shedding, backpressure, client-side measurement.

Из этого в заметках есть куски, но цельного каркаса нет.

### 2. `Head-of-Line Blocking` объяснен нормально, но не доведен до общей модели

[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Head-of-Line Blocking]] передает интуицию, но слабо связан с:
- ограниченным параллелизмом;
- очередями;
- различием между `service time` и полной `response time`.

Как у тебя:
> первый запрос в очереди выполняется слишком долго
>
> долгие запросы тормозят даже те запросы, который должны быть быстрыми

Как в DDIA:
- Раздел `Latency and Response Time`, стр. 39.
- HOL blocking связывается с тем, что сервер может обрабатывать только ограниченное число вещей параллельно.
- Даже если последующие запросы сами по себе быстрые, клиент все равно видит высокую response time из-за ожидания.

### 3. Раздел про людей в reliability местами теряет мысль книги

[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability]] полезно перечисляет rollback, тесты, monitoring и sandbox, но книга делает более точный акцент:
- не на персональной вине;
- а на `sociotechnical system`;
- на системных причинах ошибок;
- на `blameless postmortems`.

Как у тебя:
> Все таки большинство ошибок происходит по вине кожанных мешков.

Как в DDIA:
- Раздел `Humans and Reliability`, стр. 47-48.
- Книга прямо спорит с редукцией проблемы к "human error".
- Ошибки людей рассматриваются как симптом проблем в sociotechnical system, а не как единственная причина инцидента.
- Отсюда акцент на blameless postmortems и организационное обучение.

### 4. `Maintainability` покрыт верно, но слишком коротко

Ветки [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Operability]], [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Simplicity]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Evolvability]] держат правильную тройку, но не хватает нюанса:
- автоматизация не всегда улучшает operability;
- maintenance это не только код, но и организация;
- legacy возникает почти у любой успешной системы.

Как у тебя:
> Хорошо известно, что поддержка ПО сильно дороже начальных затрат на его написание.
>
> Хороший operability подразумевает систему в которой легко выполняются рутинные задания

Как в DDIA:
- Разделы `Maintainability`, `Operability: Making Life Easy for Operations`, стр. 52-54.
- Книга отдельно подчеркивает, что автоматизация полезна, но она двусторонняя: крайние случаи все равно требуют сильной operations team.
- Также DDIA явно связывает maintenance с людьми, знаниями, legacy и устройством организации, а не только с качеством кода.

### 5. `WhatsApp Service Architecture` не помогает восстановить именно главу 2

[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/WhatsApp Service Architecture]] полезна как отдельная system design заметка, но как материал по главе 2 она скорее боковая и не закрывает пробелы по основным терминам.

Как у тебя:
> Нефункциональные требования:
> 1) Low latency
> 2) Consistency
> 3) Security
> 4) Scalability

Как в DDIA:
- Глава 2 строится не вокруг произвольного system design кейса, а вокруг конкретной рамки:
- performance metrics;
- reliability;
- scalability;
- maintainability.
- Поэтому заметка полезна как расширение, но не заменяет конспект самой главы.

## Что покрыто хорошо

- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability]] держит правильный каркас: hardware faults, software faults, human mistakes.
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Maintainability]] и дочерние заметки правильно отражают тройку `operability / simplicity / evolvability`.
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Percentile]] полезна practically, если ослабить слишком общие выводы и явно отделить их от текста книги.

## Что перечитать в книге

Обязательно перечитать в [[30 - Learning/10 - Foundation/30 - DDIA/0 - Book PDFs/2.0 DDIA-original.pdf]]:

### 1. Кейс про social network timeline

Стр. 34-36:
- `Case Study: Social Network Home Timelines`
- `Representing Users, Posts, and Follows`
- `Materializing and Updating Timelines`

Причина:
- сейчас именно здесь у тебя самая грубая фактическая ошибка в `Twitter Scaling`.

### 2. Весь блок про performance metrics

Стр. 37-42:
- `Describing Performance`
- `Latency and Response Time`
- `Average, Median, and Percentiles`
- `Use of Response Time Metrics`

Причина:
- это самый недоусвоенный кусок главы по текущим заметкам;
- отсюда нужно заново собрать словарь `throughput / response time / service time / latency / queueing / percentile / tail latency amplification`.

### 3. Весь reliability block

Стр. 43-48:
- `Reliability and Fault Tolerance`
- `Fault Tolerance`
- `Hardware and Software Faults`
- `Humans and Reliability`
- `How Important Is Reliability?`

Причина:
- нужно точнее восстановить `fault vs failure`;
- нужно перечитать human factors не как "люди ломают", а как `sociotechnical system`;
- полезно заново пройти pragmatic framing про то, когда reliability можно сознательно недоинвестировать.

### 4. Весь scalability block

Стр. 49-52:
- `Scalability`
- `Understanding Load`
- `Shared-Memory, Shared-Disk, and Shared-Nothing Architectures`
- `Principles for Scalability`

Причина:
- эти идеи у тебя пока либо очень сжаты, либо не вынесены в заметки;
- особенно важны load dimensions и сравнение vertical vs horizontal scaling.

### 5. Maintainability block

Стр. 52-55:
- `Maintainability`
- `Operability: Making Life Easy for Operations`
- `Simplicity: Managing Complexity`
- `Evolvability: Making Change Easy`

Причина:
- здесь меньше фактических ошибок, но ветка пока слишком короткая относительно важности раздела.

## Приоритет исправлений

Если править не все сразу, а в порядке отдачи, то приоритет такой:

1. Исправить [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling]].
2. Исправить определения в [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability]].
3. Исправить [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Fault vs Failure]].
4. Дособрать отдельную заметку или раздел про `Describing Performance`.
5. Потом уже шлифовать `Maintainability` и practical notes.
