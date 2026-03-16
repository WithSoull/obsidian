Каждая нода, которая хранит *копию* базы и называется *репликой*. **Когда возникает несколько реплик как мы можем гарантировать, что данные окажутся на всех репликах?** Каждая запись должна быть обработана каждой репликой, самый популярный подход для решения этой проблемы - *leader-based replication*. 
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/0. Single-leader/Setting up New Replicas|Поднятие(наливка) новой реплики]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/0. Single-leader/Handling Node Outages|Обработка отказов реплик]]
###### leader-based replication
Одна нода назначается мастером (лидером). Все записи летят в лидер. Он отправляет изменения репликам, как *replication log* или *change stream*. А реплики должны  взять этот лог и обновить свои локальные копии данных (в том же порядке, в котором запросы и прилетели). Когда клиент хочет что-то прочитать, этот запрос может обработать любая нода.
![[99 - Meta/02 - Медиа/Pasted image 20251108080905.png]]
Такую схему используют многие базки как встроенная фича:
1) PostgreSQL (9.0 +)
2) MySQL
3) Oracle Data Guard
4) SQL Server's AlwaysOn Availability Groups
5) MongoDB
6) RethinkDB
7) Espresso
Более того такую схему используют еще и брокеры сообщений:
8) Kafka
9) RabbitMQ