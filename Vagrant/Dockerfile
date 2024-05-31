FROM ubuntu:focal
MAINTAINER TG <mustarmartin@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

# Installation des paquets nécessaires
RUN apt-get update && apt-get install -y \
    openssh-server \
    passwd \
    sudo \
    iproute2 \
    git \
    curl \
    iputils-ping \
    net-tools \
    wget \
    nginx \
    php-cli \
    php-mysql \
    php-curl \
    php-gd \
    php-intl \
    mariadb-server

EXPOSE 80

# Nettoyage du cache des paquets
RUN apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Nettoyage de systemd
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done) && \
    rm -f /lib/systemd/system/multi-user.target.wants/* && \
    rm -f /etc/systemd/system/*.wants/* && \
    rm -f /lib/systemd/system/local-fs.target.wants/* && \
    rm -f /lib/systemd/system/sockets.target.wants/*udev* && \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl* && \
    rm -f /lib/systemd/system/basic.target.wants/* && \
    rm -f /lib/systemd/system/anaconda.target.wants/*;

# Activation du service SSH
RUN systemctl enable ssh.service;

# Configuration de l'utilisateur vagrant
RUN useradd --create-home -s /bin/bash vagrant
RUN echo 'vagrant:vagrant' | chpasswd
RUN echo 'vagrant ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/vagrant && \
    chmod 440 /etc/sudoers.d/vagrant

# Configuration de la clé SSH de Vagrant
RUN mkdir -p /home/vagrant/.ssh && \
    chmod 700 /home/vagrant/.ssh
ADD https://raw.githubusercontent.com/hashicorp/vagrant/master/keys/vagrant.pub /home/vagrant/.ssh/authorized_keys
RUN chmod 600 /home/vagrant/.ssh/authorized_keys && \
    chown -R vagrant:vagrant /home/vagrant/.ssh

RUN nginx

# Montage du répertoire /sys/fs/cgroup en tant que volume
VOLUME [ "/var/log/nginx", "/var/www/html", "/var/lib/mysql" ]