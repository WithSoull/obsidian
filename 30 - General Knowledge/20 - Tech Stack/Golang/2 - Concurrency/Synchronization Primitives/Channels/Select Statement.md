### Базовые примеры
``` go
func async1() chan string {
	ch := make(chan string)
	go func() {
		time.Sleep(1 * time.Second)
		ch <- "async1 result"
	}()
	return ch
}

func async2() chan string {
	ch := make(chan string)
	go func() {
		time.Sleep(1 * time.Second)
		ch <- "async2 result"
	}()
	return ch
}

func main() {
	ch1 := async1()
	ch2 := async2()

	select { // <---------------------------------
	case result := <-ch1:
		fmt.Println(result)
	case result := <-ch2:
		fmt.Println(result)
	}
	
	// Как только мы прочитали какое-то значение, мы выходим из селекта
}
```
Как только мы прочитали какое-то значение и обработали тело `case`, мы выходим из `select`. Это означает что 1 `select` прочитает только одно значение из какого-то канала. Также у нас есть еще вариант установить `default` :
``` go
select {
case result := <-ch1:
	fmt.Println(result)
case result := <-ch2:
	fmt.Println(result)
default:
	fmt.Println("Exit from select by default")
}
```
Когда мы зашли в `select` и у нас нечего читать из каналов, то будет выполняться `default` и мы соответсвенно выйдем из канала. Если `default` нет, будем ждать пока кто-то запишет что-либо в канал.
###### select in loop with break and continue
``` go
func main() {
	data := make(chan int)
	go func() {
		for i := 1; i <= 4; i++ {
			data <- i
		}
		close(data)
	}()

	for {
		value := 0
		opened := true
		select {
		case value, opened = <-data:
			if value == 2 {
				continue // Для for: перейдем на след итер и снова окажемся в select
			} else if value == 3 {
				break    // Для select: выйдем из текущего select
			}
			if !opened {
				return   // Выход из функции в общем, чтобы не застрять в беск цикле
			}
		}
		fmt.Println(value)
	}
}
```

Это пример, который демонстрирует как мы може прочитать нескользко значений из нескольких каналов. Для это мы использум бесконечный `for`, и в теле этого цикла у нас здесь написаны `continue` и `break`, и `return`. Вот здесь неочивидный момент, который стоит запомнить.
- Внутри `select` можно писать только `break`, и тут он относится именно к `select`.
- Внутри `for` можно использовать `break` и `continue`

### Как обеспечить приоритетность в select?
``` go
for {
	select {
	case value := <-ch1:   // Пытаемся прочитать первый, более приоритетный канал
		fmt.Println(value)
	default:               // Если в канале нечего читать то просто выходим
	}

	select {
	case value := <-ch1:  // Пытаемся еще раз прочитать первый канал
		fmt.Println(value)
		return
	case value := <-ch2:  // Если в 1-ом канале ничего нет, то читаем второй
		fmt.Println(value)
	}
}
```

Можно использовать вот такой паттерн, в котором у нас больший приоритет на канал `ch1`. Здесь безусловно может произойти такая ситуация, что во втором канале тоже выпадет второй select, но вероятность мала и ей можно принебречь.

Чтобы задать какой-то *вес*, мы можем просто написать несколько раз `case`:
``` go
func main() {
	ch1 := make(chan struct{}, 1)
	ch2 := make(chan struct{}, 1)

	close(ch1)
	close(ch2)

	ch1Value := 0.0
	ch2Value := 0.0

	for i := 0; i < 100000; i++ {
		select {
		case <-ch1:
			ch1Value++
		case <-ch1:
			ch1Value++
		case <-ch2:
			ch2Value++
		}
	}

	fmt.Println(ch1Value / ch2Value) // 2.0185945423810674
}
```