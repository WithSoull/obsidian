## API
![[99 - Meta/02 - Медиа/Pasted image 20250923215330.png]]

### Базовый пример с несколькими горутинами
``` go
func main() {
	var once sync.Once
	onceBody := func() {
		fmt.Println("Only once")
	}

	var wg sync.WaitGroup
	wg.Add(10)

	for i := 0; i < 10; i++ {
		go func() {
			defer wg.Done()
			once.Do(onceBody)
		}()
	}

	wg.Wait()
}
```

``` input
Only once
```

Тут смысл в том что, мы хотим, чтобы функция oncebody исполнилсь лишь один раз. Для этого мы использовали примитив синхронизации once.

### Lazy initialization
``` go
type Map struct {
	once   sync.Once
	values map[interface{}]interface{}
}

func NewMap() *Map {
	return &Map{}
}

func (m *Map) Add(key, value interface{}) {
	m.init()
	m.values[key] = value
}

func (m *Map) init() {
	m.once.Do(func() {
		m.values = make(map[interface{}]interface{})
	})
}
```

Тут стоит обратить внимание на то, что мы создаем саму мапу только тогда когда собираемся это делать,  таким образом мы не тратим время в NewMap() на это, но при этом теперь обречены каждый раз проветь, что мапа была инициализорованна.

### Synchronize singleton

``` go
package main

import "sync"

// Need to show solution

type Singleton struct{}

var instance *Singleton
var once sync.Once

func GetInstance() *Singleton {
	once.Do(func() {
		instance = &Singleton{}
	})

	return instance
}
```

Вот так например можно реализовать синглтон - паттерн, в котором некоторый объект можнет существовать только в единственном экземляре.