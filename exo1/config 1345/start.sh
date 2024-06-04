#!/bin/bash

sudo apt update
sudo apt install -y software-properties-common curl

sudo add-apt-repository -y ppa:ondrej/php
sudo apt update

sudo apt install -y nginx mariadb-server php8.3 php8.3-fpm php8.3-mysql php8.3-mysqli

sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl start mariadb
sudo systemctl enable mariadb

echo -e "\ny\ny\nroot\nroot\ny\ny\ny\ny\n" | sudo mysql_secure_installation

DB_NAME=wordpress
DB_USER=root
DB_PASS=root

sudo mysql -u root -proot -e "CREATE DATABASE ${DB_NAME};"
sudo mysql -u root -proot -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';"
sudo mysql -u root -proot -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -u root -proot -e "FLUSH PRIVILEGES;"

cd /var/www/html
sudo curl -O https://wordpress.org/latest.tar.gz
sudo tar xzvf latest.tar.gz
sudo cp wordpress/wp-config-sample.php wordpress/wp-config.php

sudo sed -i "s/database_name_here/${DB_NAME}/" wordpress/wp-config.php
sudo sed -i "s/username_here/${DB_USER}/" wordpress/wp-config.php
sudo sed -i "s/password_here/${DB_PASS}/" wordpress/wp-config.php

sudo chown -R www-data:www-data /var/www/html/wordpress
sudo chmod -R 755 /var/www/html/wordpress

sudo rm /etc/php/8.3/fpm/php-fpm.conf
sudo cp /vagrant/config/php-fpm.conf /etc/php/8.3/fpm/php-fpm.conf

sudo rm /etc/nginx/sites-enabled/default
sudo cp /vagrant/config/wordpress.conf /etc/nginx/sites-available/default

sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl reload php8.3-fpm

echo "Installation et configuration de WordPress terminées !"