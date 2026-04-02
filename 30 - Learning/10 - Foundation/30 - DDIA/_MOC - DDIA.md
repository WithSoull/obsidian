# DDIA

Это верхняя карта ветки по *Designing Data-Intensive Applications*.

Здесь лучше начинать не с дерева папок, а с ближайшей главы:
- если нужен общий контекст, сначала смотри [[public/30 - Learning/10 - Foundation/30 - DDIA/1 - Trade-Offs in Data Systems Architecture/_MOC - Trade-Offs in Data Systems Architecture|Trade-Offs in Data Systems Architecture]];
- если нужен словарь про **reliability / scalability / maintainability**, иди в [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/_MOC - Defining Nonfunctional Requirements|Defining Nonfunctional Requirements]];
- если нужен storage, encoding, replication или sharding, открывай соответствующую главу ниже.

## Chapters

### 1. [[public/30 - Learning/10 - Foundation/30 - DDIA/1 - Trade-Offs in Data Systems Architecture/_MOC - Trade-Offs in Data Systems Architecture|Trade-Offs in Data Systems Architecture]]
Вводная рамка про архитектурные trade-off'ы:
- single-node vs distributed;
- cloud vs self-hosting;
- OLTP vs OLAP;
- systems of record и derived data.

### 2. [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/_MOC - Defining Nonfunctional Requirements|Defining Nonfunctional Requirements]]
Глава про базовый язык system design:
- performance metrics;
- reliability;
- scalability;
- maintainability.

### 3. [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/00 - Overview/_MOC - Data Models and Query Languages|Data Models and Query Languages]]
Карта про модели данных и способ мышления запросами:
- relational, document, graph;
- declarative vs imperative queries;
- data locality и related trade-offs.

### 4. [[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/_MOC - Storage and Retrieval|Storage and Retrieval]]
База про внутренности хранилищ:
- append-only storage;
- hash indexes, B-trees, LSM-trees;
- OLTP vs OLAP и column-oriented storage.

### 5. [[public/30 - Learning/10 - Foundation/30 - DDIA/5 - Encoding and Evolution/_MOC - Encoding and Evolution|Encoding and Evolution]]
Глава про форматы данных и совместимость:
- schema evolution;
- Avro, Protobuf, Thrift;
- dataflow через базы, RPC и message passing.

### 6. [[public/30 - Learning/10 - Foundation/30 - DDIA/6 - Replication/_MOC - Replication|Replication]]
Карта про способы репликации и их trade-off'ы:
- single-leader;
- replication lag;
- multi-leader;
- leaderless replication.

### 7. [[public/30 - Learning/10 - Foundation/30 - DDIA/7 - Sharding/_MOC - Sharding|Sharding]]
Глава про partitioning:
- partitioning by key;
- secondary indexes;
- rebalancing;
- request routing;
- связь partitioning и replication.

### 8. Transactions
Папка [[public/30 - Learning/10 - Foundation/30 - DDIA/8 - Transactions|создана]], но содержимое пока не разложено.

### 9. The Trouble with Distributed Systems
Папка [[public/30 - Learning/10 - Foundation/30 - DDIA/9 - The Trouble with Distributed Systems|создана]], но содержимое пока не разложено.

### 10. [[public/30 - Learning/10 - Foundation/30 - DDIA/10 - Consistency and Consensus/Linearizability and Quorums|Consistency and Consensus]]
Пока заполнена частично:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/10 - Consistency and Consensus/Linearizability and Quorums|Linearizability and Quorums]];
- [[public/30 - Learning/10 - Foundation/30 - DDIA/10 - Consistency and Consensus/Consensus|Consensus]].

### 11. [[public/30 - Learning/10 - Foundation/30 - DDIA/11 - Batch Processing/Change Data Capture|Batch Processing]]
Пока в ветке есть только [[public/30 - Learning/10 - Foundation/30 - DDIA/11 - Batch Processing/Change Data Capture|Change Data Capture]].

### 12. Stream Processing
Папка [[public/30 - Learning/10 - Foundation/30 - DDIA/12 - Stream Processing|создана]], но содержимое пока не разложено.

### 13. A Philosophy of Streaming Systems
Папка [[public/30 - Learning/10 - Foundation/30 - DDIA/13 - A Philosophy of Streaming Systems|создана]], но содержимое пока не разложено.

### 14. Doing the Right Thing
Папка [[public/30 - Learning/10 - Foundation/30 - DDIA/14 - Doing the Right Thing|создана]], но содержимое пока не разложено.

## Source

- Канонический PDF: [[public/30 - Learning/10 - Foundation/30 - DDIA/0 - Book PDFs/2.0 DDIA-original.pdf|2.0 DDIA-original.pdf]]
- Рядом лежит [[public/30 - Learning/10 - Foundation/30 - DDIA/Why Distribute Data Across Machines|Why Distribute Data Across Machines]] как отдельная обзорная заметка про мотивы распределения.

## How To Use This Branch

- Для изучения иди по главам сверху вниз.
- Для точечного поиска открывай ближайший `_MOC - ...` внутри нужной главы.
- Если в главе папка уже есть, а заметок почти нет, это значит "тема ещё не разложена", а не "структура сломана".
