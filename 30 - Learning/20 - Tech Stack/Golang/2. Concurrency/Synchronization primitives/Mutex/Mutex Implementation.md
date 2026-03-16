![[99 - Meta/02 - Медиа/Pasted image 20251109152621.png]]

### Самая простая реализация мьютекса - *неправильная*
``` go
package main

const (
	unlocked = false
	locked   = true
)

type BrokenMutex struct {
	state bool
}

// Здесь есть data race и нет гарантии взаимного исключения (safety),
// так как несколько горутин могут попасть совместно в критическую секцию

func (m *BrokenMutex) Lock() {
	for m.state {
		// итерация за итерацией...
	}
	// вот здесь может произойти прерывание и несколько
	// горутин могут попасть в крит секцию
	m.state = locked
}

func (m *BrokenMutex) Unlock() {
	m.state = unlocked
}
```

![[99 - Meta/02 - Медиа/Pasted image 20251109152904.png]]

Тут горутина может выпрыгнуть из крит. секции к тому же. **Когды мы не используем примитивы синхронизации мы даем волю процессору/компилятору переупорядочивать наш код**. Чтобы решить эту проблему мы сейчас будем использовать *атомарные операции*, тк они внутри себя используют барьеры памяти, которые запрящают это делать процессору.

``` go
package main

import "sync/atomic"

const (
	unlocked = false
	locked   = true
)

type BrokenMutex struct {
	state atomic.Bool
}

// Здесь нет гарантии взаимного исключения (safety), так как несколько
// горутин могут попасть совместно в критическую секцию

func (m *BrokenMutex) Lock() {
	for m.state.Load() {
		// итерация за итерацией...
	}
	// тут все еще может произойти прерывание
	m.state.Store(locked)
}

func (m *BrokenMutex) Unlock() {
	m.state.Store(unlocked)
}

```

Тут уже решили проблему data race, но проблема с liveness и safety все еще остались. Чтобы ее решить можем использовать CAS
``` go
package main

import (
	"sync/atomic"
)

const (
	unlocked = false
	locked   = true
)

type SpinLock struct {
	state atomic.Bool
}

func NewSpinLock() *SpinLock {
	return &SpinLock{}
}

func (s *SpinLock) Lock() {
	// постоянно греем процессор, горутина не уходит в
	// статут waiting
	// это оправдано только, если супер быстрые операции
	// под лочкой(в крит секции), но надо мерить бэнчмарки
	// из плюсов тут у нас нет CS
	for !s.state.CompareAndSwap(unlocked, locked) {
		// итерация за итерацией...
	}
}

func (s *SpinLock) Unlock() {
	s.state.Store(unlocked)
}
```

### Как избавиться от активного ожидания и перестать греть процессор?
![[99 - Meta/02 - Медиа/Pasted image 20251109153730.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109153740.png]]
Инструкция *PAUSE*, работает при гипертрединге и переключает поток на другой набор регистров, может там, что-то полезное есть.

``` go
package main

import (
	"runtime"
	"sync/atomic"
)

const (
	unlocked = false
	locked   = true
)

type SpinLock struct {
	state atomic.Bool
}

func NewSpinLock() *SpinLock {
	return &SpinLock{}
}

func (s *SpinLock) Lock() {
	for !s.state.CompareAndSwap(unlocked, locked) {
		runtime.Gosched() 
		// сделаем CS, и поищем еще чего-то
		// но горутина не перейдет в состояние ожидания
		// но тут появляется проблема голодания горутин
	}
}

func (s *SpinLock) Unlock() {
	s.state.Store(unlocked)
}

```

![[99 - Meta/02 - Медиа/Pasted image 20251109154052.png]]

Можно обратиться через сискол к планировщику ядра линукса и попросить заблокировать какой-то поток. Но это неэфективно, тк будет 2 CS и все зачем были созданы горутины и гошный планировщик теряет свой смысл

