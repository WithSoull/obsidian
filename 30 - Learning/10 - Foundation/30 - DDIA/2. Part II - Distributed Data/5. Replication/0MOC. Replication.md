>[!question] **Репликация** означает сохранение копии одинаковых данных на нескольких машинах, которые соеденины сетью.
>Это может понадобиться для:
>- Геораспределенности данных для умешьшения latency у пользователей
>- Улучшение доступности (abailability): система будет работать, даже если некоторые ее части упали
>- Увеличить число машин, которые могут обрабатывать читающее запросы. Это увеличит читающую пропускную способность
>- Позволить приложению работать в офлайн режиме (к примеру всякие cross-device календари)


## MAP OF CONTENT
1. **Общая топология реплицирования.** Вся сложность репликации заключается в обработке изменений данных, которые реплицируются. Существует 3 основных стратегии реплицирования
	1. [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/0. Single-leader/0MOC. Single-leader replication|single-leader (MOC)]]
	2. [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/3. Multi-Leader Replication/0MOC. Multi-Leader Replication|multi-leade (MOC)]]
	3. [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/4. Leaderless Replication/0MOC Leaderless Replication|leaderless (MOC)]]
2. [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/1. Types of Replication/0MOC. Types of Replication|Types of Replication (MOC)]]
3. [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/0MOC. Replication Lag|Replication Lag (MOC)]]