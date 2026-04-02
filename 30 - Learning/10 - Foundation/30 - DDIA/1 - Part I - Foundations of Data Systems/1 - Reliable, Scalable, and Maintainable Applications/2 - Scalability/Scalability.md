>[!danger] В общем и целом про масштабируемость
>Даже если сегодня система надежная, наступает день когда нагрузка увеличивается и системе нужно масштабироваться. 
>*Scalability* - означает способность системы справляться с увеличенной нагрузкой. Обсуждая эту тему полезно задумываться вопросами следующего характера:
>- Если система вырастет в некотором месте, как мы можем с этим справиться?
>- Как мы можем добавить вычислительной мощности чтобы справиться с повышенной нагрузкой?

## На что опирается scalability
Сначала нужно договориться о языке измерения системы, иначе разговор про масштабирование будет расплывчатым.

Все определения и эффекты под нагрузкой лежат в [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Measuring Performance|Measuring Performance]].

В этой заметке нас интересует не словарь метрик, а *что именно в системе растет* и *какими рычагами с этим работать*.

## Как описывать нагрузку
Первым делом нужно лаконично описать текущую нагрузку. Только после этого можно обсуждать рост.
- RPS
- Отношение записи к чтению в базках
- Количество одновременно активных пользователей
- Hit rate on a cache

Иногда достаточно среднего случая, а иногда нужно явно моделировать экстремальные кейсы. Хороший пример  [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling|Twitter Scaling]].

## Какие вопросы задает scalability
- Если я буду повышать нагрузку оставляя неизменными системные ресурсы, как это повлияет на производительность системы?
- Если я увеличу нагрузку, насколько надо увеличить системные ресурсы, чтобы производительность осталось неизменной?

Именно поэтому **scalability** всегда опирается на заранее описанные:
- нагрузку;
- целевые performance-метрики;
- допустимый уровень деградации.

Если нужно понять, *почему* под ростом система замедляется, смотри:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Response Time, Service Time, and Latency|Response Time, Service Time, and Latency]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Head-of-Line Blocking|Head-of-Line Blocking]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Tail Latency Amplification|Tail Latency Amplification]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Overload, Retry Storm, and Backpressure|Overload, Retry Storm, and Backpressure]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/SLO vs SLA|SLO vs SLA]].

## Подходы чтобы справиться с нагрузкой
**Scalability** в DDIA не означает "система уже большая". Это вопрос:
- как изменится производительность при росте нагрузки;
- сколько ресурсов надо добавить, чтобы удержать приемлемый уровень сервиса.

>[!important] Вариации масштабирования
>Люди разделяют масштабирование на две вариции горизонтальную и вертикальную. 
>- *Горизонтально* - про распределение нагрузки на много машинок
>- *Вертикально* - повышать производительность одной машинки

Как обычно лучшим вариантом как правило является сочетание обоих подходов, сохраняя при этом баланс.

## Что здесь важно помнить
- нет универсального рецепта масштабирования;
- разные типы нагрузки ломают систему по-разному;
- перед выбором техники нужно понять, *что именно* растет: чтения, записи, данные, конкуренция за ресурсы или fan-out.

## Итог
Сначала описываем нагрузку и целевые метрики в performance-ветке, потом уже выбираем шардирование, кэширование, fan-out, очереди, вертикальное или горизонтальное масштабирование.
