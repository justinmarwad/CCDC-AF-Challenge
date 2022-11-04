# CCDC AF Challenge #

This repository contains the code for the CCDC AF Challenge. The challenge is to build a model of the Air Force and then complete specific tasks to provide resiliency and secure communications for the Air Force.

### Getting Started ### 

#### Part 1: Install & Setup Docker ###

Docker: ```sudo apt-get install docker.io -y```

Docker Compose: 
```
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

Add Docker to your user group: 
```
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```


#### Part 2: Clone This Repository ####

```git clone https://github.com/justinmarwad/CCDC-AF-Challenge``` 

#### Part 3: Docker Compose ####

Docker Compose: 
```docker compose up -d```

#### Part 4: Coffee Break ####

Network Chuck would be proud.


### TODO ### 

1. Put haproxy and postgres on their own networks. 

2. Visualizer 

```
  visualizer:
    image: dockersamples/visualizer:stable
    ports:
      - "7001:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      placement:
        constraints: [node.role == manager]
    networks:
      - back-end
```