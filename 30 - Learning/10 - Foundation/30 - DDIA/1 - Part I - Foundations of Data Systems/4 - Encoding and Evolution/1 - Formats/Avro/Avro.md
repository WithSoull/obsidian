### Предисловие
Это еще один бинарный формат кодирования данных, изначльно был проектом **Hadoop**, так как *thrift* не особо подходил под их требования. Механизм с [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Avro/Writers & Readers в Avro|writers & readers]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Avro/Dynamically Generated Schemas in Avro|динамически-сгенерированные схемы]] это то, что отличает Avro от остальных форматов.

### Schemas
У Avro есть две схемы,  одна (Avro IDL) для людей, и JSON для машинок:
``` c
record Person {
	string               userName;
	union { null, long } favoriteNumber = null;
	array<string>        interests;
}
```

**union** тут означает, что значение *favoriteNumber* может быть null / long;
` = null` это дефолтное значение.

``` json
{
  "type": "record",
  "name": "Person",
  "fields": [
    {
      "name": "userName",
      "type": "string"
    },
    {
      "name": "favoriteNumber",
      "type": ["null", "long"],
      "default": null
    },
    {
      "name": "interests",
      "type": {
        "type": "array",
        "items": "string"
      }
    }
  ]
}
```
### Кодировка
Далее будем рассматривать вот такой JSON для кодирования:
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

![[99 - Meta/02 - Медиа/Pasted image 20251104150933.png]]

Тут стоит обратить внимание, на то, что мы никак не идентифицируем поля и их типы. Секрет в следующем: чтобы раскодировать необходима такая же схема с читающей стороны. Любое несоответствие схем приводит к тому, что данные будут прочтены неправильно.


