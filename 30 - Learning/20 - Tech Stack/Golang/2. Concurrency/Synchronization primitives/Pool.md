>[!info] **POOL** - структура, доступ к которой синхронизирован. **Паттерн OBJECT POOL**
Набор инициализированных и готовых к использованию объектов:
> - ﻿﻿когда системе требуется объект, он не создаётся, а берётся из пула
> - ﻿﻿когда объект больше не нужен, он не уничтожается, а возвращается в пул

### Плюсы и минусы
**Плюсы**:
- Не идем в алокатор, чтобы создать новый объект
- Не нагружаем GC
### API
``` go
type Pool struct {
	New func() any
}

// Забирает объект из пула
// при неоходимости может его создать
func (p *Pool) Get() any

// Возвращает объект обратно в пул
func (p *Pool) Put(x any)
```

![[99 - Meta/02 - Медиа/Pasted image 20251107204205.png]]![[99 - Meta/02 - Медиа/Pasted image 20251107204213.png]]![[99 - Meta/02 - Медиа/Pasted image 20251107204226.png]]

>[!danger]  GC все равно может собрать данные из Object Pool

![[99 - Meta/02 - Медиа/Pasted image 20251107204236.png]]
### Примеры
###### Person Pool
Тут мы написали просто обертку, чтобы не мучаться каждый раз с кастингом типов. При этом, когда мы что-то кладем в пул, эти данные никто не зануляет, это нужно делать самостоятельно.
``` go
type Person struct {
	name string
}

type PersonsPool struct {
	pool sync.Pool
}

func NewPersonsPool() *PersonsPool {
	return &PersonsPool{
		pool: sync.Pool{
			New: func() interface{} { return new(Person) },
		},
	}
}
func (p *PersonsPool) Get() *Person {
	return p.pool.Get().(*Person)
}

func (p *PersonsPool) Put(person *Person) {
	p.pool.Put(person)
}
```

``` go
func BenchmarkWithPool(b *testing.B) {
	pool := NewPersonsPool()
	for i := 0; i < b.N; i++ {
		person := pool.Get()
		person.name = "Ivan" // Need to initialize
		pool.Put(person)
	}
}

var gPerson *Person

func BenchmarkWithoutPool(b *testing.B) {
	for i := 0; i < b.N; i++ {
		person := &Person{name: "Ivan"}
		gPerson = person
	}
}
```

``` output
goos: darwin
goarch: arm64
cpu: Apple M4
BenchmarkWithPool-10            144474736                8.244 ns/op           0 B/op          0 allocs/op
BenchmarkWithoutPool-10         100000000               10.86 ns/op           16 B/op          1 allocs/op
PASS
ok      command-line-arguments  3.307s

```

### Пример реализации
``` go
package main

import "sync"

type Node struct {
	Value any
	next  *Node
}

type freeList struct {
	head *Node
}

func newLinkedList() freeList {
	return freeList{}
}

func (l *freeList) push(node *Node) {
	node.next = l.head
	l.head = node
}

func (l *freeList) pop() *Node {
	if l.head != nil {
		node := l.head
		l.head = l.head.next
		return node
	}

	return nil
}

type Pool struct {
	ctr func() any

	mtx  sync.Mutex
	list freeList
}

func NewPool(ctr func() any) *Pool {
	return &Pool{
		ctr: ctr,
	}
}

func (l *Pool) Get() *Node {
	l.mtx.Lock()
	defer l.mtx.Unlock()

	node := l.list.pop()
	if node == nil {
		node = &Node{
			Value: l.ctr(),
		}
	}
	return node
}

func (l *Pool) Put(node *Node) {
	l.mtx.Lock()
	defer l.mtx.Unlock()
	l.list.push(node)
}
```