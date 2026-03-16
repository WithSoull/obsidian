## Context Switching
Потокам ОС системы нужно переодически переключаться с одного потока на другой. Основная проблема заключается в [[30 - Learning/10 - Foundation/10 - CPU Arch/Threads and Processes#^b32443|2х Context Switching]]

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-16 в 07.23.17.png]]

У легковесного потока есть такой же контекст как и у потока ОС, т. е. набор регистров и стек. При переключение контекста регистры пушатся на стек. И из-за того что мы не переключаемя в _kernel-space_ горутину называют легковесным потоком (это первая причина, вторая в размере горутины, об этом будет ниже)

Переключение легковесных потоков происходит в *user-space*, этим занимается пользовательское приложение.

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-17 в 22.48.18.png]]

>[!done] Ключевая идея языка Go в concurrancy
> 1) Не даем в руки программисту поток
> 2) Делаем вид, что есть только горутины
> 3) Всю сложность распределения горутин абстрагируем

# Примеры кода
## runtime.NumGoroutine()
``` go 
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Printf("Goroutines: %d\n", runtime.NumGoroutine())
}
```

``` Output
Goroutines: 1
```

Возвращает 1 потому, что весь наш код был запущен в одной горутине, которую часто именуют _main_ горутиной.

---

``` go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	for i := 0; i < 10; i++ {
		go func() {
			fmt.Print(i)
		}()
	}
	fmt.Printf("Goroutines: %d\n", runtime.NumGoroutine())
}
```

``` output
Goroutines: 11
```

Возвращает 11, потому что до этого мы запустили. А иногда успевает вывести некоторые числа из цикла.


## TCP server с паникой

``` go 
package main

import (
	"errors"
	"log"
	"net"
)

// nc 127.0.0.1 12345

func main() {
	listener, err := net.Listen("tcp", ":12345")
	if err != nil {
		log.Fatal(err)
	}

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println(err)
		}

		go ClientHandler(conn)
	}
}

func ClientHandler(c net.Conn) {
	panic(errors.New("internal error"))
}
```

``` input
nc 127.0.0.1 12345
```

``` output
panic: internal error

goroutine 35 [running]:
main.ClientHandler(...)
        /Users/grishinid/home/01_Coding/concurrency_go/lessons/2_lesson_gorutines_and_scheduler/02_tcp_server_with_panic/main.go:28
created by main.main in goroutine 1
        /Users/grishinid/home/01_Coding/concurrency_go/lessons/2_lesson_gorutines_and_scheduler/02_tcp_server_with_panic/main.go:23 +0x7c
exit status 2
```

---

Падает потому что, **паника в одной из горутин аффектит все приложение**

## TCP без паники
``` go
package main

import (
	"log"
	"net"
)

// nc 127.0.0.1 12345

func main() {
	listener, err := net.Listen("tcp", ":12345")
	if err != nil {
		log.Fatal(err)
	}

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println(err)
		}

		go ClientHandler(conn)
	}
}

func ClientHandler(c net.Conn) {
	defer func() {
		if v := recover(); v != nil {
			log.Println("captured panic:", v)
		}
		c.Close()
	}()

	panic("internal error")
}
```

``` input
nc 127.0.0.1 12345
```

``` output
2025/09/17 22:58:58 captured panic: internal error
```

---

В рамках обработчика нужно сделать **recover()**, чтобы поймать панику

## Worker ИЛИ как восстановить горутину после паники
``` go
package main

import (
	"log"
	"time"
)

func task() {
	for {
		time.Sleep(time.Millisecond * 200)
		panic("unexpected situation")
	}
}

func NeverExit(name string, action func()) {
	defer func() {
		if v := recover(); v != nil {
			log.Println(name, "is crashed - restarting...")
			go NeverExit(name, action)
		}
	}()

	if action != nil {
		action()
	}
}

func main() {
	go NeverExit("first_goroutine", task)
	go NeverExit("second_goroutine", task)

	time.Sleep(time.Second)
}
```

``` output
2025/09/17 23:02:43 first_goroutine is crashed - restarting...
2025/09/17 23:02:43 second_goroutine is crashed - restarting...
2025/09/17 23:02:43 second_goroutine is crashed - restarting...
2025/09/17 23:02:43 first_goroutine is crashed - restarting...
2025/09/17 23:02:43 second_goroutine is crashed - restarting...
2025/09/17 23:02:43 first_goroutine is crashed - restarting...
2025/09/17 23:02:44 first_goroutine is crashed - restarting...
2025/09/17 23:02:44 second_goroutine is crashed - restarting...
```

