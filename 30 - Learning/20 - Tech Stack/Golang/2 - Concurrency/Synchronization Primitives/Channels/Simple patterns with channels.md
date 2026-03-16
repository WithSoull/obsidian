### Как попробовать записать/прочитать из канала?
```go
func tryToReadFromChannel(ch chan string) (string, bool) {
	select {
	case value, isOpen := <-ch:
		return value, isOpen == true
	default:
		return "", false
	}
}

func tryToWriteToChannel(ch chan string, value string) bool {
	select {
	case ch <- value: // <--- Если будет закрыт канал, получим панику
		return true
	default:
		return false
	}
}
```

### Как проверить закрыт канал или нет?
``` go
func IsClosed(ch chan int) bool {
	select {
	case _, opened := <-ch: // <--- Вот тут мы заберем значение из канала,
					        //      что не очень хорошо
		return !opened
	default:
		return false
	}
}
```

Тут надо учитывать что, мы можем *забрать значение* из канала и не обработать его, поэтому лучше так не писать и использовать `tryToReadFromChannel()` из примера выше.