``` go
package main

import (
	"runtime"
	"sync/atomic"
)

const (
	unlocked = false
	locked   = true
)

const retriesNumber = 3

type SpinLock struct {
	state atomic.Bool
}

func NewSpinLock() *SpinLock {
	return &SpinLock{}
}

func (s *SpinLock) Lock() {
	retries := retriesNumber
	for !s.state.CompareAndSwap(unlocked, locked) {
		retries--
		if retries == 0 {
			runtime.Gosched()
			retries = retriesNumber
		}
	}
}

func (s *SpinLock) Unlock() {
	s.state.Store(unlocked)
}
```

Так как критические секции чаще всего короткие, мы можем немного покрутиться в цикле

![[99 - Meta/02 - Медиа/Pasted image 20251109154507.png]]

Но тут может быть проблема с голоданием. Потому что CAS не гаранитирует никакого порядка. Нужна какая-то очередь.

![[99 - Meta/02 - Медиа/Pasted image 20251109154654.png]]

``` go
package main

import (
	"runtime"
	"sync/atomic"
)

type TicketLock struct {
	ownerTicket    atomic.Int64
	nextFreeTicket atomic.Int64
}

func NewTicketLock() *TicketLock {
	return &TicketLock{}
}

func (t *TicketLock) Lock() {
	ticket := t.nextFreeTicket.Add(1)
	for t.ownerTicket.Load() != ticket-1 {
		runtime.Gosched()
	}
}

func (t *TicketLock) Unlock() {
	t.ownerTicket.Add(1)
}
```

Тут уже у нас появляется очередь и проблема голодания решается.

### А как можно достичь всего этого без RWM (CAS)?

``` go
package main

import (
	"runtime"
	"sync/atomic"
)

const (
	unlocked = false
	locked   = true
)
// только для 2-ух горутин
type BrokenMutex struct {
	want  [2]atomic.Bool
	owner int
}

// Здесь нет гарантии прогресса (liveness), так как могут несколько
// горутин могут помешать друг другу и попасть в livelock

func (m *BrokenMutex) Lock(index int) {
	m.want[index].Store(locked)
	// вот тут может произойти прерывание
	for m.want[1-index].Load() {
		runtime.Gosched()
	}

	m.owner = index
}

func (m *BrokenMutex) Unlock(index int) {
	m.want[m.owner].Store(unlocked)
}
```

Чтобы решить проблему liveness проблему можно добавить поле *victim*, и мы получим мьютекс *Петерсона*
``` go
package main

import (
	"runtime"
	"sync/atomic"
)

const (
	unlocked = false
	locked   = true
)

type PetersonMutex struct {
	want   [2]atomic.Bool
	victim atomic.Int32
	owner  int
}

func (m *PetersonMutex) Lock(index int) {
	m.want[index].Store(locked)
	m.victim.Store(int32(index)) // ключевая идея, в том что victim 
	// может быть только одним числом и пройдет только одна горутина

	// ждет только жерва
	for m.want[1-index].Load() && m.victim.Load() == int32(index) {
		runtime.Gosched()
	}

	m.owner = index
}

func (m *PetersonMutex) Unlock(index int) {
	m.want[m.owner].Store(unlocked)
}
```

### Что делать для 2+ горутин?
![[99 - Meta/02 - Медиа/Pasted image 20251109155903.png]]
Теоритическая модель, мьютекс проще использовать с CAS'ами
## Как устроен мьютекс в ядре линукса?
![[99 - Meta/02 - Медиа/Pasted image 20251109160025.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109160040.png]]

![[99 - Meta/02 - Медиа/Pasted image 20251109160051.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109160110.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109160118.png]]

## Как устроены мьютексы в райнтайме го?
Основное отличие в том что мьютекс в го не хранит ID горутины.
![[99 - Meta/02 - Медиа/Pasted image 20251109160210.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109160219.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109160232.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109160242.png]]