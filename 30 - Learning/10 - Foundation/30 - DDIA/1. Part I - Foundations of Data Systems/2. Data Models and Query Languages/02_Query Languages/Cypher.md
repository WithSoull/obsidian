>[!info] Это *декларативный* язык для [[ 01_Data Models/03_Graph/Property-graph model | property-graph модели ]]
>Был создан для Neo4j graph db
>

![[99 - Meta/02 - Медиа/Pasted image 20251008221555.png]]

### Пример запроса
##### Создание новых вершин и ребер
``` cypher
CREATE
	(NAmerica:Location {name:'North America', type:'continent'}),
	(USA:Location {name:'United States', type:'country' }),
	(Idaho:Location {name:'Idaho', type:'state' }),
	(Lucy:Person {name:'Lucy' }),
	(Idaho) -[:WITHIN]-> (USA) -[:WITHIN]-> (NAmerica),
	(Lucy) -[:BORN_IN]-> (Idaho)
```
##### Поиск всех людей, которые эмигрировали из USA в EU
Здесь мы хотим найти все вершины, которые через `BORN_IN` ребро соединяются с локацией внутри США, а так же через ребро `LIVING_IN` с вершиной локации внутри Европы.
``` cypher
MATCH
	(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name:'United States'}),
	(person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (eu:Location {name:'Europe'})
RETURN person.name
```

Здесь `:WITHIN*0..` выражение означает следуй по графу 0 или больше раз.

Запрос формулирует два независимых условия достижимости: от рёбер `BORN_IN` и `LIVES_IN` через *транзитивное замыкание* `WITHIN` нужно прийти к целевым вершинам “United States” и “Europe”, после чего вернуть имя человека.

Выполнение может стартовать либо от вершин Person с последующей фильтрацией путей, либо от вершин `Location` с обратным расширением по входящим `WITHIN` и присоединением людей через входящие `BORN_IN/LIVES_IN`. **Оптимизатор выберет план по статистикам и индексам**.

###### Ключевые идеи
- Выражается шаблон графа с двумя путями от одной вершины Person к двум различным корневым локациям через произвольную длину WITHIN.
- Индексы по свойству name у локаций и по концам рёбер (head/tail) позволяют выбирать селективный начальный набор и эффективно выполнять обход.
- Декларативность скрывает план: разработка фокусируется на описании соответствия шаблону, а не на порядке соединений и направлений обхода.

---
[[ 30 - Learning/10 - Foundation/30 - DDIA/0. PDFs of the book/DDIA-original.pdf#page=63&selection=12,0,12,25 | DDIA-original, page 52 - The Cypher Query Language ]]