Как и большинство типизированных языков, Go позволяет программисту декларировать собственные типы. С помощью определений вы можете создавать новые типы, улучшая читаемость кода. Из-за строгости типизации вы ограничиваете определениями в том числе применимость функций и конструкций к вашим типам

``` go
package main

import "fmt"

type FirstName string
type LastName string

func main() {
	var fn FirstName = "Илья"
	var ln LastName = "Гришин"

	// Нужно привести к одному типу
	fmt.Println(fn + " " + FirstName(ln))
	fmt.Println(LastName(fn) + " " + ln)
	fmt.Println(string(fn) + " " + string(ln))
}

```


``` output
Илья Гришин
Илья Гришин
Илья Гришин
```

Для пользовательских типов можно создать свой метод - [[30 - Learning/20 - Tech Stack/Golang/1 - Foundation/Methods on User-Defined Types]]
