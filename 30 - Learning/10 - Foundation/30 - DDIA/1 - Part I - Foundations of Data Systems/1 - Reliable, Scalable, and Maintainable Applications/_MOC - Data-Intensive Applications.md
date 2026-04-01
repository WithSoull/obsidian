Сегодня большая часть приложений *data-intensive*, а не *cpu-intensive*. Основные проблемы это: 
- Количество данных
- Сложность данных
- Скорость с которой они меняются

*Data-intensive* приложения строятся из дефолтных частей, потому что им всем нужно: 
- Хранить данные (*databases*)
- Хранить результат дорогих операций (*caches*) 
- Поиск по ключевым словам (*search indexes*)
- Отправлять сообщения другим процессам (*stream processing*)
- Перерабатывать большие объемы данных (*batch processing*)

Пример системы которая комбинирует несколько компонентов
![[99 - Meta/02 - Медиа/Pasted image 20250411134021.png]]

Чтобы построить хорошее *data-intensive* приложение нам необходимо:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/1 - Reliability/Reliability|Reliability(надежность)]] - Работает всегда корректно, даже если что-то идет не так. Faults могут быть связаны с железом, софтом и человеческим фактором.
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/2 - Scalability/Scalability|Scalability(масштабируемость)]] - Во время роста системы, у нас должны быть конкретные(достижимые) способы справиться с этим ростом. В первую очередь мы должны описать нагрузку и производительности.
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/3 - Maintainability/Maintainability|Maintainability(удобство сопровождения)]] - Все, кто работают над данным приложением, должны быть способны работать над ним продуктивно. Хорошие абстракции и мониторинг помогут с этим.

До этих качеств полезно договориться о базовой архитектурной рамке:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Distributed Versus Single-Node Systems|Distributed Versus Single-Node Systems]]
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/0 - Trade-Offs in Data Systems Architecture/Systems of Record and Derived Data|Systems of Record and Derived Data]]

Дополнительные материалы:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/Defining Nonfunctional Requirements Audit|Defining Nonfunctional Requirements Audit]]
