>[!info] Атомарные операции
>Операции, которые выполняются целиком, либо не выполняются вовсе

# API
![[99 - Meta/02 - Медиа/Pasted image 20251109092608.png]]
![[99 - Meta/02 - Медиа/Pasted image 20251109092640.png]]
### Incorrect increment
``` go
func main() {
	wg := sync.WaitGroup{}
	wg.Add(1000)

	var value int
	for i := 0; i < 1000; i++ {
		go func() {
			defer wg.Done()
			value++
		}()
	}

	wg.Wait()

	fmt.Println(value)
}
```

Мы уже помним, что здесь доступ в критическую зону могут получить несколько горутин и поэтому value != 1000. Одним из решением этой проблемы может быть мьютекс, нужно просто защитить критическую секцию `value++` мьютексом. Но это можно и сделать решить эту проблему еще? С помощью атомиков  - ведь если `value++` будет атомарной операцией, она перестанет быть критической секцией.

``` go
func main() {
	wg := sync.WaitGroup{}
	wg.Add(1000)

	var value int64
	for i := 0; i < 1000; i++ {
		go func() {
			defer wg.Done()
			atomic.AddInt64(&value, 1)
		}()
	}

	wg.Wait()

	fmt.Println(value)
}
```

``` output
 ➜  go run 06_incorrect_increment/main.go --race
1000

```

### Compare and swap
``` go
var data map[string]string
var initialized atomic.Bool

func initialize() {
	if !initialized.Load() {
		initialized.Store(true)
		data = make(map[string]string)
		fmt.Println("initialized")
	}
}

func main() {
	wg := sync.WaitGroup{}
	wg.Add(1000)

	for i := 0; i < 1000; i++ {
		go func() {
			defer wg.Done()
			initialize()
		}()
	}
	wg.Wait()
}
```
Этот код кажется должен инициализировать мапу только один раз, но это не так. Горутина может пройти в тело условия `!initialized.Load()`,  а планироващик переключиться на другую горутинку, и еще одна горутина сможет зайти в это условие, таким образом несколько горутин окажутся внутри условия.

![[99 - Meta/02 - Медиа/Pasted image 20251109093541.png]]
Нам нужно атомарно прочитать и записать данные. Для этого используют CompareAndSwap:
``` go
// compare and swap
// вот как он устроен семантически
if *addr == old {
	*addr = new
	return true
}
return false
```

``` go
var data map[string]string
var initialized atomic.Bool

func initialize() {
	if initialized.CompareAndSwap(false, true) {
		data = make(map[string]string)
		fmt.Println("initialized")
	}
} 
```

###### CAS loop
``` go 
func IncrementAndGet(pointer *int32) int32 {
	for {
		currentValue := atomic.LoadInt32(pointer)
		//  тут может встроиться кто угодно
		nextValue := currentValue + 1
		// и тут может встроиться кто угодно
		if atomic.CompareAndSwapInt32(pointer, currentValue, nextValue) {
			return nextValue
		}
	}
}
```

Еще один пример CAS, в котором при успешном свопе мы вернем значение, а если нет: то попытаемся еще раз

###### Излишнее атомики
``` go
func (d *Data) Process() {
	d.count.Add(1) // 99 + 1, другая горутина 100 + 1 == 101
	// шедулер переключился
	if d.count.CompareAndSwap(100, 0) { // а счетчик уже == 101, а не 100
		// do something...
	}
}
```

Тут все решается намного проще:
``` go
func (d *Data) Process() {
	value := d.count.Add(1)
	if value == 100 {
		// do something...
	}
}
```

Теперь у нас value просто сохранится в локальную переменную, которая уже не будет измененена

###### Atomic pointer
``` go
func main() {
	// До появления дженериков это был единственный вариант
	{
		var value1 int32 = 100
		var value2 int32 = 100
		pointer := unsafe.Pointer(&value1)
		atomic.StorePointer(&pointer, unsafe.Pointer(&value2))
	}
	
	// Этот вариант кажется слегка проще
	{
		var value1 int32 = 100
		var value2 int32 = 100
		var pointer atomic.Pointer[int32]
		pointer.Store(&value1)
		pointer.Store(&value2)
	}
}
```