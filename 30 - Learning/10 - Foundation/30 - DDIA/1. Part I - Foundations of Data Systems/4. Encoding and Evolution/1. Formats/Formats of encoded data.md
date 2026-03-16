Программы работают с двумя видами представления данных:
1) **In-memory** ([[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/4. Encoding and Evolution/1. Formats/Language-Specific Formats|Language-Specific Formats]]) - данные хранятся в объектах, структурах, массивах, списках и тд. Эти данные оптимизированы под эффективный доступ, управляются CPU через указатели
2) **Самодостаточная последовательность байт(self-contained sequence of bytes)**([[30 - Learning/10 - Foundation/30 - DDIA/1. Part I - Foundations of Data Systems/4. Encoding and Evolution/1. Formats/Self-contained sequence of bytes formats.|Self-contained sequence of bytes formats.]]) - JSON, XML и тд.

При этом еще нужен слой, который умеет переводить из одного представления в другой:
1) **Encoding** - serialization/marshaling: in-memory -> byte sequence
2) **Decoding** - parsing/deserialization/unmarshling: byte sequence -> in-memory
