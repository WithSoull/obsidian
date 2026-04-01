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

## Критичные замечания

### 1. Перепутана логика кейса про Twitter timeline

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling]] перепутан основной вывод кейса.

Как в DDIA:
- для обычных пользователей выгодно материализовать home timeline и делать `fan-out on write`;
- для celebrity-аккаунтов массовая запись в миллионы лент слишком дорогая, поэтому их посты часто обрабатываются отдельно и подмешиваются при чтении.

Сейчас в заметке записано наоборот. Это не просто огрубление, а инверсия идеи раздела.

### 2. Неверно определена `latency`

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability]] `latency` описана как время чистой обработки запроса без сети и очередей.

Это противоречит DDIA. В книге различаются:
- `response time` = все, что видит клиент;
- `service time` = время активной обработки;
- `queueing delay` = ожидание в очередях;
- `network latency` = сетевые задержки;
- `latency` = общий термин для времени, когда запрос не обрабатывается активно.

Тут нужен пересмотр формулировок, иначе начнет путаться весь словарь производительности.

### 3. `fault` и `failure` разведены слишком грубо

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Fault vs Failure]] написано:
- `fault` = сломался один компонент;
- `failure` = система целиком.

Это слишком грубо. В терминах DDIA:
- `fault` это дефект или отказ компонента;
- `failure` это ситуация, в которой система в целом перестает предоставлять пользователю требуемый сервис корректно.

`Failure` не требует полного падения всей системы.

### 4. `P999` подан как почти универсальная норма

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Percentile]] практический блок местами звучит слишком категорично:
- `P999` как основной полезный индикатор;
- `P9999` как бессмысленная или вредная метрика.

У DDIA утверждение уже:
- высокие percentiles важны;
- `p999` полезен в некоторых контекстах, например у Amazon;
- `p9999` для их задач оказался слишком дорогим относительно пользы.

Это контекстная инженерная эвристика, а не универсальный закон.

### 5. SLO/SLA сведены только к performance

В [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability]], [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Service Level Objective]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Service Level Agreement]] SLO/SLA описаны в основном как цели производительности.

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

Из этого в заметках есть куски, но цельного каркаса нет.

### 2. `Head-of-Line Blocking` объяснен нормально, но не доведен до общей модели

[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Head-of-Line Blocking]] передает интуицию, но слабо связан с:
- ограниченным параллелизмом;
- очередями;
- различием между `service time` и полной `response time`.

### 3. Раздел про людей в reliability местами теряет мысль книги

[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability]] полезно перечисляет rollback, тесты, monitoring и sandbox, но книга делает более точный акцент:
- не на персональной вине;
- а на `sociotechnical system`;
- на системных причинах ошибок;
- на `blameless postmortems`.

### 4. `Maintainability` покрыт верно, но слишком коротко

Ветки [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Operability]], [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Simplicity]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Evolvability]] держат правильную тройку, но не хватает нюанса:
- автоматизация не всегда улучшает operability;
- maintenance это не только код, но и организация;
- legacy возникает почти у любой успешной системы.

### 5. `WhatsApp Service Architecture` не помогает восстановить именно главу 2

[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/WhatsApp Service Architecture]] полезна как отдельная system design заметка, но как материал по главе 2 она скорее боковая и не закрывает пробелы по основным терминам.

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
