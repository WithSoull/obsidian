DDIA сначала предлагает договориться не о масштабировании, а о языке измерения системы.

## Зачем это нужно
Пока мы не описали нагрузку и измерения, разговоры про "быстро" и "медленно" остаются слишком расплывчатыми.

## Базовые метрики
Ключевые метрики:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Response Time, Service Time, and Latency|Response Time, Service Time, and Latency]].
- **Throughput**  это сколько запросов, событий или байт система обрабатывает за единицу времени.
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Percentile|Percentile]] нужны, потому что среднее плохо отражает опыт медленных пользователей.
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Service Level Objective|SLO]] и [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Service Level Agreement|SLA]] фиксируют ожидаемый уровень сервиса.

## Как метрики связаны
Связь между метриками:
- при фиксированных ресурсах рост `throughput` повышает `response time`, потому что появляются очереди;
- ближе к пределу системы очередь растет нелинейно;
- из-за этого пользователь чаще страдает не от "медленного кода", а от ожидания.

## Где ломается интуиция
Что важно держать рядом с метриками:
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Head-of-Line Blocking|Head-of-Line Blocking]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Tail Latency Amplification|Tail Latency Amplification]];
- [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Overload, Retry Storm, and Backpressure|Overload, Retry Storm, and Backpressure]].

## Практический вывод
Практический вывод:
- `response time` лучше мерить на стороне клиента;
- `throughput` нужен для capacity planning;
- `scalability` обсуждается только после того, как нагрузка и ожидаемая производительность описаны явно.
