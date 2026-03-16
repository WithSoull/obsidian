Это одна из вариаций графовой модели данных, похожа на [[ 01_Data Models/03_Graph/Property-graph model | Property-graph model ]], но тем не менее имеет некоторые отличия.
### Структура
1) subject
2) predicate
3) object

Например: `(Jim, likes, banana)`
- `Jim` -> subject
- `likes` -> predicate
- `banaba` -> object

Здесь subject эквивалентен вершине в графе. А вот объект это одно из двух:
1) свойство
   `(lucy, age, 33)` -> vertext `lucy` со свойством `{"age":33}`
2) другая вершина
   `(lucy, marriedTo, bob)`  -> vertext `lucy` соединена с vertext `bob` ребром `marriedTo`

![[99 - Meta/02 - Медиа/Pasted image 20251008231537.png]]

Вот так выглядят эти данные в формате _Turtle_, подмножества *Notation3*. (троек)
``` Turtle
@prefix : <urn:example:> .

_:lucy a :Person ;
  :name "Lucy" ;
  :bornIn _:idaho .

_:idaho a :Location ;
  :name "Idaho" ;
  :type "state" ;
  :within _:usa .

_:usa a :Location ;
  :name "United States" ;
  :type "country" ;
  :within _:namerica .

_:namerica a :Location ;
  :name "North America" ;
  :type "continent" .
```

Здесь вершина графа выражена как `_:someName`

### Semantic Web | RDF
Легко перемутать это все вместе, подробно описано [[ 01_Data Models/03_Graph/Semantic web & RDF | тут ]].
Если кратко, Semantic Web это попытка принудить сайты публиковать данные в машиночитаемом формате, але база знаний всего. А RDF это *Resourse Description Framework*. Все это дело не прижилось. Но в популярном языке запросов [[ 02_Query Languages/SPARQL | SPARQL ]] в основе лежит этот RDF.

## Triple Stores и производительность

### Сравнение Triple Stores

| Triple Store        | Тип         | Масштабируемость | SPARQL  | Особенности      | Связь с Semantic Web |
| ------------------- | ----------- | ---------------- | ------- | ---------------- | -------------------- |
| **Apache Jena/TDB** | Open Source | Средняя          | Да      | Java экосистема  | Прямая               |
| **GraphDB**         | Commercial  | Высокая (15B)    | Да      | Reasoning, BI    | Прямая               |
| **AllegroGraph**    | Commercial  | Высокая (1T+)    | Да      | Multi-master     | Прямая               |
| **Stardog**         | Commercial  | Высокая (50B)    | Да      | ML интеграция    | Прямая               |
| **Virtuoso**        | Commercial  | Очень высокая    | Да      | Универсальная DB | Прямая               |
| **Datomic**         | Commercial  | Высокая          | Datalog | Иммутабельность  | Независимая          |

### Архитектурные подходы
**Три основные архитектуры**:
- **In-memory** — быстрые операции, ограниченный объём
- **Native Store** — персистентное хранение, оптимизированное для RDF
- **Non-native Store** — использование реляционных СУБД как backend

**Современные возможности масштабирования**:
- AllegroGraph: 1+ trillion триплетов
- Stardog: до 50 billion триплетов  
- GraphDB/Virtuoso: до 15 billion триплетов

### Практические показатели производительности
**Query Performance** (milliseconds average):
- Relational DB: 6ms (baseline)
- AllegroGraph: 7ms (comparable to SQL)
- Blazegraph: 37ms
- Sesame: 58ms
- Jena: 1251ms

**Stability под нагрузкой**:
- GraphDB: наилучшие показатели стабильности (139 errors из 5,100 operations)
- Virtuoso: высокая производительность, но больше ошибок (4,732 errors)

## Выводы и рекомендации

### Выбор технологии
**Для внутренних приложений**: Triple stores полезны даже без Semantic Web интеграции благодаря:
- Гибкости эволюционных схем данных
- Эффективности работы со связными данными  
- Мощным возможностям inference и reasoning

**Критерии выбора triple store**:
- Требования к масштабируемости (объём данных)
- Сложность запросов и производительность
- Стабильность под нагрузкой
- Интеграция с существующей инфраструктурой

### Практические рекомендации
1. **Начинайте с Turtle** для человеко-читаемых RDF документов
2. **Используйте Apache Jena** для прототипирования и преобразований форматов
3. **Планируйте namespace strategy** заранее для production систем
4. **Тестируйте производительность** на реальных данных и запросах
5. **Рассматривайте CONSTRUCT** для сложных трансформаций данных

---
[[ 30 - Learning/10 - Foundation/30 - DDIA/0. PDFs of the book/DDIA-original.pdf#page=66&selection=116,0,116,24 | DDIA-original, page 55 - Triple-Stores and SPARQL ]]