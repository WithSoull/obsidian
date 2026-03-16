Утилита вместо Docker Desktop на MacOS

```
brew install colima
colima start
```
# Чтобы заработал docker в pycharm пришлось добавить такой симлинк:

```
sudo ln -s ~/.colima/docker.sock /var/run/docker.sock
```