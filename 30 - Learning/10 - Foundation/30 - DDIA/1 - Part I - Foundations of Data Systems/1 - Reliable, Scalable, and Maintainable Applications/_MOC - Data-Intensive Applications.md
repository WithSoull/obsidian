# Reliable, Scalable, and Maintainable Applications

Это карта главы 2 DDIA **Defining Nonfunctional Requirements**.

## Зачем нужна эта глава
**Функциональные** требования отвечают на вопрос "что система умеет".

**Нефункциональные** требования отвечают на вопрос "насколько хорошо система должна это делать":
- насколько быстро;
- насколько надежно;
- какую нагрузку должна выдерживать;
- насколько легко ее сопровождать и менять.

## Что здесь считается data-intensive
Большинство современных приложений упираются не в CPU как таковой, а в данные:
- сколько данных нужно хранить;
- насколько они сложны;
- как быстро они меняются;
- как быстро их нужно читать, пересчитывать и доставлять.

Поэтому система обычно собирается из нескольких типовых компонентов:
- **database**;
- **cache**;
- **search index**;
- **stream processing**;
- **batch processing**.

Пример системы, где эти части комбинируются:
![[99 - Meta/02 - Медиа/Pasted image 20250411134021.png]]

## Как читать ветку
Лучше идти в таком порядке:
1. [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Measuring Performance|Performance]]
2. [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability|Reliability]]
3. [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability|Scalability]]
4. [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Maintainability|Maintainability]]

# Каркас главы
### [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Measuring Performance|Performance]]
Сначала нужно договориться о языке измерения системы:
- **throughput**;
- **response time**;
- **service time**;
- **latency**;
- percentiles;
- SLO/SLA.

Эта ветка отвечает за словарь и поведение системы под нагрузкой. Подробности не повторяем в **Scalability**, а только используем как базу.

### [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability|Reliability]]
Надежность  это способность системы продолжать работать корректно, когда что-то идет не так.

Внутри ветки:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Fault vs Failure|Fault vs Failure]]

### [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability|Scalability]]
Масштабируемость  это не "система большая", а способность удерживать приемлемую производительность при росте нагрузки.

Эта ветка отвечает за load dimensions и выбор подходов к росту, а не за повторное объяснение performance-метрик.

Внутри ветки:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Twitter Scaling|Twitter Scaling]]

### [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Maintainability|Maintainability]]
Система должна быть не только рабочей сегодня, но и понятной, операбельной и изменяемой завтра.

Внутри ветки:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Operability|Operability]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Simplicity|Simplicity]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Evolvability|Evolvability]]

## Что держать рядом
До этой главы полезно помнить две рамки из предыдущей части:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Distributed Versus Single-Node Systems|Distributed Versus Single-Node Systems]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Systems of Record and Derived Data|Systems of Record and Derived Data]]

Дополнительно:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/Defining Nonfunctional Requirements Audit|Defining Nonfunctional Requirements Audit]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/WhatsApp Service Architecture|WhatsApp Service Architecture]]
