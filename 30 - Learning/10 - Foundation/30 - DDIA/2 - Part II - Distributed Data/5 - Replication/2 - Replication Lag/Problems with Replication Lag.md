### Предисловие
Первая причина реплицирования которую мы подробно рассмотрели - устойчивость к падению одной ноды. Но, конечно есть и другие причины:
- *scalability* - обрабатывать больше запросов, чем одна машинка может себе позволить 
- *latency* - хочется поставить реплику по ближе к пользователям, сделать геораспределенность

Leader-based стратегия реплицирования подразумевает, что все записи идут через одну ноду, а читать можно с любой. Если у нас большая нагрузка на чтение, есть привлекательная опция наклипать много реплик и распределить запросы между ними. Для этого нам в реальности не подходит [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Synchronous Replication|синхронная репликация]], потому что отказ одной ноды и мы в г...вне. Причем чем больше у нас нод будет, тем больше вероятность, что какая-то нода упадет.

### Replication Lag
С другой стороны, [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Asynchronous Replication|асинхронная репликация]] не гарантирует нам, актуальные данные. Да, если мы там перестанем условно писать и подождем изменения подтянуться. Такой эффект называется конечная согласованность - *eventual consistency*. И иногда "слегка" необновленные данные это нормально, например лайки на видосе на ютубе.

И вот это расхождение в данных, их несогласованность (неконсистентность) как раз таки и называется *replication lag*, как правило это доли секунд, но если железки пашут уже на пределе это время может так то и до парочки минут вырасти.

Когда у нас лаг вырастает, это уже серьезная проблема. Вот 3 примера таких проблем:
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/2 - Replication Lag/Reading Your Own Writes|Reading your own writes]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/2 - Replication Lag/Consistent Prefix Reads|Consistent Prefix Reads]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/2 - Replication Lag/Monotonic Reads|Monotonic Reads]]

Ну и заметка про решение конечно тоже имеется - [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/2 - Replication Lag/Solutions for Replication Lag|Solutions for replication lag]]