### Исторический контекст
Это подход в котором вообще нет понятия мастера и репики, тут все ноды равны, можно читать с любой и писать в любую. Самые первые replicated data systems исопользовали именно такой подход. Он вновь набрал популярность, когда Amazon использовал его для своей *in-house **Dynamo** system*. После этого появились опенсорсные Riak, Cassandra и Voldemort вдохновленные Dynamo, и поэтому такой вид репликации стал называться *Dynamo-style*

>[!info] Необычная разновидность leaderless репликаций с координатором под капотом
>В некотрых реализациях leadless репликации клиенты шлют записи не во все ноды, а только в определенные, ноды-координаторы. Но в отличии от leader-base репликации, координатор не требует соблюдения порядка операций.

### Содержание
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/Writing to the Database When a Node Is Down|Writing to the Database When a Node Is Down]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/How Quorum Works|What is quorum and how does it work?]]
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/Limitations of Quorum Consistency|Limitations of Quorum Consistency]]
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/Sloppy Quorums and Hinted Handoff|Sloppy Quorums and Hinted Handoff]]
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/Monitoring Staleness|Monitoring Staleness]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/Multi-Datacenter Operations in Leaderless Replication|Multi-datacenter operations in leaderless replication]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/4 - Leaderless Replication/Detecting Concurrent Writes|Detecting Concurrent Writes]]
