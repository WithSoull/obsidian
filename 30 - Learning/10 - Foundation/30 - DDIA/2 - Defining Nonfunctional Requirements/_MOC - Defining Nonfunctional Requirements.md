# Reliable, Scalable, and Maintainable Applications

Это карта ветки про нефункциональные требования в data-intensive системах.

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
1. [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/0 - Performance/Measuring Performance|Performance]]
2. [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/1 - Reliability/Reliability|Reliability]]
3. [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/2 - Scalability/Scalability|Scalability]]
4. [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Maintainability|Maintainability]]

# Каркас главы
### [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/0 - Performance/Measuring Performance|Performance]]
Сначала нужно договориться о языке измерения системы:
- **throughput**;
- **response time**;
- **service time**;
- **latency**;
- percentiles;
- SLO/SLA.

Эта ветка отвечает за словарь и поведение системы под нагрузкой. Подробности не повторяем в **Scalability**, а только используем как базу.

### [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/1 - Reliability/Reliability|Reliability]]
Надежность  это способность системы продолжать работать корректно, когда что-то идет не так.

Внутри ветки:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/1 - Reliability/Fault vs Failure|Fault vs Failure]]

### [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/2 - Scalability/Scalability|Scalability]]
Масштабируемость  это не "система большая", а способность удерживать приемлемую производительность при росте нагрузки.

Эта ветка отвечает за load dimensions и выбор подходов к росту, а не за повторное объяснение performance-метрик.

Внутри ветки:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/2 - Scalability/Twitter Scaling|Twitter Scaling]]

### [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Maintainability|Maintainability]]
Система должна быть не только рабочей сегодня, но и понятной, операбельной и изменяемой завтра.

Внутри ветки:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Operability|Operability]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Simplicity|Simplicity]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Evolvability|Evolvability]]

## Что держать рядом
До этой главы полезно помнить две рамки из предыдущей части:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/1 - Trade-Offs in Data Systems Architecture/Distributed Versus Single-Node Systems|Distributed Versus Single-Node Systems]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/1 - Trade-Offs in Data Systems Architecture/Systems of Record and Derived Data|Systems of Record and Derived Data]]

Дополнительно:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/Defining Nonfunctional Requirements Audit|Defining Nonfunctional Requirements Audit]]
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/WhatsApp Service Architecture|WhatsApp Service Architecture]]
