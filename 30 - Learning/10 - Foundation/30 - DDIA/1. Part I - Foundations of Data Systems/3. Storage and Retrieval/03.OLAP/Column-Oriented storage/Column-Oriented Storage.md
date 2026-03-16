### *Проблема* Relational model, которую решает Column-Oriented model
Если у вас трилионы записей и ПБ данных в вашей *fact* таблице в [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/03.OLAP/Data Warehousing|DWH]], то эфеективные запросы становяться проблемой.
Несмотря на то, что в *fact* таблице как правило более 100 колонок, в запросах мы используем от силы колонок 5. Вот пример запроса, который анализирует: *В какой день недели люди чаще покупают свежие фрукты или конфеты?*

``` sql
SELECT
	dim_date.weekday, dim_product.category,
	SUM(fact_sales.quantity) AS quantity_sold
FROM fact_sales
	JOIN dim_date ON fact_sales.date_key = dim_date.date_key
	JOIN dim_product ON fact_sales.product_sk = dim_product.product_sk
WHERE
	dim_date.year = 2013 AND
	dim_product.category IN ('Fresh fruit', 'Candy')
GROUP BY
	dim_date.weekday, dim_product.category;
```

Проблема тут заключается в том, что когда нам приходится подгружать строки со всеми их аттрибутами, включая те, что нам не нужны. Это происходит потому, что в relational (и кстати в document таблицах, данные расположены строка за строкой в памяти.

### Идея которая, *решит эту проблему*
Сама идея: **Не хранить данные строка за строчкой, а хранить наоборот: колонка за колонкой**

![[99 - Meta/02 - Медиа/Pasted image 20251030104241.png]]

### Самый сок - Compession
Помимо того, что мы таким расположением данных решаем проблему эффективности запросов, у нас теперь тут есть огромный [[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/3. Storage and Retrieval/03.OLAP/Column-Oriented storage/Column Compresion. Сжатие в колоночных БД|простор для сжатия]], ведь это тоже немаловажный факт.

### Путаница с relational column families
- Cassandra и HBase поддерживают column families (семейства столбцов), но это не значит, что они хранят данные по столбцам ("column-oriented storage").
- Данные в column family фактически хранятся по строкам: все значения столбцов строки лежат вместе с ключом строки.
- Внутри column family не используется сжатие по каждому столбцу и нет настоящей "колоночной" организации хранения.
- Такие базы называют wide-column stores, но это вводит в заблуждение — они ближе к row-oriented, а не column-oriented подходу.
- Вывод: Cassandra — не классическая колоночная СУБД, а скорее row-partitioned NoSQL.

### Column-oriented storage: память и векторная обработка
- Основное ограничение аналитических запросов — не только диск, но и *пропускная способность между памятью и CPU cache.*
- Колоночные хранилища позволяют обрабатывать сжатые блоки данных из одного столбца, которые помещаются в *CPU L1 cache*.
- Важно *избегать лишних условий*, цикл обработки должен быть tight loop(цикл без условий и фукнций).
- Современные процессоры поддерживают *SIMD* — выполнение одной операции сразу над многими значениями (например, побитовое (bitwise) AND/OR над блоками данных).
- Сжатие колонок позволяет ещё больше данных держать в кэше и работать быстрее.
- Такая организация называется *vectorized processing* и очень эффективна для OLAP-нагрузки.
