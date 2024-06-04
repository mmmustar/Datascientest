FROM ubuntu:focal
MAINTAINER TG <mustarmartin@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server \
    passwd \
    sudo \
    curl \
    wget \
    nginx \
    php-cli \
    php-mysql \
    php-curl \
    php-gd \
    php-intl \
    mariadb-server

# Modifie le fichier de configuration SSH pour qu'il écoute sur le port 2222
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

EXPOSE 2222 80

RUN apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done) && \
    rm -f /lib/systemd/system/multi-user.target.wants/* && \
    rm -f /etc/systemd/system/*.wants/* && \
    rm -f /lib/systemd/system/local-fs.target.wants/* && \
    rm -f /lib/systemd/system/sockets.target.wants/*udev* && \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl* && \
    rm -f /lib/systemd/system/basic.target.wants/* && \
    rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN useradd --create-home -s /bin/bash admin
RUN echo 'admin:admin' | chpasswd
RUN echo 'admin ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/admin && \
    chmod 440 /etc/sudoers.d/admin

RUN mkdir -p /home/admin/.ssh && \
    chmod 700 /home/admin/.ssh
ADD https://raw.githubusercontent.com/hashicorp/vagrant/master/keys/vagrant.pub /home/admin/.ssh/authorized_keys
RUN chmod 600 /home/admin/.ssh/authorized_keys && \
    chown -R admin:admin /home/admin/.ssh

RUN mkdir -p /run/sshd

VOLUME [ "/var/log/nginx", "/var/www/html", "/var/lib/mysql" ]

CMD /bin/bash -c "php-fpm -F & service nginx start && /usr/sbin/sshd -D"
