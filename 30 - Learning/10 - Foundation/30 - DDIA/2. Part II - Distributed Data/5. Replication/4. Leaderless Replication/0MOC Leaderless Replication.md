### Исторический контекст
Это подход в котором вообще нет понятия мастера и репики, тут все ноды равны, можно читать с любой и писать в любую. Самые первые replicated data systems исопользовали именно такой подход. Он вновь набрал популярность, когда Amazon использовал его для своей *in-house **Dynamo** system*. После этого появились опенсорсные Riak, Cassandra и Voldemort вдохновленные Dynamo, и поэтому такой вид репликации стал называться *Dynamo-style*

>[!info] Необычная разновидность leaderless репликаций с координатором под капотом
>В некотрых реализациях leadless репликации клиенты шлют записи не во все ноды, а только в определенные, ноды-координаторы. Но в отличии от leader-base репликации, координатор не требует соблюдения порядка операций.

### Содержание
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/Writing to the Database When a Node Is Down|Writing to the Database When a Node Is Down]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/What is quorum and how does it work?|What is quorum and how does it work?]]
	- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/Limitations of Quorum Consistency|Limitations of Quorum Consistency]]
	- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/Sloppy Quorums and Hinted Handoff|Sloppy Quorums and Hinted Handoff]]
	- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/Monitoring Staleness|Monitoring Staleness]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/Multi-datacenter operations in leaderless replication|Multi-datacenter operations in leaderless replication]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/Detecting Concurrent Writes|Detecting Concurrent Writes]]
