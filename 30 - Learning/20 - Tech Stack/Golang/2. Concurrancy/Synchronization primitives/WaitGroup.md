## API
![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-18 в 14.55.03.png]]

Метод Add() можно в целом использовать как Done(), если передать туда `-1`.

# Код
### Цикл с горутинами
#### **Примерное** решение
``` go
func main() {
	var wg sync.WaitGroup

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			log.Printf("test %d", i)
			wg.Done()
		}()
	}

	wg.Wait()
}
```

``` output
2025/09/18 15:10:26 test 0
2025/09/18 15:10:26 test 4
2025/09/18 15:10:26 test 3
2025/09/18 15:10:26 test 1
2025/09/18 15:10:26 test 2

```

Так можно использовать waitGroup, для того чтобы дождаться выполнения всех горутин.

>[!danger] wg.Add(1)
>Тут очень важно написать эту строчку до создания горутины, иначе если написать это внутри горутины, тогда горутина просто создаться, а запуститься она не сразу

#### **Правильное** решение
``` go
func main() {
	var wg sync.WaitGroup

	wg.Add(5)
	for i := 0; i < 5; i++ {
		go func() {
			defer wg.Done()
			log.Println("test")
		}()
	}

	wg.Wait()
}

```

Тут два важных изменения:
1) чтобы не забыть `wg.Done()`, засунем его в `defer`
2) *Инкремент атомарной переменной* в *15* раз **медленнее**, чем обычной, поэтому здесь по возможности стоит поэкономить, поэтому мы выносим `wg.Add()` до цикла и передаем ему `5`
#### А как сделать последовательное выполнение горутин?
``` go
func main() {
	var wg sync.WaitGroup

	wg.Add(5)
	for i := 0; i < 5; i++ {
		go func() {
			defer wg.Done()
			log.Printf("test %d", i)
		}()
	}

	wg.Wait()
}
```

``` ouput
2025/09/18 15:11:59 test 0
2025/09/18 15:11:59 test 1
2025/09/18 15:11:59 test 2
2025/09/18 15:11:59 test 3
2025/09/18 15:11:59 test 4
```

Для этого можно ждать завершения всех горутин внутри цикла, т. е. мы инкриментируем счетчик, ждем декремент, и так по кругу

### Операции над waitgroup
#### Отрицательное значение счетчика
```go
func main() {
	wg := sync.WaitGroup{}
	wg.Add(-10)
}
```

``` output
panic: sync: negative WaitGroup counter

goroutine 1 [running]:
sync.(*WaitGroup).Add(0x14000052738?, 0x1007627e8?)
        /opt/homebrew/Cellar/go/1.24.1/libexec/src/sync/waitgroup.go:64 +0x104
main.main()
        /Users/grishinid/home/01_Coding/concurrency_go/lessons/3_lesson_sync_primitives_1/03_wait_group_operations/main.go:17 +0x2c
exit status 2
```

Пакет sync устоен так, что когда мы его используем в нетривиальном сценарии(контр-интуитивные операции), он *чаще всего* выкидывает панику. Ну очевидно, что счетчик внутри waitGroup не должен быть меньше нуля.

#### Нулевое значение счетчика
``` go
func main() {
	wg := sync.WaitGroup{}
	wg.Wait()
}
```

Счетчик не блокируется и идет дальше, ничего не происходит. Логично!

#### Копирование WaitGroup
``` go
func done(wg sync.WaitGroup) {
	wg.Done()
}

func main() {
	wg := sync.WaitGroup{}
	wg.Add(1)
	done(wg)
	wg.Wait()
}
```

``` output
fatal error: all goroutines are asleep - deadlock!

goroutine 1 [sync.WaitGroup.Wait]:
sync.runtime_SemacquireWaitGroup(0x14000052701?)
        /opt/homebrew/Cellar/go/1.24.1/libexec/src/runtime/sema.go:110 +0x2c
sync.(*WaitGroup).Wait(0x1400000e0a0)
        /opt/homebrew/Cellar/go/1.24.1/libexec/src/sync/waitgroup.go:118 +0x70
main.main()
        /Users/grishinid/home/01_Coding/concurrency_go/lessons/3_lesson_sync_primitives_1/04_wait_group_copying/main.go:13 +0x64
exit status 2
```

Такое происходит, видим, что произошел *дедлок*, потому что мы в функцию `done()` передали копию нашей `wg`.
`wg` из `main()` осталась с счетчиком 1, и дальше она бы нигде не задекрементилась, поэтому рантайм выкинул дедлок.

Чтобы решить эту проблему, нужно просто передавать `wg` по ссылке.

# Важная цитата от разрабов го
>[!quote] Values containing the types defined in this package should not be copied!

