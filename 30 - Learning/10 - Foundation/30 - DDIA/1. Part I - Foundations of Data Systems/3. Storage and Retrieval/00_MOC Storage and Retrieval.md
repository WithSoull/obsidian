>[!quote] If you keep things tidily ordered, you’re just too lazy to go searching.

## Главная задача
Две главная задачи базы данных:
1) Хранить данные
2) Возвращать данные

Важно понимать как устроен движок базки чтобы, выбрать подходящий для своего workload или в случае чего можно было подтюнить его.

Для начала посмотрим как устроена самая примитивный движок, затем будем добавлять все больше и больше фич - [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/01. Simple DB Implementation/Simple database implementation|Simple database implementation]].

## Структуры данных, которые лежат под капотом
Так называемые [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/Индексы в базах данных|Индексы в базах данных]], котоыре ускоряют чтение, но замедляют запись, могут содержать в себе разные структуры данных.

## Какие бывают нагрузки?
У нас бывает [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/03. OLAP/OLTP vs OLAP|два вида нагрузки]]:
1) OLAP - аналитика
2) OLTP - транзакции