>[!info] Условная переменная
>Примитив синхронизация, обеспечивающий блокирование одного или нескольких потоков до момента поступления сигнала от другого потока о выполнении некоторого условия.

### API
``` go
type Cond struct {
	L Locker
}

func NewCond(l Locker) *Cond // создает Cond с использованием мьютекса

func (c *Cond) BroadCast()   // оповещает все горутины
func (c *Cond) Signal()      // оповещает одну горутину
func (c *Cond) Wait()        // ожидает наступления сигнала
```

### Что происходит внутри `Wait()`?
``` go
c.checker.check()
t := runtime_notifyListAdd(&c.notify)
c.L.Unlock()
runtime_notifyListWait(&c.notify, t)
c.L.Lock()
```

### Примеры
###### subscriber & publisher
Тут мы всегда зависаем на subcriber, пока данные не запишутся в словарь. И когда мы записываем данные в словарь (под лочкой), мы вызываем `c.Broadcast()`,  оповещая таким образом двух subscriber'ов.
``` go
func subscribe(name string, data map[string]string, c *sync.Cond) {
	c.L.Lock()
	for len(data) == 0 {
		c.Wait() // Внутри мьютекс снова анлочится, ждет, и потом лочится
	}
	log.Printf("[%s] %s\n", name, data["key"])
	c.L.Unlock()
}

func publish(name string, data map[string]string, c *sync.Cond) {
	time.Sleep(time.Second)
	c.L.Lock()
	data["key"] = "value"
	c.L.Unlock()
	log.Printf("[%s] data publisher\n", name)
	c.Broadcast()
}

func main() {
	data := map[string]string{}
	cond := sync.NewCond(&sync.Mutex{})
	wg := sync.WaitGroup{}
	wg.Add(3)
	go func() {
		defer wg.Done()
		subscribe("subscriber_1", data, cond)
	}()
	go func() {
		defer wg.Done()
		subscribe("subscriber_2", data, cond)
	}()
	go func() {
		defer wg.Done()
		publish("publisher", data, cond)
	}()
	wg.Wait()
}

```
###### Краевые случаи
``` go
func waitWithoutLock() {
	// при вызове будет паника, потому что внутри Wait()
	// мы пытаемся освободить лочку, а она и так никем не захвачена

	cond := sync.NewCond(&sync.Mutex{})
	cond.Wait() // fatal error: sync: unlock of unlocked mutex
}

// Если вызвать Signal() перед Wait(), то
// мы мы не получим этот сигнал

// В этом примере main-горутина останется висеть
// поэтому тут будет deadlock
func waitAfterSignal() {
	cond := sync.NewCond(&sync.Mutex{})

	cond.Signal()

	cond.L.Lock()
	cond.Wait() // fatal error: all goroutines are asleep - deadlock!
	cond.L.Unlock()
}

```

### Почему нужно ждать в цикле?
``` go
c.L.Lock()
for !condition() {
	c.Wait()
}
// make use of condition ...
c.L.Unlock()
```

Пока горутина спит, *условие может поменять свое значение*, поэтому нужно его проверять также после выхода из сна. Нужно быть готовым к тому что, код может меняться, сегодня это условие не нужно проверять повторно, а завтра нужно. 

>[!danger] SPURIOUS WAKEUP
>В вычислениях **ложное пробуждение** происходит, когда поток просыпается после ожидания условной переменной без удовлетворения этой переменной. Его называют ложным, потому что поток, по-видимому, был разбужен без всякой причины

### Чем это отличается от каналов?
С каналами мы можем оповестить все горутины закрыв канал, но при этом **закрыть канал можно только один раз**. А вот `cond.Broadcast()` можно вызывать несколько раз.