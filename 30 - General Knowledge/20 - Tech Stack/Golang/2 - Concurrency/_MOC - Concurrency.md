## Foundation
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Goroutines|Goroutines]] — основа конкурентности в Go
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Go Scheduler|Go Scheduler]] — как планируется выполнение горутин
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Data Race vs Race Condition|Data race & race condition]] — проблемы при неправильной синхронизации
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Wait Queue|Wait Queue]] — внутренний механизм ожидания
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Hanging Goroutines|Hanging goroutines]] - подвисшие горутины
---
## Sync primitves
Примитивы синхронизации из пакета `sync` для безопасной работы с конкурентностью в Go.
## 📡 Communication (Каналы)

**Для обмена данными между горутинами (CSP model)**

- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Channels/Synchronous Channels|Synchronous channels]] — основная концепция передачи данных между горутинами
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Channels/Asynchronous Buffered Channels|Asynchronous buffered channels]] — каналы с буфером для асинхронной коммуникации
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Channels/Unidirectional Channel|Unidirectional Channel]] - однонаправленный канал, который работает только на запись или только на чтение.
---
* [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Channels/Select Statement|Select]] — мультиплексирование операций с каналами
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Channels/Simple Channel Patterns|Simple patterns with channels]] - простые паттерны (как попытаться записать/прочитать из канала)
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Channels/Why Nil Channels Matter|Why do we need nil channels?]] - почему разработчики Go разрешают делать nil-каналы
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Channel Patterns|Channel Patterns]] — распространенные паттерны (pipeline, fan-out/fan-in, worker pool)

>[!quote] **Go Philosophy**: _"Don't communicate by sharing memory; share memory by communicating"_
### Mutual Exclusion (Блокировки)
**Для защиты критических секций от одновременного доступа**
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Mutex/Mutex|Mutex]] — взаимная блокировка для эксклюзивного доступа
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/RWMutex|RWMutex]] — читатель/писатель блокировка для read-heavy нагрузок
### Coordination (Координация)
**Для синхронизации выполнения горутин**
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/WaitGroup|WaitGroup]] — ожидание завершения группы горутин
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Once|Once]] — гарантированное однократное выполнение
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Cond|Cond]] — условная переменная для сложных условий ожидания
### Lock-Free & High-Performance
**Для быстрых операций без блокировок**
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Atomic|Atomic]] — атомарные операции на уровне CPU
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Map|Map]] — конкурентно-безопасная мапа без явных блокировок
### Resource Pooling
**Для переиспользования объектов**
- [[public/30 - General Knowledge/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Pool|Pool]] — пул временных объектов для снижения аллокаций
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
