# Alpha Project - Tech Development
#### Desc
 ini adalah central log, digunakan untuk memonitoring segala kegiatan di server dengan pola kerja menggunakan syslog server, dan memiliki dashboard untuk memonitoring segala kegiatan dalam server.

### How to setup on server
```shell
# echo "*.* @ip_address_alpha_client:514" >> /etc/(rsyslog.conf/syslog.conf)
```

### Requirement Tools
 - [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)
 - [Docker Compose](https://docs.docker.com/compose/install/#install-compose)

### How to install (Debian Family)
```shell
# update db packages debian #
$ sudo apt-get update

# install dependencies #
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# download key #
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# add GPG key #
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# reload packages db, and install docker-ce #
$ sudo apt-get update && sudo apt-get install docker-ce

# register user to docker groups #
$ sudo usermod -aG docker $SUDO_USER

# install docker-compose #
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose
```
### Port bind & access
| Service | Address | Ports | Access/DSN
| :----------- | :------ | :------------: | :------------ |
| AlphaServer | 0.0.0.0   | 5000/TCP | http://0.0.0.0:5000 |
| AlphaClient | 0.0.0.0 | 514/UDP | udp://0.0.0.0:541 |

###
### How to start server
```shell
$ docker-compose build
### update/pull latest images docker / if error return to login

$ docker-compose up --abort-on-container-exit
### docker-compose down ###
```
###
### How to scale server
```shell
$ docker-compose scale alpha_client=3
```
### How to start server DEMO
```shell
$ docker-compose -f docker-compose.demo.yml build
### update/pull latest images docker / if error return to login

$ docker-compose -f docker-compose.demo.yml up --abort-on-container-exit
### docker-compose down ###
```