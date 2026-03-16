>[!question] На каком уровне работаю мьютексы в Go?
>![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.08.12.png]]
>![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.08.26.png]]
>
>Если бы у нас гошные мьютексы работали на уровне ОС, то мы бы блокировали поток ОС, тем самым никакие другие горутины там бы не смогли исполняться. Поэтому в Go свой мьютекс (легковесный хахаха)

### Куда девать горутины, которые были заблокированы?

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.11.08.png]]

Особенность этой очереди в том, что эти горутины в статусе **waiting**

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.11.56.png]]

Это вот так выглядит мьютекс в ядре линукс

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.12.27.png]]

Здесь у каждого мьютекса есть указатель на список P, которые будут блокироваться этим мьютексом.

А вот как реализованы дерево для wait queue в го:
``` go
// Asynchronous semaphore for sync.Mutex.

// A semaRoot holds a balanced tree of sudog with distinct addresses (s.elem).
// Each of those sudog may in turn point (through s.waitlink) to a list
// of other sudogs waiting on the same address.
// The operations on the inner lists of sudogs with the same address
// are all O(1). The scanning of the top-level semaRoot list is O(log n),
// where n is the number of distinct addresses with goroutines blocked
// on them that hash to the given semaRoot.
// See golang.org/issue/17953 for a program that worked badly
// before we introduced the second level of list, and
// BenchmarkSemTable/OneAddrCollision/* for a benchmark that exercises this.
type semaRoot struct {
	lock  mutex
	treap *sudog        // root of balanced tree of unique waiters.
	nwait atomic.Uint32 // Number of waiters. Read w/o the lock.
}

var semtable semTable
```

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.26.01.png]]

>[!danger] Надо переосмыслить, ничего не понял
> Если у нас мьютекс заблокирован, мы идем в глобальный пул, находим тот мьютекс на которые нужно повесить горутину и добавляем в список горутину, что она заблокирована

### Не будет ли горутины голодать в этой очереди?
 ![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.31.04.png]]

Когда 1-ый мьютекс разблокируется, пока 3-ий голодающий дойдет до лока, ему же там надо в *ready* перейти, 2-ая горутина может успеть захватить лок.

![[99 - Meta/02 - Медиа/Снимок экрана 2025-09-19 в 12.33.03.png]]

Это режим голодания (режим мьютекса), 1-ая горутина _абстрактно_ передает владение мьютекса 2-ой горутине. Таким образом, 3-ий не сможет захвотить лок.