>[!danger]  tl;dr
>Чтобы в `select` не читать дефолтные значения из закрытого канала, мы можем сделать этот канал `nil`

Рассмотрим, зачем разработчики го добавили nil каналы на следующем примере:
``` go
package main

import (
	"fmt"
	"sync"
)

func WaitToClose(lhs, rhs chan struct{}) {
	lhsClosed, rhsClosed := false, false
	for !lhsClosed || !rhsClosed {
		select {
		case _, ok := <-lhs:
			fmt.Println("lhs", ok)
			if !ok {
				lhsClosed = true
			}
		case _, ok := <-rhs:
			fmt.Println("rhs", ok)
			if !ok {
				rhsClosed = true
			}
		}
	}
}

func main() {
	lhs := make(chan struct{}, 1)
	rhs := make(chan struct{}, 1)

	wg := sync.WaitGroup{}
	wg.Add(1)

	go func() {
		defer wg.Done()
		WaitToClose(lhs, rhs)
	}()

	lhs <- struct{}{}
	rhs <- struct{}{}

	close(lhs)
	close(rhs)

	wg.Wait()
}
```

В этом примере, мы ожидаем что у нас будет примерно такой вывод:
``` output
lhs
rhs
```

Но мы ловим вот такой вывод:
```
rhs true
rhs false
lhs true
rhs false
rhs false
rhs false
lhs false
```

Это происходит потому что вот в этом кусочке, мы можем прочитать "дефолтное" значение из канала после его закрытия:
``` go
select {
case _, ok := <-lhs:
	fmt.Println("lhs", ok)
	if !ok {
		lhsClosed = true
	}
case _, ok := <-rhs:
	fmt.Println("rhs", ok)
	if !ok {
		rhsClosed = true
	}
}
```
И чтобы это исправить, чтобы мы перестали читать дефолтные значения из каналов, нам нужно присвоить nil каждый канал после того, как мы убедились что он закрыт:
``` go
select {
case _, ok := <-lhs:
	fmt.Println("lhs", ok)
	if !ok {
		lhsClosed = true
		lhs = nil
	}
case _, ok := <-rhs:
	fmt.Println("rhs", ok)
	if !ok {
		rhsClosed = true
		rhs = nil
	}
}
```
