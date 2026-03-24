# Trade-Offs in Data Systems Architecture

Вводная глава DDIA про рамку, в которой дальше рассматриваются системы данных: архитектура зависит не только от throughput, latency и стоимости, но и от того, кто эксплуатирует систему, как меняется нагрузка, и какие legal/social constraints накладываются на хранение данных.

## Основные trade-offs
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Operational Versus Analytical Systems|Operational Versus Analytical Systems]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Cloud Versus Self-Hosting|Cloud Versus Self-Hosting]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Distributed Versus Single-Node Systems|Distributed Versus Single-Node Systems]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Data Systems, Law, and Society|Data Systems, Law, and Society]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Systems of Record and Derived Data|Systems of Record and Derived Data]]

## Как читать эту главу
- `Operational Versus Analytical Systems` задаёт базовое разделение между OLTP, OLAP, DWH и data lake.
- `Cloud Versus Self-Hosting` объясняет, когда выгодно брать managed services, а когда нужен собственный контроль над системой.
- `Distributed Versus Single-Node Systems` напоминает, что распределённость нужна не всегда и сама по себе создаёт новые failure modes.
- `Data Systems, Law, and Society` добавляет ещё один слой требований: privacy, compliance, data minimization и реальный вред, который может причинить неправильная работа с данными.
- `Systems of Record and Derived Data` вводит рамку про `source of truth`, производные представления и распространение обновлений между системами.

## Зачем это нужно дальше
- Эта глава заранее показывает, что архитектуру нельзя выбирать только по технической красоте: operations, vendor lock-in и regulatory constraints так же важны, как throughput и latency.
- Она задаёт язык для обсуждения того, где нужна распределённость, а где лучше остаться на одной машине.
- Она подводит к темам про [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/3 - Storage and Retrieval/03 - OLAP/Data Warehousing|Data Warehousing]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/3 - Storage and Retrieval/03 - OLAP/Column-Oriented Storage/Column-Oriented Storage|Column-Oriented Storage]].
- Она подводит к темам про caches, indexes, materialized views и другие derived representations, которые дальше будут встречаться по всей книге.
- Она связывает вводную часть книги со следующей главой про [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/_MOC - Data-Intensive Applications|reliability, scalability и maintainability]].
