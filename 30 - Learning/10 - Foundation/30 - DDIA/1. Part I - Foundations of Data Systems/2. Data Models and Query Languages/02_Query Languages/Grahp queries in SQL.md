Вот тут мы уже представляли графовую модель в виде SQL - [[Property-graph model#^1a4bda|SQL запрос на создание]]

Графовые обходы с переменной длиной рёбер удобно выражаются в специализированных языках вроде [[Cypher|Cypher]], а в SQL их приходится моделировать через рекурсивные CTE (*recursive common table expressions (* **WITH RECURSIVE** *))*, что работает, но громоздко и требует осторожности с производительностью и циклами.

Вот пример такого запроса
```postgresql
WITH RECURSIVE
  -- in_usa is the set of vertex IDs of all locations within the United States
  in_usa(vertex_id) AS (
    SELECT vertex_id
    FROM vertices
    WHERE properties->>'name' = 'United States'
    UNION
    SELECT edges.tail_vertex
    FROM edges
    JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
    WHERE edges.label = 'within'
  ),

  -- in_europe is the set of vertex IDs of all locations within Europe
  in_europe(vertex_id) AS (
    SELECT vertex_id
    FROM vertices
    WHERE properties->>'name' = 'Europe'
    UNION
    SELECT edges.tail_vertex
    FROM edges
    JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
    WHERE edges.label = 'within'
  ),

  -- born_in_usa is the set of vertex IDs of all people born in the US
  born_in_usa(vertex_id) AS (
    SELECT edges.tail_vertex
    FROM edges
    JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
    WHERE edges.label = 'born_in'
  ),

  -- lives_in_europe is the set of vertex IDs of all people living in Europe
  lives_in_europe(vertex_id) AS (
    SELECT edges.tail_vertex
    FROM edges
    JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
    WHERE edges.label = 'lives_in'
  )

SELECT vertices.properties->>'name'
FROM vertices
JOIN born_in_usa ON vertices.vertex_id = born_in_usa.vertex_id
JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;
```
---
[[ 30 - Learning/10 - Foundation/30 - DDIA/0. PDFs of the book/DDIA-original.pdf#page=64&selection=126,0,126,20 | DDIA-original, page 53 - Graph Queries in SQL ]]
