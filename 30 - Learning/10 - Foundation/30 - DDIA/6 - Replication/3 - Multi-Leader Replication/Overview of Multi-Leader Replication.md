# TL;DR
У *single-leader* репликации есть один существенный недостаток - **у нас всего один лидер**. И это может стать узким горлышком в нашей системе, потому что если вы по какой-то причине не можете подлкючиться к мастеру, вы не можете писать в базу.

*Multi-leader* репликация в свою очередь имеет нескольких мастеров, она также еще называется *master - master* или *active/active* репликация. **В таком сетапе каждый мастер явлется репликой для других реплик.**

>[!question] А какая связь между ДЦ для *single* и *multi-based* стратегии реплицирования?
>Как правило:
>- ***single-leader*** между ДЦ у нас ***синхронная*** связь.
>  ```
>Датацентр A (лидер)
>           ↓ синхронно
>    [ИНТЕРНЕТ] ← точка отказа!
>           ↓
>Датацентр B (раб)
> ```
> - ***multi-leader*** между ДЦ ***асинхронная*** связь.
> ```
> Датацентр A (лидер)
>        ↓ асинхронно (не ждет!)
>[ИНТЕРНЕТ] ← сбой не блокирует запись
>        ↓
>Датацентр B (тоже лидер)
> ```
### Что стоит почитать про **Multi-Leader** репликацию?
1) [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/3 - Multi-Leader Replication/Single-Leader vs Multi-Leader Replication|Single VS Multi leader replication]]
2) Use Cases for Multi-Leader Replication:
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/3 - Multi-Leader Replication/Use Cases for Multi-Leader Replication: Offline Clients|Clients with offline operations]]
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/3 - Multi-Leader Replication/Use Cases for Multi-Leader Replication: Collaborative Editing|Collaborative editing]]
3) [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/3 - Multi-Leader Replication/Handling Write Conflicts|Handling Write Conflicts]]
4) [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/3 - Multi-Leader Replication/Multi-Leader Replication Topologies|Multi-Leader Replications Topologies]]

## Стоит ли игра свеч?
**Multi-leader** - это достаточно редкий кейс в рамках одного ДЦ, потому что бенифиты зачастаю не стоят этой излишней сложности в логике реплицирования. Но все же иногда игра стоит свеч.

>[!info] Какие есть реализации *multi-leader* сетапов?
>Вообще некоторые базки это поддерживают из коробки, но также зачастую есть реализации у внешних тулов:
>- Tungsten Replicator for MySQL
>- BDR for PostgreSQL 
>- GoldenGate for Oracle


Если для мулти-ДЦ взять *single-leader* реплицирование с одним мастером, то этот один мастер будет сидеть в одном определенном ДЦ. А значит все записи полетят через этот ДЦ.
А можно взять и посадить в каждый ДЦ своего лидера. Внутри каждого ДЦ будет обычная *single-leader* стратегия реплицирования. А вот между ДЦ каждый мастер будет реплицировать в мастеры других ДЦ.

![[99 - Meta/02 - Медиа/Pasted image 20251112224534.png]]

### Какие недостатки у *multi-leader* сетапа?
У нас конечно есть сильные преимущества, но есть и большие недостатки:
- Проблемы с конкурентным обновлением данных в двух разных ДЦ, и эти конфликты решаются отдельным компонентном *conflict resolution*, который есть на картинке. Вот тут более подробно будет про все это дело рассказано: [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/3 - Multi-Leader Replication/Handling Write Conflicts|Handling Write Conflicts]]
- Огромное количество подводных камней в конфигурировании всего этого дела, очень много конфликтов с привычными фичами базок: 
	- автоинкремент
	- триггеры
	- integrity constrains - это набор правил и условий, которые автоматически применяются к данным в базе данных для гарантии их точности, консистентности и надежности. Примеры: PK, FK, Unique, Not Null, Check (field > 0)
	
**Именно поэтому все стараются избегать *multi-leader* сетапа.**
