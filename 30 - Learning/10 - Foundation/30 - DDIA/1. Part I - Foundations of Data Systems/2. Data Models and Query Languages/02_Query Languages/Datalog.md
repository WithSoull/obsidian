- Старше чем [[SPARQL|SPARQL]] и [[Cypher|Cypher]]
- Разработан в 1980х
- Фундамент для языков запросов
- Используется в Datomic
- Casalog это Datalog реализация для огромных запросов в Hadoop.

``` datalog
name(namerica, 'North America').
type(namerica, continent).

name(usa, 'United States').
type(usa, country).
within(usa, namerica).

name(idaho, 'Idaho').
type(idaho, state).
within(idaho, usa).

name(lucy, 'Lucy').
born_in(lucy, idaho).
```

![[99 - Meta/02 - Медиа/Pasted image 20251009001638.png]]
Здесь ключевой смысл в том, что мы маленькими шагами определяем правила:
1) within_recurisve(Location, Name) ищет вершину *subject* `Location` связанную с *object* `Name` с помощью *predicate* `Name`
2) within_recurisve(Location, Name) ищет делает это рекуксивно
3) migrated опрделяет оставшиеся правила
![[99 - Meta/02 - Медиа/Pasted image 20251009163519.png]]

Этот язык стал основой для других, потому что использует мощный подход, потому что правила можно комбинировать и переиспользовать в других запросах.

---
[[ 30 - Learning/10 - Foundation/30 - DDIA/0. PDFs of the book/DDIA-original.pdf#page=71&selection=28,0,28,23 | DDIA-original, page 60 - The Foundation: Datalog ]]
