Работает также как и в реальной жизни.
По принципу Первый вошел, первый вышел - **FiFo**(_First in First out_)

- На Python:
	```python
	from collections import deque
	
	q = deque([...])
	q.append(1) # добавляет в конец 1
	q.popleft() # удаляет первый элемент и возвращает его
	```