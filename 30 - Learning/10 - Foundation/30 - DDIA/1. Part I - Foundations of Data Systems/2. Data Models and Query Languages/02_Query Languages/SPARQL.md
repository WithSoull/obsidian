**SPARQL** — язык запросов для [[Triple-store model|triple-store]] с [[Semantic web & RDF|RDF]] моделью данных. Расшифровывается как **SPARQL Protocol and RDF Query Language**.
## Связь с [[Cypher|Cypher]]

SPARQL появился **раньше Cypher**, и Cypher заимствовал pattern matching из SPARQL. Поэтому синтаксис очень похож:

**Cypher:**
```cypher
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location)
```

**SPARQL:**
```sparql
?person :bornIn / :within* ?location.
```

Но тем не менее синтаксис смахивает и на SQL немного:
```sparql
PREFIX : <urn:example:> # Как раз тот урл из Sematic Web

SELECT ?personName WHERE { 
	?person :name ?personName. 
	?person :bornIn / :within* / :name "United States". 
	?person :livesIn / :within* / :name "Europe". 
}
```
## Ключевые особенности
- **Переменные** начинаются с `?` (например, `?person`, `?location`)
- **Унифицированный синтаксис**: RDF не различает свойства и рёбра — использует предикаты для обоих случаев
- **Компактность**: запросы часто более лаконичны чем в Cypher

## Практическое применение
SPARQL — **мощный инструмент для внутренних приложений**, даже если Semantic Web не материализуется. Подходит для:
- Запросов к RDF данным
- Pattern matching по графовым структурам  
- Работы с triple stores

**Вывод**: SPARQL полезен независимо от судьбы Semantic Web как эффективный язык запросов для графовых данных в RDF формате.

---
[[ 30 - Learning/10 - Foundation/30 - DDIA/0. PDFs of the book/DDIA-original.pdf#page=70&selection=0,0,0,25 | DDIA-original, page 59 - The SPARQL query language ]]
