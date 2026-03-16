---
evolution: "[[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/4. Encoding and Evolution/1. Formats/Field tags & schema evolution|Field tags & schema evolution]]"
---

>[!danger]  Мой любимый **protobuf**

Это специальный самодостаточный бинарный формат файлов, разработанный *Google* в 2007-2008. Рассмотрим на практике.
Вот так выглядит *Protocol buffers interface definition language*:

``` protobuf
message Person {
	required string user_name = 1;
	optional int64 favorite_number = 2;
	repeated string interests = 3;
}
```

Далее будем рассматривать вот такой JSON:
``` json
{
	"userName": "Martin",
	"favoriteNumber": 1337,
	"interests": [
		"daydreaming",
		"hacking"
	]
}
```

![[99 - Meta/02 - Медиа/Pasted image 20251103204543.png]]

Здесь мы не храним в памяти имя поля, храним его номер, тип и длину если требуется. У нас есть 3 вида анотации: привычные *required*, *optional*, и **repeated**, который означает, что далее идет список. При этом у **repeated** элементов, просто ставиться одинаковый тэг, что символизирует о том, что это элемент *массива*.

Также стоит обратить внимание, на более сжатое хранение чисел засчет *variable-length integers*.