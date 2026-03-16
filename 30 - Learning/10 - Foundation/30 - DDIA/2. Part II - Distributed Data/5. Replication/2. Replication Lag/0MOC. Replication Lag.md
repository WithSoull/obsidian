## Обзор
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/Implementation of Replication Logs|Implementation of Replication Logs]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/Проблемы с Replication Lag|Проблемы с Replication Lag]]
## Последовательность чтения и согласованность
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/Consistent Prefix Reades|Consistent Prefix Reades]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/Monotonic Reads|Monotonic Reads]]
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/Reading your own writes|Reading your own writes]]
## Методы и решения
- [[30 - Learning/10 - Foundation/30 - DDIA/2. Part II - Distributed Data/5. Replication/2. Replication Lag/Solutions for replication lag|Solutions for replication lag]]
## Вопросы для проработки
- Что такое replication lag и какие основные причины его возникновения?
- Как задержка репликации влияет на консистентность данных?
- Чем различаются модели:
  - Reading your own writes
  - Monotonic reads
  - Consistent prefix reads?
- Какие практические подходы используются для минимизации lag при репликации между датацентрами?
- Как архитектура репликации (single-leader vs multi-leader) влияет на задержку?