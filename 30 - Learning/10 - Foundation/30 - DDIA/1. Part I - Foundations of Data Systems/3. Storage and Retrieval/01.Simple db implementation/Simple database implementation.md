## Самое простое что можно сделать
``` bash
#!/bin/bash
db_set () {
	echo "$1,$2" >> database
}

db_get () {
	grep "^$1," database | sed -e "s/^$1,//" | tail -n 1
}
```

Тут у нас всего две функции, которые реализовывают key-value хранилище. Запросы можно будет делать вот так: 
``` bash
db_set 123456 '{"name":"London","attractions":["Big Ben","London Eye"]}'
db_set 123456 '{"name":"London","attractions":["Big Ben","London Eye"]}'

db_get 42 
{"name":"San Francisco","attractions":["Golden Gate Bridge"]}
```

Под капотом у нас просто лежит вот такой файлик:
``` ./database
123456,{"name":"London","attractions":["Big Ben","London Eye"]}
42,{"name":"San Francisco","attractions":["Golden Gate Bridge"]}
42,{"name":"San Francisco","attractions":["Exploratorium"]}
```

Во время get мы достаем последнюю (самую свежую) строчку из файлика, а старые записи не перезаписываются.аа
#### Запись

>[!warning] append - это самая простая операция, поэтому она очень *быстрая* ([[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/01.Simple db implementation/Почему append-only операция выгодный подход?|Почему?]])
>

Тут у нас все очень даже хорошо, многие базы данных используют **log-file**, при этом он **append-only**. Но базки часто сталкиваются с такими проблемами:
1) Конкурентность
2) [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02.Data structers that power your database/Сегментация логов для движка базы данных|Сегментация логов для движка базы данных]]
3) Обработка ошибок и частичные записи (записи, которые смогли выполниться только наполовину)
#### Чтение
Сейчас тут у нас ужасная производительность - **O(N)**
Чтобы решить эту проблему мы можем использвать [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/02.Data structers that power your database/Индексы в базах данных|индексы]], которые ускоряют чтение, но замедляют запись.