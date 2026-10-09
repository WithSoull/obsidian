>[!info] Buffered channels VS Unbuffered channels
>![[99 - Meta/02 - Медиа/Pasted image 20251114161205.png]]
>![[99 - Meta/02 - Медиа/Pasted image 20251114161214.png]]

### Примеры
###### Создание, запись и чтение из буф канала + len(ch) + cap(ch) 
``` go
func main() {
	ch := make(chan int, 2)
	ch <- 1
	fmt.Printf("write value %d: len(ch) = %d \t cap(ch) = %d\n", 1, len(ch), cap(ch))
	ch <- 2
	fmt.Printf("write value %d: len(ch) = %d \t cap(ch) = %d\n", 2, len(ch), cap(ch))

	close(ch)
	fmt.Println("close channel")
	// ch <- 100 этот вызов уже будет блокирующим, потому что
	// канал переполнен, мы получим deadlock, потому что единственная горутина
	// будет ждать все время
	for val := range ch {
		fmt.Printf("read  value %d: len(ch) = %d \t cap(ch) = %d\n", val, len(ch), cap(ch))
	}
}
```

``` ouput
write value 1: len(ch) = 1       cap(ch) = 2
write value 2: len(ch) = 2       cap(ch) = 2
close channel
read  value 1: len(ch) = 1       cap(ch) = 2
read  value 2: len(ch) = 0       cap(ch) = 2
```

**Важно:** Функция *len(ch chan)* и *cap(ch chan)* уже синхронизированы и не нужно оборачивать их в мьютексы их.

###### Операции с закрытыми/nil каналами
![[99 - Meta/02 - Медиа/Pasted image 20251115115028.png]]

---
**Запись в nil канал:**
``` go
func writeToNilChannel() {
	var ch chan int
	ch <- 1
}
```

``` output
fatal error: all goroutines are asleep - deadlock!
```
---
**Запись в закрытый канал:**
``` go
func writeToClosedChannel() {
	ch := make(chan int, 2)
	close(ch)
	ch <- 20
}
```

``` output
panic: send on closed channel
```
---
**Чтение из nil канала:**
``` go
func readFromNilChannel() {
	var ch chan int
	<-ch
}

// тоже самое с range, потому что под капотом он
// вызывает <-chan
func rangeNilChannel() {
	var ch chan int
	for range ch {

	}
}
```

``` output
fatal error: all goroutines are asleep - deadlock!
```
---
**Чтение из закрытого канала:**
``` go
func readFromChannel() {
	ch := make(chan int, 2)
	ch <- 10
	ch <- 20

	val, ok := <-ch        // Достали первое значение 10
	fmt.Println(val, ok)

	close(ch)              // Закрыли канал
	val, ok = <-ch         // Достали второе значение 20
	fmt.Println(val, ok)

	val, ok = <-ch         // Достали дефолт значение
	fmt.Println(val, ok)   // в котором ok = false
}
```

``` output
10 true
20 true
0 false
```
---
**Закрытие nil канала:**
``` go
func closeNilChannel() {
	var ch chan int
	close(ch)
}
```

``` output
panic: close of nil channel
```
---
**Закртыие уже закрытого канала:**
``` go
func closeChannelAnyTimes() {
	ch := make(chan int)
	close(ch)
	close(ch)
}
```

``` output
panic: close of closed channel
```
---
**Чтение из нескольких каналов сразу:**
``` go
func readAnyChannels() {
	ch1 := make(chan int)
	ch2 := make(chan int)

	go func() {
		ch1 <- 100
	}()

	go func() {
		ch2 <- 200
	}()

	select {
	case val1 := <-ch1:
		fmt.Println(val1)
	case val2 := <-ch2:
		fmt.Println(val2)
	}
}
```

Здесь у нас нет никакого порядка, первый кто напишет в канал, тот и пройдет в `select`
###### `chan` это указатель на внутреннюю структуру канала
Поэтому, сделав копию, мы будем писать в исходный канал (копируется указатель):
``` go
func main() {
	source := make(chan int)
	clone := source

	go func() {
		source <- 1
	}()

	fmt.Println(<-clone) // 1
}
```

**Также можно сравнивать каналы:** `chan` это указатель на внутренню структуру канала, поэтому сравнивая два `chan` мы сравниваем два указателя, `ch1 == ch2`, когда указатели равны.
``` go
func compareChannels() {
	ch1 := make(chan int)
	ch2 := make(chan int)

	equal1 := ch1 == ch2 // false
	equal2 := ch1 == ch1 // true

	fmt.Println(equal1)
	fmt.Println(equal2)
}
```

### Кто должен закрывать канал?
1) Если *писатель один*: канал закрывает тот, кто в него пишет
2) Если *писателей несколько*: канал закрывает тот, кто создал писателей и сам канал

### А что будет если канал не закрыть?
###### Простой пример с 1 горутиной
``` go
func main() {
	doWork := func(strings <-chan string) {
		go func() {
			for str := range strings {
				fmt.Println(str)
			}

			log.Println("doWork exited")
		}()
	}

	strings := make(chan string)
	doWork(strings)
	strings <- "Test"
	// Здесь стоит закрыть канал
	time.Sleep(time.Second)
	fmt.Println("Done")
}
```
Здесь мы видим, что канал читает горутинка, и после цикла она должна завершить исполнение и напечатать `doWork exited`, но она этого не сделает, потому что в range она сидит и ждет новую запись или закрытие. Конечно, с закрытием приложения, горутина принудительно тоже зафаталится, но если приложение работает вечно, такие утечки не к чему. Чтобы избежать утечки достаточно закрыть канал, добавим `close(strings)`.
``` output
# Без закрытия канала
Test
Done

# С закрытием канала
Test
2025/11/15 13:20:58 doWork exited
Done
```
###### Пример с FRW стратегией
``` go
// First-response-wins strategy
func request() int {
	ch := make(chan int)
	for i := 0; i < 5; i++ {
		go func() {
			ch <- i // 4 горутины просто заблокируются
		}()
	}

	return <-ch
}
```

Здесь у нас будет прочитан только самый первый ответ, остальные остануться в ожидании, поэтому мы должны здесь использовать буфферизированные каналы. Канал здесь закрывать необязательно, потому что сборщик мусора его соберет, ведь все горутины которые могли на него ссылаться закончилили своб работу уже.

```go
func request() int {
	ch := make(chan int, 5)
	for i := 0; i < 5; i++ {
		go func() {
			ch <- i
		}()
	}

	return <-ch
}
```
