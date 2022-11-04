# Docker Compose For The Task #


#### Install Docker Compose and Add User to Group ###

```
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

```
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```