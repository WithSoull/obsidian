## Основные типы
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Synchronous Replication|Synchronous replication]] — запись подтверждается только после того, как данные сохранены на всех репликах; обеспечивает высокую консистентность, но увеличивает задержки.  
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Asynchronous Replication|Asynchronous replication]] — лидер не ждёт подтверждения от реплик; повышает производительность, но может приводить к потере данных при сбоях.  
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Semi-Synchronous Replication|Semi-synchronous replication]] — компромисс: лидер ждёт как минимум одного (настравивается) подтверждения от реплики перед подтверждением клиенту.  
- [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/1 - Types of Replication/Chain-Based Replication|Chain-based replication]] — данные распространяются по цепочке узлов; снижает нагрузку на лидера, но добавляет сложность в маршрутизации и обработке отказов.

## Вопросы для проработки
- Какие trade-offs существуют между синхронной и асинхронной репликацией?
- Как задержка сети и географическое распределение влияет на выбор способа репликации?
- Какие стратегии применяются для минимизации рисков потери данных в асинхронных системах?
- Когда оправдано использование цепочечной (chain-based) архитектуры репликации?
- Как выбор вида репликации влияет на целостность, доступность и скорость системы?
