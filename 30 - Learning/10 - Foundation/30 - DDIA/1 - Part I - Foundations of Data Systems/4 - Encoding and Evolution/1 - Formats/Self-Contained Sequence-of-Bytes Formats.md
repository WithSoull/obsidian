---
Сравнение Binary Schemas VS Human-readable: "[[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Binary Schemas VS (JSON & XML)|Binary Schemas VS (JSON & XML)]]"
---
# Какие у нас есть самодостаточные форматы представления данных?

###### 1. Human-readable
Это самые популярные форматы, подробнее [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/JSON, XML & Binary Formats|тут]]:
1) JSON
2) XML
3) CSV
###### 2. Binary
Перед тем, как что-то перечислять, стоит оговорить что у Human-readable форматов тоже есть опция бинарного формата, но она сильно привязана к JSON/XML, поэтому не может в полной мере раскрыть данный формат данных. А вот тру бинарники:
1) [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Apache Thrift|Apache Thrift]] - от Facebook
2) [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Protocol Buffers|Protocol Buffers]] - от Google
3) [[30 - Learning/10 - Foundation/30 - DDIA/1 - Part I - Foundations of Data Systems/4 - Encoding and Evolution/1 - Formats/Avro/Avro|Avro]] - от Hadoop, после передано Apache
