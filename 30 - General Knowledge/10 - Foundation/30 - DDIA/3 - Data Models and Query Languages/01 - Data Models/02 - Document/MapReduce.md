>[!quote] MapReduce is a programming model for processing large amounts of data in bulk across many machines, popularized by Google 

*MapReduce* — это модель вычислений для обработки больших объемов данных, где разработчик описывает преобразование данных через функции, а система управляет их выполнением.

###### Позиция в контексте языков запросов
- Не декларативный язык — как SQL, не позволяет описывать задачу на уровне «что получить» без указания логики.
- Не полностью императивный API — не требует полного описания всех шагов выполнения.
- Гибридный подход — логику запроса описывают небольшие фрагменты кода (map и reduce), а фреймворк сам управляет распределением и исполнением.
###### Компоненты MapReduce
- **Map** (Collect) — применяется к каждому элементу входных данных, преобразуя их в пары ключ/значение.
- **Reduce** (Fold, Inject) — агрегирует значения с одинаковыми ключами, возвращая итоговый результат.

**MongoDB** и **CouchDB** поддерживают ограниченную форму MapReduce.
MapReduce нельзя назвать ни декларативным, ни имеративным языком: логика запроса описана 

###### Пример: Нужно собрать количество увиденных акул за каждый месяц
Вот как бы это сделали с Postgres:
``` sql
SELECT date_trunc('month', observation_timestamp) AS observation_month, sum(num_animals) AS total_animals
FROM observations
WHERE family = 'Sharks'
GROUP BY observation_month;
```

А вот так выглядел бы это запрос с использованием MapReduce в MongoDB:
``` js
db.observations.mapReduce(
	function map() { 
		var year = this.observationTimestamp.getFullYear();
		var month = this.observationTimestamp.getMonth() + 1;
		emit(year + "-" + month, this.numAnimals);
	},
	
	function reduce(key, values) { 
		return Array.sum(values); 
	},
	
	{
	query: { family: "Sharks" },
	out: "monthlySharkReport" 
	} 
);
```

Представим такие данные на входе:
``` json
{
	observationTimestamp: Date.parse("Mon, 25 Dec 1995 12:34:56 GMT"),
	family: "Sharks",
	species: "Carcharodon carcharias",
	numAnimals: 3
}
{
	observationTimestamp: Date.parse("Tue, 12 Dec 1995 16:17:18 GMT"),
	family: "Sharks",
	species: "Carcharias taurus",
	numAnimals: 4
}
```

Здесь для каждого документа единожды выполняется функция *map()*, где высчитывется текущий месяц и год и мы получим `emit("1995-12", 3)` и `emit("1995-12", 4)`. 
Затем вызовется функция `reduce("1995-12", [3, 4])`. которая вернет 7. Она вызывается таким образом, чтобы объединить одинаковые ключи и поместить значения value в один массив.

При этом функции `map()` и `reduce()` весьма ограничены в своем поведение: они могут работать только с теми данными, которые подаются на вход, нельзя например в другую базку сгонять, а также не должно быть никаких побочных эффектов. Это требуется для безопасного *параллельного* и повторного выполнения в *распределенной среде*.

При этом возможность встраивать JS код в запрос есть не только у MapReduce, это могут делать и некоторые SQL db: Postrgres и Oracle например.

MapReduce нужно писать аккуратно, при этом *декларативные* языки предлагают больше возможностей для *query optimizer*. Поэтому в MongoDB добавили *декларативный* язык запросов, называнный **aggregation pipline**. Тот же запрос будет выглядеть так:

``` js
db.observations.aggregate([
	{ $match: { family: "Sharks" } },
	{ $group: {
		_id: { year:
		{ $year: "$observationTimestamp" },
		month: { $month: "$observationTimestamp" }
		},
		totalAnimals: { $sum: "$numAnimals" }
	} }
]);
```

Это похожий на JSON язык, но при этом имеет аля кусочки, как в SQL. 

>[!danger] Мораль
>NoSQL заново изобрел SQL. хехе :)

