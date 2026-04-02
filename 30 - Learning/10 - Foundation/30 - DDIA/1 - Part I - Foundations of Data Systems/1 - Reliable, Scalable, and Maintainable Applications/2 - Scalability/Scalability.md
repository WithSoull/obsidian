>[!danger] В общем и целом про масштабируемость
>Даже если сегодня система надежная, наступает день когда нагрузка увеличивается и системе нужно масштабироваться. 
>*Scalability* - означает способность системы справляться с увеличенной нагрузкой. Обсуждая эту тему полезно задумываться вопросами следующего характера:
>- Если система вырастет в некотором месте, как мы можем с этим справиться?
>- Как мы можем добавить вычислительной мощности чтобы справиться с повышенной нагрузкой?

## Как описывать scalability
### Как можно описать нагрузку?
Первым делом нужно лаконично описать текущую нагрузку на систему. Только после этого можно обсуждать вопросы роста.
- RPS
- Отношение записи к чтению в базках
- Количество одновременно активных пользователей
- Hit rate on a cache

Иногда достаточно среднего случая, а иногда нужно описывать нагрузку через экстремальные кейсы. Хороший пример  [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling|Twitter Scaling]].

## Как описывать performance под ростом
### Описание производительности
- Если я буду повышать нагрузку оставляя неизменными системные ресурсы, как это повлияет на производительность системы?
- Если я увеличу нагрузку, насколько надо увеличить системные ресурсы, чтобы производительность осталось неизменной?

Чтобы это обсуждать предметно, нужно зафиксировать:
- `throughput`;
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Response Time, Service Time, and Latency|response time / service time / latency]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Percentile|percentiles]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Service Level Objective|SLO]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Service Level Agreement|SLA]].

## Что мешает масштабироваться
### Подводные камни
Проблемы, который могут нам помешать:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Head-of-Line Blocking|HOL]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Tail Latency Amplification|Tail Latency Amplification]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Overload, Retry Storm, and Backpressure|retry storm и backpressure]].

## Подходы чтобы справиться с нагрузкой
`Scalability` в DDIA не означает "система уже большая". Это вопрос:
- как изменится производительность при росте нагрузки;
- сколько ресурсов надо добавить, чтобы удержать приемлемый уровень сервиса.

>[!important] Вариации масштабирования
>Люди разделяют масштабирование на две вариции горизонтальную и вертикальную. 
>- *Горизонтально* - про распределение нагрузки на много машинок
>- *Вертикально* - повышать производительность одной машинки

Как обычно лучшим вариантом как правило является сочетание обоих подходов, сохраняя при этом баланс. 
#### Автоматизация
Есть *гибкие системы* которые задействуют доп ресурсы при увеличении нагрузки. Это достаточно сложно, поэтому зачастую можно увидеть как этим заниматься человек.

## Итог
Единого рецепта нет. Сначала описываем нагрузку и целевые метрики, потом уже выбираем шардирование, кэширование, fan-out, очереди, вертикальное или горизонтальное масштабирование.
