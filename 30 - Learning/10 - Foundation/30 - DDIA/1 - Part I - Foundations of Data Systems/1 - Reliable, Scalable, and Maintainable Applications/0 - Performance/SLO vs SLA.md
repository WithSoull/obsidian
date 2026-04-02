| Название | Смысл | Для кого | Пример |
| --- | --- | --- | --- |
| [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Service Level Objective|SLO]] | внутренняя целевая планка качества | инженеры, SRE, продукт | `99.95%` uptime, `95%` запросов `<200 ms` |
| [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/1 - Reliable, Scalable, and Maintainable Applications/0 - Performance/Service Level Agreement|SLA]] | внешнее обещание клиенту | бизнес, юристы, клиенты | `99.9%` uptime, иначе компенсация |

Обычно связь такая:
- `SLO` строже и используется внутри команды;
- `SLA` опирается на те же метрики, но оформлен как обязательство.
