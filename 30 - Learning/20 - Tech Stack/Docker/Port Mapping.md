![[99 - Meta/02 - Медиа/Pasted image 20231120131219.png]]

# На примере *nginx* 
`> docker run -d --name web1 -p 80:80 nginx` - порт 80 на сервере перебрасывается в контейнер _web_ ![[99 - Meta/02 - Медиа/Pasted image 20231120131740.png]]
`> netstat -tulpen` - показывает свободные порты и ip![[99 - Meta/02 - Медиа/Pasted image 20231120132049.png]]
`> ip a` - показывает ip-адрес серверов