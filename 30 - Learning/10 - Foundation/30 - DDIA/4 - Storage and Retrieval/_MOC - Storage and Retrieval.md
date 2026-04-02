>[!quote] If you keep things tidily ordered, you’re just too lazy to go searching.

## Главная задача
Две главная задачи базы данных:
1) Хранить данные
2) Возвращать данные

Важно понимать как устроен движок базки чтобы, выбрать подходящий для своего workload или в случае чего можно было подтюнить его.

Для начала посмотрим как устроена самая примитивный движок, затем будем добавлять все больше и больше фич - [[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/01 - Simple DB Implementation/Building a Simple Database|Simple database implementation]].

## Структуры данных, которые лежат под капотом
Так называемые [[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/Indexes in Databases|Индексы в базах данных]], котоыре ускоряют чтение, но замедляют запись, могут содержать в себе разные структуры данных.

## Какие бывают нагрузки?
У нас бывает [[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/03 - OLAP/OLTP vs OLAP|два вида нагрузки]]:
1) OLAP - аналитика
2) OLTP - транзакции