---
Структура и принцип работы: "[[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/B-Tree/How B-Tree Works|Структура и принцип работы B-tree]]"
Reliable: "[[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/B-Tree/How to Ensure Reliability in B-Tree|Как обспечить Reliable (надежность) для B-tree]]"
B-Tree VS LSM-Tree: "[[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/LSM-Tree vs B-Tree|LSM-Tree VS B-Tree]]"
Оптимизация: "[[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/B-Tree/How to Optimize B-Tree|Как можно оптимизировать B-tree]]"
---
## Что за зверь такой?
Это самый распространенный индекс в базах данных, прошедший испытание времени. Его единственное сходство с [[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/LSM-Tree/SSTables|SSTables]], в том что b-tree также хранит в себе ключи в отсортированном порядке.

B-tree индекс делит данные, не на [[public/30 - Learning/10 - Foundation/30 - DDIA/4 - Storage and Retrieval/02 - Data Structures That Power Your Database/Log Segmentation for Storage Engines|cегменты]], а на *страницы(pages)*, обычно размером 4КБ. Такой дизайн больше похож на устройство диска, потому что тот также делиться на фиксированные по размеру блоки.

![[99 - Meta/02 - Медиа/Pasted image 20251025092830.png]]





