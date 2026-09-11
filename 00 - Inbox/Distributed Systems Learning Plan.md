# Distributed Systems Learning Plan

## Цель

Системно прокачать distributed systems, внутренности БД и backend infrastructure, не превращая обучение в бесконечный просмотр YouTube.

Основной принцип: **глубокие курсы + реализация + DDIA**, а YouTube-каналы использовать как дополнительную инженерную насмотренность.

## Основной трек

### 1. MIT 6.824 / 6.5840 — Distributed Systems

Главный курс на старте.

- Пройти лекции последовательно, а не выбирать случайные темы.
- Делать labs на Go; просмотр без реализации даёт сильно меньше пользы.
- Особое внимание:
  - RPC и failure model;
  - replication;
  - Raft;
  - linearizability и consistency;
  - distributed transactions;
  - Spanner;
  - optimistic concurrency control;
  - fault tolerance.

Ресурс: https://www.youtube.com/playlist?list=PLrw6a1wE39_tb2fErI4-WkMbsvGQk9_UB

### 2. DDIA — параллельно с MIT

Не читать книгу отдельно от практики: связывать главы с темами из MIT и реальными системами.

После важной темы фиксировать не пересказ, а:

- какой invariant система пытается сохранить;
- какие есть failure scenarios;
- какой consistency model получается;
- какие trade-offs сделаны;
- где подобное встречается в PostgreSQL, Kafka, S3, Redis и других знакомых системах.

### 3. CMU 15-445/645 — Database Systems

После появления устойчивого ритма с MIT или после основной части курса.

Фокус:

- storage engines;
- buffer pool;
- indexes;
- query execution;
- transactions;
- concurrency control;
- MVCC;
- WAL и recovery;
- query optimization.

Ресурс: https://www.youtube.com/playlist?list=PLSE8ODhjZXjbohkNBWQs_otTrBTrjyohi

### 4. CMU 15-721 — Advanced Database Systems

Идти сюда после 15-445, выборочно или полностью в зависимости от интереса.

Особенно интересны:

- advanced concurrency control;
- OLTP internals;
- storage layouts;
- recovery;
- execution engines;
- database scheduling;
- query optimization.

Ресурс: https://www.youtube.com/playlist?list=PLSE8ODhjZXjasmrEd2_Yi1deeE360zv5O

## Дополнительный фундаментальный контент

### Martin Kleppmann — Distributed Systems

Использовать как альтернативное объяснение тем из DDIA/MIT, а не как ещё один обязательный параллельный курс.

https://www.youtube.com/playlist?list=PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB

## Casual engineering content

Не считать это «учёбой». Смотреть в свободное время для инженерной насмотренности.

### English

- Hussein Nasser — backend, networking, DB internals, protocols.
- Arpit Bhayani — distributed systems и system design.
- ThePrimeagen / ThePrimeTime — engineering, codebases, performance, tooling.
- ByteByteGo — быстрые карты технологий и обзор новых тем; не использовать как основной источник.
- GopherCon / Gopher Academy — выборочные production-oriented Go talks.
- Computerphile — широкий CS-кругозор.

### Russian

Не отказываться от русскоязычных авторов ради искусственного English-only режима.

Из уже нравящихся:

- Тузов;
- Влад Тен;
- Козырев.

Использовать их прежде всего для инженерной насмотренности, Go/backend-контекста, карьеры и опыта индустрии.

## Technical English

Цель — не «учить английский», а перестать воспринимать язык как дополнительный слой между собой и технической концепцией.

Базовый режим:

- около 80% фундаментального технического контента — English;
- английская речь + английские субтитры;
- не искать русскую замену сильному первичному материалу только из-за языка;
- незнакомые термины разбирать в исходной английской форме;
- русский YouTube оставить там, где конкретный автор действительно полезен или приятен для casual-просмотра.

Желаемый результат: `linearizability`, `quorum`, `lease`, `write skew`, `WAL`, `snapshot isolation`, `happens-before` воспринимаются непосредственно как инженерные понятия без мысленного перевода.

## Как не утонуть в материалах

Не проходить MIT, CMU, Kleppmann и десятки каналов одновременно.

Приоритет примерно такой:

1. **MIT 6.824/6.5840 + labs** — основной активный курс.
2. **DDIA** — параллельный фундамент и база для собственных заметок.
3. **CMU 15-445** — следующий большой курс.
4. **CMU 15-721** — углубление после базы.
5. Kleppmann — дополнительное объяснение сложных distributed systems тем.
6. Остальной YouTube — casual engineering content.

## Практика

После каждой крупной темы должен появляться хотя бы один активный результат:

- реализованный lab;
- небольшой эксперимент;
- разбор production-системы;
- архитектурная заметка;
- применение идеи к OpenS3;
- объяснение механизма своими словами без подсказок.

Особенно полезно постоянно задавать вопросы:

- Что произойдёт при network partition?
- Где находится source of truth?
- Какие состояния могут наблюдаться конкурентно?
- Что произойдёт при retry?
- Где нужна idempotency?
- Что можно потерять при crash?
- Как восстанавливается состояние?
- Какой порядок событий гарантируется?
- Где проходит transaction boundary?
- Какую consistency система реально обещает?

## Пример минимального недельного режима

Не фиксированный календарь, а ориентир по нагрузке:

- 2–3 глубоких сессии MIT / labs;
- 1–2 сессии DDIA;
- casual YouTube — без обязательной нормы;
- CMU пока не добавлять как второй полноценный курс, пока MIT не идёт стабильно.

Главный критерий прогресса — не количество просмотренных часов, а способность **реализовать механизм, объяснить invariant и разобрать поведение системы при отказе**.
