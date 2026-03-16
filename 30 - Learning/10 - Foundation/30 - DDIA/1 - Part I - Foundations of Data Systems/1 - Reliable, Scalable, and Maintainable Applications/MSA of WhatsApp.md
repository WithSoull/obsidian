Ссылка на статью: https://www.geeksforgeeks.org/system-design/designing-whatsapp-messenger-system-design/?ysclid=mfte28gsg3152705856

Функциональные требования:
1) **Conversation** - чаты + группы людей
2) **Acknowledgment** - статусы отправлено / доставлено / прочитано
3) **Sharing** - передача файлов
4) **Chat storage** - хранить состояние чатов, даже если пользователи офлайн
5) **Push notifications**

Нефункциональные требования:
1) **Low latency**
2) **Consistency** - сообщения должны быть доставлены в том же порядке что и отправлены
3) **Security** - посмотреть содержимое чата могут только участники чата, никто посередине не должен иметь доступ к сожержимому, даже WhatsApp
4) **Scalability**

# Оценка capacity
### Storage
100b сообщений проходит через мессенджер и в среднем одно сообщение весит 100 байт.
Это 10TB в день, 300 TB в месяц

### Bandwidth
10 TB / day => 10 TB / 86400 sec = 925 MB/ sec

### Number of Servers
Кол-во серверов = Общее кол-во подключений в день/Кол-во подключений на сервер = 2 billion/10 million = 200 servers

# High level design (HLD)
![[99 - Meta/02 - Медиа/Pasted image 20250922143822.png]]

# Data model design
![[99 - Meta/02 - Медиа/Pasted image 20250922145247.png]]

1) **users** - содержит информацию о пользователе, номер, имя
2) **messages** - сообщения с разными типа (текст, фото, видео и тд)
3) **chats**  - приватные чаты между двумя пользователями, могут содержать множество сообщений
4) **users_chats** - N:M = users : chats
5) **groups** - группы между несколькими пользователями
6) **users_groups** - N:M = users : groups

# API Design
1) SendMessage(message_ID, sender_ID, reciever_ID, type, text=None, media_object=None, document=None)
2) GetMessage(user_ID) - получить все непрочитанные сообщения после некоторого периода офлайна
3) UploadFile(file_type, file) - возвращает идентификатор, который является ID который потом перенаправляется получателю.
4) DownloadFile(user_id, file_id) - получить файл
# ***Low Level Design*** (LLD) of System Design
![[99 - Meta/02 - Медиа/Pasted image 20250922150403.png]]

#### 1. WebSocket
**WebSocket Server** — облегчённый сервер, способный обрабатывать до 10 миллионов одновременных соединений на одном сервере (решение проблемы C10M) . Использует event-driven архитектуру с неблокирующим I/O для избежания накладных расходов “один поток на соединение” .
**WebSocket Manager** — центральный компонент, который управляет маппингом между пользователями и их портами/соединениями, используя Redis как распределённый кеш для хранения состояния соединений .

###### **APIs**:

- `connectUser(userId, port)` - Assigns a port to a user.
- `disconnectUser(userId)` - Disconnects a user.
- `getUserConnection(userId)` - Retrieves the user connection details.

#### 2. Message Service

###### Основные компоненты
- **Message Queue (FIFO)**: Kafka с единственной партицией на чат для strict ordering
- **Mnesia Database**: distributed Erlang DBMS для persistent storage
- **Delivery Status**: three-tier система (sent→delivered→read)

###### API Methods
- `storeMessage(message)` — персистентное сохранение в Mnesia
- `getMessages(userId)` — извлечение offline messages при reconnect
- `markAsDelivered(messageId)` — обновление статуса доставки
- `setRetentionPolicy(chatId, days)` — конфигурация retention

###### Kafka FIFO Implementation
- Single partition per chat: `partitionKey = hash(chat_id)` 
- Producer idempotence для exactly-once delivery
- Consumer ordering гарантии только внутри партиции 
- Batch processing для повышения throughput

###### Mnesia Features
- Distributed transactions с ACID properties
- Dynamic schema reconfiguration в runtime
- Multi-node replication для fault tolerance 
- Query List Comprehension (QLC) для complex queries
