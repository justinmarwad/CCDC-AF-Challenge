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

#### Part 3: Docker Compose -- One System ####

Docker Compose: 
```docker compose up -d```

*Docker File*
```dockerfile
version: "3.9"
```
The Version describes the version of docker compose that will be used in the spinning up of the stack. This is necessary and will appear in all docker compose files 

```dockerfile
services:
```
This Tag specifies the start of the file where we will define the services that will be spun up by compose, all the services will be indented with one **Tab** (or 2 spaces?) 

```dockerfile
  db:
    image: postgres
    volumes:
      - db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    networks:
      - db_net
```
This defines a service with the **name** db, this will provide a **DNS alias** that the **docker DNS** service can use to address the container(s)

The following describes the internal tags of the service db.

***image: postgres*** defines the image that this service will be build off of, *remember* all containers are a running version of some image. We can alternatively use the tag **build: \<path to dockerfile\>** where the image will be built, and run off of that build rather then pulled from dockerhub. **In this case** we are using a postgres SQL database image.

***[volumes](https://docs.docker.com/storage/volumes/):*** is a tag used to define volumes associated with the image. Volumes are structures, or mounts used to add persistence to docker containers. There can be zero or more volumes per container, but when we use this tag at least one is expect. **In this case** we use a **named volume** db (defined later!), the short or long [syntax](https://docs.docker.com/compose/compose-file/compose-file-v3/#:~:text=in%20the%20documentation.-,Short%20syntax,-The%20short%20syntax) can be used depending on preference. Each volume is listed in the following form under the **volume:** tag. 
```dockerfile
# Not a part of the final code! 
<tab> - <volume>
<tab> - <volume>
...
```

***environment:*** defines the environment variables to be passed to the docker container generated by the image, in this case the environment variables are used to describe some of the parameters that will be used by the postgres database. As with the volumes there can be zero or more environment, but when this tag is used then at least one is expected. They also have essentially the same format as the volumes Tag, with the following format 
```dockerfile
# Not a part of the final code! 
<tab> - <envName>=<value>
<tab> - <envName2>=<value2>
...
```

***networks:*** defines the docker networks that the container will be attacked to, if this is not provided it will be assumed that the container will be on the default network. This follows the same format as the volumes tag! **In this case** we are attaching this container to one network called db_net



```dockerfile
  web:
    image: sh0rtcyb3r/ccdc23_af_django:latest
    #ports: # This is not needed as it does not need to be exposed, we currently have it as part of the internal network. 
      #- "8000:8000"
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    networks:
      - db_net
      - wb_net    
    depends_on:
      - db
```
This defines a service with the **name** web, this will provide a **DNS alias** that the **docker DNS** service can use to address the container(s)

***image: sh0rtcyb3r/ccdc23_af_django:latest*** defines the image that this service will be build off of. This is a custom image, and is hosted on docker hub.

***environment:*** is the same format as described before. **In this case** these are defined and used by the Django sever, so they are slightly different and are used by the django server to access the database.

***networks:*** This format is the same as described before. **In this case** the web service will be connected to the bd_net and wb_net networks.

***depends_on:*** Tells docker compose that this service cannot be created unless the following services are already created and running. **In this case** the web service depends on the db (databse) service, this is because it needs to connect to the database and if it is unable to do so errors will occur. The depends_on tag has a format similar to the volumes Tag.
```dockerfile
# Not a part of the final code! 
<tab> - <service>
<tab> - <service2>
...
```

```dockerfile
  haproxy:
    image: haproxy:latest
    volumes:
      - ./data/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro 
    ports:
      - "80:80"
    networks: 
      - db_net
      - wb_net
      - out_net
    depends_on:
      - web
    restart: on-failure 
```
This is a service defining the proxy container that will be used to implement further security measures.

***image: haproxy:latest*** defines the image that will be used in creating this service, this is a offical HAProxy image from docker hub.

***volumes:** The format is the same as described before. **In this case** we are using a bind mount, where are a mapping a directory (or file in this case) to a location (or file) on the container. Changes made in either the host or container will affect each other in this case. Functionally this is no different from the **named** or **anonymous** volumes, just they are mapped to a known place in the filesystem.  

***ports:** defines the port mapping of the host port to the container port, there can be zero or more of these mapping, but when this tag is used atleast one is expected. When mapping to he host machine, keep in mind that only one container can bind to a port at a time. Each container has its own network stack so each can have a service listening on 80, but only one can bind to the host's port 80 (unless swarm is used, as discussed lated). **In this case** we are mapping port 80 on the host to the port 80 on the container, which is what the HAProxy container will be listing on. The format following the Tag will be
```dockerfile
# Not a part of the final code! 
<tab> - "<HostPort#>:<ContainerPort#>"
<tab> - "<HostPort#>:<ContainerPort#>"
```

***depends_on:*** this format is the same as described before. **In this case** the haproxy service depends on the web service, so it will not start till the web service container(s) have started. Since the web service depends on the db (database) service then it will not start till both the db, and web services have started.

```dockerfile
volumes: 
  db: 
```
This ***volumes:*** Tag defines the **named** volumes that should be created and used in the docker compose file. The format after the tag is quite simple as shown below.

```dockerfile
# Not a part of the final code! 
<tab><NamedVolume>:
<tab><NamedVolume2>:
...
```

```
networks: 
  db_net: 
    driver: bridge 
    attachable: true
    internal: true
  wb_net:
    driver: bridge 
    attachable: true
    internal: true
  out_net:
    driver: bridge  
    attachable: true
```
The ***networks:*** tag defines the networks to be created (and later used) by the services.

Each network is named and is created one tab in from the initial networks tab. So we would have the following 
```dockerfile
# Not a part of the final code! 
networks: 
  db_net: 
  wb_net:
  out_net:
```

After this we can define options and configurations for the networks as needed, there are a large number of possible [options](https://docs.docker.com/compose/compose-file/compose-file-v2/#network-configuration-reference) that can be used!

***driver: \<type\>** there are a number of types of [drivers](https://docs.docker.com/network/#network-drivers) that can be used. **In this case** we can used a **bridge** driver as we have yet to move to a swarm based configuration.

***attachable: \<bool\>***  this defines whether manual container attachment is enabled (true) or not (false).

***internal: \<bool\>*** this defines whether this network is created to be externally isolated. This means it has not internet gateway (true) or can access the internat through a gateway directly (false). 

##### Final docker-compose.yml
```dockerfile
version: "3.9"

services:
  db:
    image: postgres
    volumes:
      - db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    networks:
      - db_net

  web:
    image: sh0rtcyb3r/ccdc23_af_django:latest
    #ports: # This is not needed as it does not need to be exposed, we currently have it as part of the internal network. 
      #- "8000:8000"
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    networks:
      - db_net
      - wb_net
    depends_on:
      - db
  
  haproxy:
    image: haproxy:latest
    volumes:
      - ./data/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro 
    ports:
      - "80:80"
    networks: 
      - db_net
      - wb_net
      - out_net
    depends_on:
      - web
    restart: on-failure

volumes: 
  db: 

networks: 
  db_net: 
    driver: bridge 
    attachable: true
    internal: true
  wb_net:
    driver: bridge 
    attachable: true
    internal: true
  out_net:
    driver: bridge  
    attachable: true
```


#### Part 4: HAProxy Basic Configuration ####

Create the necessary directory structure and files in the directory you will be launching the compose stack from:
```
mkdir -p ./data/haproxy/
touch ./data/haproxy/haproxy.cfg
```

Edit the configuration file to provide basic proxy services (route traffic!) with the following:
```
frontend: 
    mode http
    bind *:80  
    use_backend be_http
```
This defines the ***frontend*** of the proxy. This is what processes incoming connections, there can be multiple frontends (as they are named to differentiate them!)

***mode \<type\>*** defines the type of traffic the proxy will be listening to. **In this case** we will be Listening for HTTP traffic.

***bind \<Ip\>:<Port>*** this makes HAProxy [bind](https://www.haproxy.com/documentation/hapee/latest/configuration/binds/syntax/) to and listen on a specified port, with a specific IP as there may be more then one IP assigned to the server hosting the proxy. The \<ip\> portion can be left blank, or as we do a "*" provided to specify any IP dest coming to the port on the system is acceptable.  The can be **One or more** specified in the **frontend** of the proxy. **In this case** we listen for all incoming connections on port 80.  

***use_backend \<backend\>*** tells HAProxy what backend to use. **In this case** we will use a backend defined shortly. Later we will see that conditions can be added which means one frontend can lead to multiple backends!

```
backend be_http
    mode http
    server srv1 web:8000 
```
This defines a ***backend*** be_http. This is used to communicate with teh backend servers the proxy should have access to. There can again be multiple backends defined as they have unique identifiers.

***mode \<type\>*** defines the type of traffic the proxy will be listening to. **In this case** we will be using HTTP traffic.

***server \<name\> \<IP\>:\<Port#\>*** defies a server that the backend can connect to. In this case we are using the nature of DNS, and the docker DNS service to provide a basic form of load balancing (round robin ish).


##### Configuration File
```
frontend fe_http
    mode http
    bind *:80
    use_backend be_http 

backend be_http
    mode http
    server srv1 web:8000 
```
#### Part 5: Security Upgrade - TLS/SSL

##### Creation of CA/Certificate 
1. Use Self Signed for ease of pain?

##### HAProxy

Edit Config file to be the following:
```
global
   ssl-default-bind-options ssl-min-ver TLSv1.2
```
***global*** defines global configuration parameters 

***ssl-default-bind-options ssl-min-ver TLSv1.2*** defines TLS version 1.2 to be the minimum supported version by the proxy.


```
frontend fe_http
    mode http 
    bind *:80
    bind *:443 ssl crt <PathToTLS-Certificate>
    
    http-request redirect scheme https unless { ssl_fc }
    
    use_backend be_http 
```

***bind *:443 ssl crt \<PathToTLS-Certificate\>*** tell HAProxy to bind to port 443, and listen for any connections made to it. Port 443 is a well known port used for HTTPS connections, as the traffic is encrypted and the server's identity is verified with a certificate we need to provide one. This is where the additional **ssL crt \<PathToTLS-Certificate\>** comes from. **ssL** tells HAProxy we want a SSL/TLS connection, and **crt** specifies the location of the certificate.

***http-request redirect scheme https unless { ssl_fc }*** tells HAProxy to redirect (upgrade) HTTP traffic to become HTTPS traffic unless it is already TLS (SSL) traffic.

```
backend be_http  
    server srv1 web:8000 ssl verify none
```
***server srv1 web:8000 ssl verify none*** this line will redirect the traffic to the web containers **without** verifying the certificate **used with self signed certificates** we can specify ***ssl verify required ca-file \<PathToCA-File\>*** to add verification requirements. ([more](https://www.haproxy.com/documentation/hapee/latest/security/tls/))

###### Final Config File - TLS/SSL
```
global
   ssl-default-bind-options ssl-min-ver TLSv1.2

frontend fe_http
    mode http 
    bind *:80
    bind *:443 ssl crt <PathToTLS-Certificate>
    
    http-request redirect scheme https unless { ssl_fc }
    
    use_backend be_http 

backend be_http  
    server srv1 web:8000 ssl verify none ## No SSL since server is http and internal?
```
#### Part 6: Security Upgrade - ACL  

We would like to restrict access to the admin page of the website which is accessed through the (similar) following URL
```
https://localhost:80/admin
```

Edit configuration file as follows:

###### NEED TO EDIT TO MATCH TLS ONCE IMPLEMENTED AND TESTED
``` 
frontend fe_http
    bind *:80
    mode http 
    acl restricted_page path_beg, url_dec -i /admin 
    use_backend be_http unless restricted_page
```
***acl restricted_page path_beg, url_dec -i /admin*** HAProxy creates a **named** access control list, they can also be **inline**. This one is named **path_beg** and it will evaluate to *true* or *false*. url_dec will take an encoded url, and decode it, this is used with the ACL to find all URLs that try accessing **/admin**. If the URL has **/admin** then the acl evaluates to *true* otherwise *false*

***use_backend be_http unless restricted_page*** replaces the simpler *use_backend be_http* by adding a **conditional**, the backend will be used **unless** the **restricted_page** ACL is true. If it is true the request is refused, otherwise the connection is sent to the backend and fulfilled.



```
backend be_http
    mode http
    server srv1 web:8000 
```
***There are no changes to the backend***

##### Final Config File - ACL

###### NEED TO EDIT TO MATCH TLS ONCE IMPLEMENTED AND TESTED
``` 
frontend fe_http
    bind *:80
    mode http 
    acl restricted_page path_beg, url_dec -i /admin 
    use_backend be_http unless restricted_page

backend be_http
    mode http
    server srv1 web:8000 
```

#### Part X: Coffee Break ####

Network Chuck would be proud.


### TODO ### 

1. Put haproxy and postgres on their own networks. Done!

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




#### Redources
##### Matt
* ACL
  * https://serverfault.com/questions/754752/block-specific-url-in-haproxy-url-encoding
  * https://www.haproxy.com/documentation/hapee/latest/configuration/acls/overview/

* Docker 
  * [volumes](https://docs.docker.com/storage/volumes/)
  * [networks](https://docs.docker.com/compose/compose-file/compose-file-v2/#network-configuration-reference)
    *[drivers](https://docs.docker.com/network/#network-drivers)

* DNS
  * https://vegibit.com/dns-round-robin-in-docker/ (It will work :))

* HAProxy 
  * https://www.haproxy.com/documentation/hapee/latest/configuration/binds/syntax/
  * https://www.haproxy.com/documentation/hapee/latest/configuration/config-sections/backend/
  * SSL
    * https://support.ptc.com/help/thingworx/platform/r9/en/index.html#page/ThingWorx/Help/ThingWorxHighAvailability/configuringssltlsforhaproxy.html
    * https://www.haproxy.com/documentation/hapee/latest/security/tls/
  * ACL
    * https://www.haproxy.com/blog/introduction-to-haproxy-acls/ 
    * https://cbonte.github.io/haproxy-dconv/1.6/configuration.html#7.3.1-url_dec 
    * https://www.haproxy.com/blog/introduction-to-haproxy-acls/ 

