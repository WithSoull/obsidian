![[99 - Meta/02 - Медиа/Pasted image 20251114142018.png]]

>[!info] Каналы `chan T`
>Некие примитивы, в которых мжно писать и из которых можно читать:
>- блокируют/разблокируют горутины
>- работают с конкретным типом
>- похожи на очереди FIFO
>- goroutione-safe
### API
``` go
ch := make(chan int) // создаем канал

ch <- 1 // записываем в канал
value, isOpened <- ch // читаем из канала

close(ch)
```

Что чтение, что запись это **блокирующие** вызовы:
- Когда мы записываем, мы ждем пока кто-то прочитает значение из канала
- Когда мы читаем, мы ждем пока кто-то запишет данные в канал
### Принцип работы
![[99 - Meta/02 - Медиа/Pasted image 20251114142701.png]]
Когда мы используем каналы, мы передаем копии наших данных, поэтому это безопасно. 
### Канал это объект *первого класса*
Это означает что они могут быть использованы как значение элемента структуры, или аргументы функции, как возврат значения из функции/метода и даже как тип для другого канала

---
### Примеры
###### Чтение и запись из/в канала это *блокирующие* операции
``` go
func async(ch chan string) {
	time.Sleep(2 * time.Second)
	ch <- "async result" // блокирующий вызов
}

func main() {
	ch := make(chan string)
	go async(ch)
	// ...
	result := <-ch // блокирующий вызов
	fmt.Println(result)
}
```
###### Наш любимы пример с счетчиком
``` go
func main() {
	mutex := sync.Mutex{}
	wg := sync.WaitGroup{}
	wg.Add(2)

	value := 0
	for i := 0; i < 2; i++ {
		go func() {
			defer wg.Done()

			mutex.Lock()
			value++
			mutex.Unlock()
		}()
	}

	wg.Wait()

	fmt.Println(value)
}
```

А вот как это можно сделать используя каналы?
``` go
func main() {
	ch := make(chan int)

	go func() {
		ch <- 1
	}()
	go func() {
		ch <- 1
	}()

	value := 0
	value += <-ch
	value += <-ch

	fmt.Println(value)
}
```

Или вот так:
``` go
func main() {
	ch := make(chan int)
	result := make(chan int, 1)

	var wg sync.WaitGroup

	// Сумматор: считает всё из ch и по закрытию отдаёт результат
	go func() {
		sum := 0
		for v := range ch {
			sum += v
		}
		result <- sum
	}()

	// Отправители
	wg.Add(10000)
	for i := 0; i < 10000; i++ {
		go func() {
			defer wg.Done()
			ch <- 1
		}()
	}

	// Когда все отправители завершились — закрываем канал
	wg.Wait()
	close(ch)

	// Забираем итог
	summa := <-result
	fmt.Println(summa)
}

```
###### producer & concumer
``` go
func producer(ch chan int) {
	defer close(ch)
	for i := 0; i < 5; i++ {
		ch <- i
	}
}

func consumer(ch chan int) {

	/*
	for {
		select {
		case value, opened := <-ch:
			if !opened {
				return
			}

			fmt.Println(value)
		}
	}
	*/

	for value := range ch { // syntax sugar
		fmt.Println(value)
	}
}

func main() {
	ch := make(chan int)
	wg := sync.WaitGroup{}
	wg.Add(2)

	go func() {
		defer wg.Done()
		producer(ch)
	}()

	go func() {
		defer wg.Done()
		consumer(ch)
	}()
	
	wg.Wait()
}
```
###### signals. notifier / subscriber
``` go 
func notifier(signals chan struct{}) {
	signals <- struct{}{}
}

func subscriber(signals chan struct{}) {
	<-signals
	fmt.Println("signaled")
}

func main() {
	signals := make(chan struct{})
	wg := sync.WaitGroup{}
	wg.Add(2)

	go func() {
		defer wg.Done()
		notifier(signals)
	}()

	go func() {
		defer wg.Done()
		subscriber(signals)
	}()

	wg.Wait()
}
```

Чтобы ововещать другие горутины, мы можем использовать пустые структуры. 
**А что если мы хотим оповестить сразу несколько горутин?**

``` go
func notifier(signals chan int) {
	close(signals)
}

func subscriber(signals chan int) {
	<-signals
	fmt.Println("signaled")
}

func main() {
	signals := make(chan int)
	wg := sync.WaitGroup{}
	wg.Add(3)

	go func() {
		defer wg.Done()
		notifier(signals)
	}()

	go func() {
		defer wg.Done()
		subscriber(signals)
	}()

	go func() {
		defer wg.Done()
		subscriber(signals)
	}()

	wg.Wait()
}
```

Если канал зыкрывается `<-signals` вернет `value, isOpened`: `value` будет равно нулевому значению типа данных, которым он является (в данном случае будет 0), а `isOpened` будет `false`. Но это "сообщение" придет всем горутинам, котоыре ждут канал и `<-signals` разблокируется.
**Причем это сообщение получат даже те горотины, которые еще не начали слушать этот канал.**

Для этого use-case важно понимать, что нельзя несколько раз закрывать канал, поэтому если требуется несколько раз передать сигнал, нужно использовать [[30 - Learning/20 - Tech Stack/Golang/2 - Concurrency/Synchronization Primitives/Cond|Cond variable]].