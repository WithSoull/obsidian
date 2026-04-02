## Обзор
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/2 - Replication Lag/Implementation of Replication Logs|Implementation of Replication Logs]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/2 - Replication Lag/Problems with Replication Lag|Problems with Replication Lag]]
## Последовательность чтения и согласованность
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/2 - Replication Lag/Consistent Prefix Reads|Consistent Prefix Reads]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/2 - Replication Lag/Monotonic Reads|Monotonic Reads]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/2 - Replication Lag/Reading Your Own Writes|Reading your own writes]]
## Методы и решения
- [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/2 - Replication Lag/Solutions for Replication Lag|Solutions for replication lag]]
## Вопросы для проработки
- Что такое replication lag и какие основные причины его возникновения?
- Как задержка репликации влияет на консистентность данных?
- Чем различаются модели:
  - Reading your own writes
  - Monotonic reads
  - Consistent prefix reads?
- Какие практические подходы используются для минимизации lag при репликации между датацентрами?
- Как архитектура репликации (single-leader vs multi-leader) влияет на задержку?