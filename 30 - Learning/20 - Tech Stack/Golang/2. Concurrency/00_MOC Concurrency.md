## Foundation
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Goroutines|Goroutines]] — основа конкурентности в Go
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Go Scheduler|Go Scheduler]] — как планируется выполнение горутин
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Data race & race condition|Data race & race condition]] — проблемы при неправильной синхронизации
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Wait Queue|Wait Queue]] — внутренний механизм ожидания
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Hanging goroutines|Hanging goroutines]] - подвисшие горутины
---
## Sync primitves
Примитивы синхронизации из пакета `sync` для безопасной работы с конкурентностью в Go.
## 📡 Communication (Каналы)

**Для обмена данными между горутинами (CSP model)**

- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Channels/Synchronous channels|Synchronous channels]] — основная концепция передачи данных между горутинами
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Channels/Asynchronous buffered channels|Asynchronous buffered channels]] — каналы с буфером для асинхронной коммуникации
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Channels/Unidirectional Channel|Unidirectional Channel]] - однонаправленный канал, который работает только на запись или только на чтение.
---
* [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Channels/Select statement|Select]] — мультиплексирование операций с каналами
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Channels/Simple patterns with channels|Simple patterns with channels]] - простые паттерны (как попытаться записать/прочитать из канала)
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Channels/Why do we need nil channels?|Why do we need nil channels?]] - почему разработчики Go разрешают делать nil-каналы
- [[Channel Patterns|Channel Patterns]] — распространенные паттерны (pipeline, fan-out/fan-in, worker pool)

>[!quote] **Go Philosophy**: _"Don't communicate by sharing memory; share memory by communicating"_
### Mutual Exclusion (Блокировки)
**Для защиты критических секций от одновременного доступа**
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Mutex/Mutex|Mutex]] — взаимная блокировка для эксклюзивного доступа
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/RWMutex|RWMutex]] — читатель/писатель блокировка для read-heavy нагрузок
### Coordination (Координация)
**Для синхронизации выполнения горутин**
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/WaitGroup|WaitGroup]] — ожидание завершения группы горутин
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Once|Once]] — гарантированное однократное выполнение
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Cond|Cond]] — условная переменная для сложных условий ожидания
### Lock-Free & High-Performance
**Для быстрых операций без блокировок**
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Atomic|Atomic]] — атомарные операции на уровне CPU
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Map|Map]] — конкурентно-безопасная мапа без явных блокировок
### Resource Pooling
**Для переиспользования объектов**
- [[30 - Learning/20 - Tech Stack/Golang/2. Concurrency/Synchronization Primitives/Pool|Pool]] — пул временных объектов для снижения аллокаций
---
## Сравнительная таблица

| Primitive | Use Case | Performance | Complexity |
|-----------|----------|-------------|------------|
| Mutex | Exclusive access | Medium | Low |
| RWMutex | Read-heavy workloads | High (reads) | Medium |
| WaitGroup | Wait for goroutines | High | Low |
| Once | One-time initialization | High | Low |
| Cond | Complex conditions | Medium | High |
| Atomic | Simple counters/flags | Very High | Medium |
| Map | Concurrent map ops | High | Low |
| Pool | Object reuse | Very High | Medium |

## Когда что использовать?
- **Protecting shared state** → Mutex / RWMutex
- **Waiting for completion** → WaitGroup
- **One-time setup** → Once
- **Simple counters** → Atomic
- **Complex conditions** → Cond
- **Concurrent map** → sync.Map
- **Reduce GC pressure** → Pool
