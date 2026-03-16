---
evolution: "[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Field tags & schema evolution|Field tags & schema evolution]]"
---

Это специальный самодостаточный бинарный формат файлов, разработанный *Facebook* в 2007-2008. Рассмотрим на практике.
Вот так выглядит *Thrift interface definition language*:
``` c
struct Person {
	1: required string userName,
	2: optional i64 favoriteNumber,
	3: optional list<string> interests
}
```

У thrift есть 3 разных бинарных видов кодировки под капотом: BinaryProtocol, CompactProtocol, DenseProtocol(поддерживается только C++, поэтому далее не рассматривается)

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
### BinaryProtocol
![[99 - Meta/02 - Медиа/Pasted image 20251103203219.png]]

Тут стоит обратить внимание, что мы не храним имя поля, у нас есть только номер поля, анотация типа(string, integer, list, etc.), длина строки/массива. Из 81 байтового JSON получили 59 байтовую запись, но можно лучше.

### CompactProtocol
![[99 - Meta/02 - Медиа/Pasted image 20251103203645.png]]

Он уже весит 34 байта. Давайте рассмотрим, за счет чего мы получили такое сжатие:
1) Хранит номер поля как 1 байт, а не 2 как раньше
2) Используем *variable-length integers*. Вместо того, чтобы использовать полные 8 байт для чисел, здесь мы используем 2. Верхний бит каждого байта отвечает за то, последний ли это байт или нет. Благодаря этому, можно кодировать числа `[-64, 63]` в 1 байт, `[-8192, 8191]` в 2 байта и тд. Большие числа используют больше байт