---

Этот паттерн называется **NeverExit**, во время `recover()` нам нужно просто заново запустить эту горутину

>[!warning] `log.Print()`  VS  `fmt.Print()`
>Операции в пакете **_log_** _синхронизируются_, поэтому сообщения, напечатанные двумя горутинами не будут перепутаны/перемешаны
## Паника с другой горутины
``` go
package main

import (
	"fmt"
	"time"
)

func process() {
	defer func() {
		v := recover()
		fmt.Println("recovered:", v)
	}()

	go func() {
		panic("error")
	}()

	time.Sleep(time.Second)
}

func main() {
	process()
}
```

``` input
panic: error

goroutine 34 [running]:
main.process.func2()
        /Users/grishinid/home/01_Coding/concurrency_go/lessons/2_lesson_gorutines_and_scheduler/05_panic_from_other_goroutine/main.go:15 +0x2c
created by main.process in goroutine 1
        /Users/grishinid/home/01_Coding/concurrency_go/lessons/2_lesson_gorutines_and_scheduler/05_panic_from_other_goroutine/main.go:14 +0x40
exit status 2
```

--- 

>[!danger] Здесь очень важный момент, панику нельзя перехватить из другой горутины
>Тут мы попытались перехватить панику из main горутины, но тем не менее отловить ее у нас не получилось. 
>
>У каждой горутины *свой* *стек*, поэтому разматываясь стек не доходит до `recover` просто, потому что в этом стеке `recover` просто нет
>

## Цикл с индексем с горутинами
``` go
package main

import (
	"fmt"
	"time"
)

func main() {
	for i := 0; i < 5; i++ {
		go func() {
			log.Printf("log print -> %d ", i)
		}()
	}
	time.Sleep(2 * time.Second)
}
```

``` output
2025/09/17 23:24:42 log print -> 1
2025/09/17 23:24:42 log print -> 0
2025/09/17 23:24:42 log print -> 4
2025/09/17 23:24:42 log print -> 3
2025/09/17 23:24:42 log print -> 2
```

---

До версии Go 1.22 в цикле не создавалась переменная каждую итерацию, использовалась всегда одна, и это означает, что происходит замыкание переменной
Грубо говоря, цикл успевал прогнать несколько итераций, только потом стартовала первая горутина, но она выводила значение i такое какое было в тот момент, а не то, которое в нее попало

Чтобы избежать этого достаточно добавить `i := i` или передавать в функцию `i` как аргумент.

>[!warning]  Недетерминированность
>Также как планировщик ОС, планировщик Go недетерминированный, а значит мы не можем предсказать в каком порядке будут запущены горутины.
## Endless loop
``` go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	runtime.GOMAXPROCS(1) // условно указываем, что наш код будет исполняться на одном ядре

	var i int
	go func() {
		for {
			i++
		}
	}()

	fmt.Println(i)
}
```

``` output
0
```

---

Тут горутина даже не успевает стартануть, потому что еще не законила работу первая main горутина, а горутина с циклом даже не успевает стартануть. Даже если там поспать, все равно будет выходить 0, очевидно.

>[!danger] Создание горутны != Запуск горутины

# Размер стека горутины
Горутину еще называют легковесной, потому что минимальный размер ее стека равен 2kB. При этом можно алоцировать стек горутины где угодно, хоть в heap'е 

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-17 в 23.51.20.png]]

Если нам не хватало стека, выделялся новый стек, и связывалось все это дело как _связный список_. Такой стек себя не зарекомендовал, потому что стек, это _кэш-дружелюбная_ структура, ведь данные расположены последовательно, а здесь это условие нарушается. Соответсвенно это уже _некэш-локально_. 
Еще одна проблема, _hotspot_. Представим ситуацию с тяжелой функцией, когда мы в нее заходим на не хватает размера стека и мы алоцируем новый кусок, а затем, по завершении функции удаляем его из-за ненадобности. А потом заново заходим в функцию :)

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-17 в 23.55.56.png]]
Придумали вот такую концепцию, работает как динамический массив, база. Только здесь стек может сужаться вполовину, когда меньше 25% занято.

## Какой максимальный размер стекa

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-17 в 23.57.52.png]]

---

>[!quote] «So, it is not a problem for a Go program to maintain tens of thousands goroutines at the same time, as long as the system memory is sufficient»

