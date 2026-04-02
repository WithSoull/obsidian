Для сложных *many-to-many* отношений графовая модель подходит отлично, хотя для не особо сложных подходит нормализованная relational модель. Если связи в основном *one-to-many*(tree-structered data), то документо-ориентированная модель бы хорошо вписалась.

У графа есть:
1) *Vertices* - nodes / entities / вершины
2) *Edges* - relationships / arcs / ребра

Graphs не ограниченны однородным типом данных: это мощная возможность данной модели данных, которая позволяет хранить разные типы объектов в одном хранилище.

Напимер Facebook:
1) Verices: люди, локации, события, комментарии пользователей
2) Edges: друзья, кто комментирует какой пост, кто добавил какое событие

![[99 - Meta/02 - Медиа/Pasted image 20251008192025.png]]

Есть разные способы структурировать данные и строить запросы в графах, как минимум потомучто есть разные виды графов:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/01 - Data Models/03 - Graph/Property Graph Model|Property model]] (реализованная Neo4j, Titan и InfiniteGraph)
- [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/01 - Data Models/03 - Graph/Triple-Store Model|Triple-store model]] (реализованная Datomic, AllegroGraph и другие)

Есть разные языки запросов:
- декларативные:
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/02 - Query Languages/Cypher|Cypher]] - язык для [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/01 - Data Models/03 - Graph/Property Graph Model|property-graph model]], а конкретно Neo4j
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/02 - Query Languages/SPARQL|SPARQL]] - язык запросов для [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/01 - Data Models/03 - Graph/Triple-Store Model|triple-store model]], которые используют [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/01 - Data Models/03 - Graph/Semantic Web & RDF#^840081|RDF]]. 
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/02 - Query Languages/Datalog|Datalog]] - язык запросов для Datomic
	- [[public/30 - Learning/10 - Foundation/30 - DDIA/3 - Data Models and Query Languages/02 - Query Languages/Graph Queries in SQL|SQL]] - с болью, но можно
- имеративные:
	- Gremlin
- фреймворки:
	- Pregel

##### Graph Databases vs CODASYL Network Model

###### Общий вопрос
На первый взгляд, сетевая модель CODASYL похожа на графовые базы данных. Являются ли графовые БД "вторым пришествием" CODASYL? **Нет** — есть важные различия.

###### Ключевые различия

| Аспект                   | CODASYL Network Model                                                             | Graph Databases                                                                               |
| ------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Схема**                | Жёсткая схема определяла, какой тип записи может быть вложен в какой другой       | Нет ограничений — любая вершина может иметь рёбро к любой другой вершине                      |
| **Гибкость**             | Низкая — изменения схемы сложны                                                   | Высокая — легкая адаптация к изменяющимся требованиям                                         |
| **Доступ к данным**      | Единственный способ — пройти один из access paths                                 | Прямой доступ по уникальному ID или через индексы по значению                                 |
| **Упорядочивание**       | Дочерние записи — упорядоченное множество, БД поддерживает порядок                | Вершины и рёбра не упорядочены (сортировка только при запросе)                                |
| **Вставка данных**       | Приложения должны заботиться о позициях новых записей в множествах                | Нет необходимости заботиться о порядке при вставке                                            |
| **Языки запросов**       | Все запросы императивные, сложные в написании, легко ломались при изменении схемы | Поддержка как императивного кода, так и высокоуровневых декларативных языков (Cypher, SPARQL) |
| **Сложность разработки** | Высокая — сложные запросы, хрупкость к изменениям                                 | Низкая — декларативные запросы, устойчивость к изменениям                                     |

---
[[30 - Learning/10 - Foundation/30 - DDIA/0 - Book PDFs/DDIA-original.pdf#page=61&selection=0,0,0,22|DDIA-original, page 49 - Graph-like Models]]
