>[!info] Mutex - Muteral Exclusion - взаимное исключение

![[99 - Meta/02 - Медиа/Pasted image 20251121221103.png]]

>[!danger] Критическая секция
>Это место в которое должна зайти только одна горутина

## Код

### Неправильный инкремент

``` go
func main() {
	wg := sync.WaitGroup{}
	wg.Add(1000)

	value := 0
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

``` output
➜  3_lesson_sync_primitives_1 git:(master) ✗ go run 05_incorrect_increment/main.go
966
➜  3_lesson_sync_primitives_1 git:(master) ✗ go run 05_incorrect_increment/main.go
936
➜  3_lesson_sync_primitives_1 git:(master) ✗ go run 05_incorrect_increment/main.go
946
➜  3_lesson_sync_primitives_1 git:(master) ✗ go run 05_incorrect_increment/main.go
917
➜  3_lesson_sync_primitives_1 git:(master) ✗ go run 05_incorrect_increment/main.go
927
```

Видим, что 1000 не выводит. Почему так происходит? Как вообще устроен инкремент?
``` go
oldValue := value
newValue := oldValue + 1
value = newValue
```

Между любыми строчками может втиснуться другая горутина, а еще планировщик ОС может свичнуться на другой поток, мы получаем *недетерминированный вывод*

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 11.20.06.png]]

Вот пример  того, что может произойти: сначала две горутины прочитаю значение 100, а потом прибавят 1, и дважды присвоят 101 к переменной `value`. И данный инкремент можно назвать **критической** секцией.

Такую проблему можно решить _НЕ_ эффективно через `wg.Wait()` на каждой итерации цикла, заставив горутины выполняться последовательно:
``` go
func main() {
	wg := sync.WaitGroup{}

	value := 0
	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			value++
		}()
		wg.Wait() // Ждем пока горутина отработает
	}

	fmt.Println(value)
}
```

Эффективнее всего решить эту проблему через Mutex конечно, как минимум это эффективнее потому что инкремент атомика стоит весьма дорого, и лучше сразу инкрементить на 1000:
``` go
func main() {
	wg := sync.WaitGroup{}
	mu := sync.Mutex{}

	wg.Add(1000)
	value := 0
	for i := 0; i < 1000; i++ {
		go func() {
			defer wg.Done()

			mu.Lock()   // Сюда пропускаем одну горутину
			value++
			mu.Unlock() // Остальные горутины ждут когда текущая отпустит лок
		}()
	}

	wg.Wait()
	fmt.Println(value)
}
```

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 11.28.50.png]]
![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 11.29.09.png]]

>[!danger] Когда горутина блокируется в мьютексе, она переходитиз состояния **Running** в **Waiting**

### Несколько критических секций

``` go
var mutex sync.Mutex
var value string

func set(v string) {
	mutex.Lock()
	value = v
	mutex.Unlock()
}

func print() {
	mutex.Lock()
	fmt.Println(value)
	mutex.Unlock()
}
```

Этот пример показывает то, что если **один** мьютекс охраняет несколько критических секций, то во время блокировки ни одна другая горутина не попадет в другую крит. секцию. В целом логично.

### Мьютекс с локальной переменной
``` go
func main() {
	mutex := sync.Mutex{}
	wg := sync.WaitGroup{}
	wg.Add(1000)

	for i := 0; i < 10; i++ {
		go func() {
			defer wg.Done()

			value := 0
			for j := 0; j < 10; j++ {
				mutex.Lock()
				value++
				mutex.Unlock()
			}

			log.Println(value)
		}()
	}

	wg.Wait()
}
```

Здесь переменная value для каждой итерации цикла своя, и нет смысла обмазывать ее мьютексом.

### Использование мьютекса для обеспечения упорядочности
``` go
package main

import (
	"log"
	"sync"
	"time"
)

func main() {
	var mutex sync.Mutex
	mutex.Lock()

	go func() {
		time.Sleep(time.Second)
		log.Println("Hi")
		mutex.Unlock()
	}()

	mutex.Lock()
	log.Println("Bye")
}
```

Здесь мы перед запуском горутины захватили мьютекс, и после печати отпустили мьютекс, таким образом у нас сначала выведется "Hi", а только потом "By"

## Print foo bar alternately
``` go
type FooBar struct {
	number   int
	fooMutex sync.Mutex
	barMutex sync.Mutex
}

func NewFooBar(number int) *FooBar {
	fb := &FooBar{number: number}
	fb.barMutex.Lock()
	return fb
}

func (fb *FooBar) Foo(printFoo func()) {
	for i := 0; i < fb.number; i++ {
		fb.fooMutex.Lock()
		printFoo()
		fb.barMutex.Unlock()
	}
}

func (fb *FooBar) Bar(printBar func()) {
	for i := 0; i < fb.number; i++ {
		fb.barMutex.Lock()
		printBar()
		fb.fooMutex.Unlock()
	}
}

func main() {
	fb := NewFooBar(3)
	wg := sync.WaitGroup{}
	wg.Add(1)

	go func() {
		defer wg.Done()
		fb.Foo(func() {
			log.Println("foo")
		})
	}()

	go func() {
		defer wg.Done()
		fb.Bar(func() {
			log.Println("bar")
		})
	}()

	wg.Wait()
}

```

Здесь задача заключается в том чтобы конкуренто выводить FooBarFooBar в таком порядке несколько раз подряд.
Решение: при создании мы захватываем лок для Bar, во время выполнения `Foo()`, захватыватываем Foo, чтобы в следующей итерации наша Foo горутина попала в статус *waiting*, дальше мы вы выполняем `printFoo()`, и после отпускаем Bar лок, тем самым даем возможность Bar горутине захватить barMutex и выполнить `printBar()`. Ну и дальше они друг друга блокируют по очереди и ждут.