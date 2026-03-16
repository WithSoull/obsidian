>[!info] SHARED MUTEX (RW)
>Примитив синхронизации, который позваляет **нескольким потокам** (горутине) иметь доступ к общему ресурсу для *чтения*, но *предоставлять доступ для записи* только **одному** потоку (горутине)

### API
``` go
type RWMutex struct {...}

// взаимодействие с записью
func (rw *RWMutex) Lock()          // блокировать на запись
                                   // смогут записывать только 1 писатель
func (rw *RWMutex) Unlock()        // разблокировать на запись
func (rw *RWMutex) TryLock() bool  // попробовать заблокировать на запись

// взаимодействие с чтением
func (rw *RWMutex) RLock()         // блокировать на чтение
                                   // смогут читать N читателей
func (rw *RWMutex) RUnlock()       // разблокировать на чтение
func (rw *RWMutex) TryRLock() bool // попробовать заблокировать на чтение

// RLocker returns a [Locker] interface that implements
// the [Locker.Lock] and [Locker.Unlock] methods by calling rw.RLock and rw.RUnlock.
func (rw *RWMutex) RLocker() Locker {
	return (*rlocker)(rw)
}

// A Locker represents an object that can be locked and unlocked.
type Locker interface {
	Lock()
	Unlock()
}


```

![[99 - Meta/02 - Медиа/Pasted image 20251111202330.png]]

 1. G3 (писатель) ждет пока G1 и G2 освободят лочку, чтобы спокойно записать данные
 2. G2 / G1 отпустили лочку, и теперь G3 может прийти и записать данные
 3. G4 пришел читать и ждет, пока G3 отпустит записывающую лочку 

У нас тут возможно два варианта:
1. Будет один писатель в крит. секции
2. Будет неограниченное количество читателей
Главное: **Писатель и читатель одновременно не могут находится в крит. секции**

---
### Примеры
###### 1. Map
```go
package main

import "sync"

type Counters struct {
	mu sync.RWMutex
	m  map[string]int
}

// Читающее действие
func (c *Counters) Load(key string) (int, bool) {
	c.mu.RLock() // Блокируем только на чтение
	defer c.mu.RUnlock()

	value, found := c.m[key]
	return value, found
}

// Записывающее действие
func (c *Counters) Store(key string, value int) {
	c.mu.Lock() // Блокируем на запись
	defer c.mu.Unlock()
	c.m[key] = value
}

```

###### 2. Контр интуитивные операции пакета sync фаталятся
``` go
// Ловим ошибку
// fatal error: sync: RUnlock of unlocked RWMutex
func RUnlockLockedMutex() {
	m := sync.RWMutex{}
	m.Lock()
	m.RUnlock()
}

// Ловим ошибку
// fatal error: sync: Unlock of unlocked RWMutex
func UnlockRLockedMutex() {
	m := sync.RWMutex{}
	m.RLock()
	m.Unlock()
}

// Ловим ошибку
// fatal error: all goroutines are asleep - deadlock!
func LockRLockedMutex() {
	m := sync.RWMutex{}
	m.Lock()
	m.RLock() // читатель ждет, пока писатель лочку отпустит
	// а этого никогда не произойдет -> дедлок
}
```

### Реализация RWMutex
``` go


import "sync"

type RWMutex struct {
	notifier      *sync.Cond
	mutex         *sync.Mutex
	readersNumber int
	hasWriter     bool
}

func NewRWMutex() *RWMutex {
	var mutex sync.Mutex
	notifier := sync.NewCond(&mutex)

	return &RWMutex{
		mutex:    &mutex,
		notifier: notifier,
	}
}

func (m *RWMutex) Lock() {
	// Берем мьютекс, потому что
	// hasWriter и readersNumber нужно защитить
	// их изменение = крит. секция
	m.mutex.Lock()
	defer m.mutex.Unlock()

	// Если у нас есть писатель, то
	// второй писатель попасть не может
	// пожому ждем через Cond
	for m.hasWriter {
		m.notifier.Wait()
	}

	// Его разбудили, пред писатель ушел
	// Подтверждаем, что "следующие на очередь"
	m.hasWriter = true

	// Ждем чтобы все слушатели отпустили лок
	for m.readersNumber != 0 {
		m.notifier.Wait()
	}
}

func (m *RWMutex) Unlock() {
	// Берем мьютекс, потому что
	// hasWriter нужно защитить
	// его изменение = крит. секция
	m.mutex.Lock()
	defer m.mutex.Unlock()

	// Отпускаем флаг, чтобы
	// другая горутина смогла занять наше место
	m.hasWriter = false
	// оповещаем все горутины, и писателей, и читателей
	m.notifier.Broadcast()
}

func (m *RWMutex) RLock() {
	// Берем мьютекс, потому что
	// hasWriter и readersNumber нужно защитить
	// их изменение = крит. секция
	m.mutex.Lock()
	defer m.mutex.Unlock()

	// Ждем пока писатель отпустит лок
	for m.hasWriter {
		m.notifier.Wait()
	}

	// Добавляемся к другим читателям (а может мы и первые)
	m.readersNumber++
}

func (m *RWMutex) RUnlock() {
	// Берем мьютекс, потому что
	// readersNumber нужно защитить
	// его изменение = крит. секция
	m.mutex.Lock()
	defer m.mutex.Unlock()

	// Выходим из активных читателей
	m.readersNumber--

	// Если мы вышли последними
	// Оповещаем другие горутины (писателей)
	if m.readersNumber == 0 {
		m.notifier.Broadcast()
	}
}
```
