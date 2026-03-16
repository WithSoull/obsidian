>[!info] СЕМАФОР
>Примитив синхронизации, который используется для управления доступом к общим ресурсам **несколькими** потоками (горутинами)

![[99 - Meta/02 - Медиа/Pasted image 20251107200511.png]]

Семафор, в отличии от мьютекса может предоставить доступ сразу N горутинам. Это полезно в ситуациях когда нужно ограничить доступ к ресурсу.  

К сожалению в Go, нет реализации семафора, но мы можем ее написать самостоятельно.

### Пример реализации семафора на [[30 - Learning/20 - Tech Stack/Golang/2. Concurrancy/Synchronization primitives/Cond|Cond Variable]]
``` go
package main

import (
	"sync"
)

type Semaphore struct {
	count     int
	max       int
	condition *sync.Cond
}

func NewSemaphore(limit int) *Semaphore {
	mutex := &sync.Mutex{}
	return &Semaphore{
		max:       limit,
		condition: sync.NewCond(mutex),
	}
}

func (s *Semaphore) Acquire() { // simple to Lock
	s.condition.L.Lock()
	defer s.condition.L.Unlock()

	for s.count >= s.max {
		s.condition.Wait()
	}

	s.count++
}

func (s *Semaphore) Release() { // simple to Unlock
	s.condition.L.Lock()
	defer s.condition.L.Unlock()

	s.count--
	s.condition.Signal()
}
```