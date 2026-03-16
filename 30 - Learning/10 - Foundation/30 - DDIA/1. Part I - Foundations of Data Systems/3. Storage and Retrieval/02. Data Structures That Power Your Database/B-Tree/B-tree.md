---
Структура и принцип работы: "[[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/B-Tree/Структура и принцип работы B-tree|Структура и принцип работы B-tree]]"
Reliable: "[[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/B-Tree/Как обспечить Reliable (надежность) для B-tree|Как обспечить Reliable (надежность) для B-tree]]"
B-Tree VS LSM-Tree: "[[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/LSM-Tree VS B-Tree|LSM-Tree VS B-Tree]]"
Оптимизация: "[[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/B-Tree/Как можно оптимизировать B-tree|Как можно оптимизировать B-tree]]"
---
## Что за зверь такой?
Это самый распространенный индекс в базах данных, прошедший испытание времени. Его единственное сходство с [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/LSM-Tree/SSTables|SSTables]], в том что b-tree также хранит в себе ключи в отсортированном порядке.

B-tree индекс делит данные, не на [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02. Data Structures That Power Your Database/Сегментация логов для движка базы данных|cегменты]], а на *страницы(pages)*, обычно размером 4КБ. Такой дизайн больше похож на устройство диска, потому что тот также делиться на фиксированные по размеру блоки.

![[99 - Meta/02 - Медиа/Pasted image 20251025092830.png]]





