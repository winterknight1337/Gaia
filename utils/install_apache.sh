#!/usr/bin/bash

apt install apache2 -y;
a2enmod rewrite proxy proxy_http;
systemctl restart apache2;

echo '<Directory /var/www/html/>' >> /etc/apache2/sites-enabled/000-default.conf;
echo -e '\t Options Indexes FollowSymLinks MultiViews' >> /etc/apache2/sites-enabled/000-default.conf;
echo -e '\t AllowOverride All' >> /etc/apache2/sites-enabled/000-default.conf;
echo -e '\t Require all granted' >> /etc/apache2/sites-enabled/000-default.conf;
echo '</Directory>' >> /etc/apache2/sites-enabled/000-default.conf;

touch /var/www/html/.htaccess;
echo -e 'RewriteEngine on';