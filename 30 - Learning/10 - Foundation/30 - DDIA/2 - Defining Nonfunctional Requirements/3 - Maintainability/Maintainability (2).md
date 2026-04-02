## Что такое maintainability
Поддержка системы обычно длится намного дольше, чем ее первоначальная разработка. Поэтому **maintainability**  это не "приятный бонус", а одно из базовых качеств системы.

## Почему это сложно
Важно помнить:
- maintenance  это не только код, но и люди, процессы, знания и организационная память;
- любая достаточно полезная система рано или поздно станет legacy;
- цель не в том, чтобы "никогда не иметь legacy", а в том, чтобы сделать жизнь следующим инженерам менее болезненной.

Короткий пример:
- сервис может быть написан аккуратно;
- но через три года он уже завязан на десяток интеграций, старые форматы данных, ручные runbooks и исторические компромиссы;
- legacy появляется не только из-за плохого кода, а как побочный эффект долгой и полезной жизни системы.

## Три опоры
Три главные грани:
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Operability|Operability]]  делает повседневную эксплуатацию предсказуемой;
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Simplicity|Simplicity]]  снижает ненужную сложность;
- [[public/30 - Learning/10 - Foundation/30 - DDIA/2 - Defining Nonfunctional Requirements/3 - Maintainability/Evolvability|Evolvability]]  упрощает изменение системы под новые требования.
