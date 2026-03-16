### Проблема
Это еще одна популярная аномалия *replication lag*, при использовании асинхронных реплик. И касается она нарушения причинно-следственной связи. Представим вот такой диалог между Mr. Poons and Mrs. Cake:

>\[Mr. Poons\]: How far into the future can you see, Mrs. Cake?
>\[Mrs. Cake\]: About ten seconds usually, Mr. Poons.

Тут мы видим причинно следственную связь между двумя предложенями: Mrs. Cake слышит вопрос и отвечает на него.

Теперь представим, что у Mrs. Cake минимальный лаг, а у Mr. Poons наоборот, большой лаг. Со стороны их диалог будет выглядеть уже вот так:

>\[Mrs. Cake\]: About ten seconds usually, Mr. Poons.
>\[Mr. Poons\]: How far into the future can you see, Mrs. Cake?

![[99 - Meta/02 - Медиа/Pasted image 20251112001357.png]]

### Гарантия *consistent prefix reads*
Чтобы избежать эту проблему, нам нужна гарантия *consistent perfix reads*: если последовательность записей была сделана в определенном порядке, то в таком же порядке ее должны читать все остальные.
Если в базка что-то в себя записывает в определенном порядке, читая ее мы будем видеть *consistent prefix*, и такой анамолии даже не произойдет. Но тем не менее, если данные у нас шардированы, шарды друг от друга независимы, а значит у нас нет глобального порядка записей.

### Решение
Одно из решений: *нужно быть уверенным, что все по смыслу связанные записи хранятся в одном и том же шарде*, но в некоторых приложения это нельзя сделать эффективно. Существуют также алгоритмы, которые явно отслеживают причинно-следственные зависимости ( [[30 - Learning/10 - Foundation/30 - DDIA/2 - Part II - Distributed Data/5 - Replication/4 - Leaderless Replication/Detecting Concurrent Writes#The "happened-before" Relationship and Concurrency | The "happened-before" Relationship and Concurrency]] )