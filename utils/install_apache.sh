#!/usr/bin/bash

# Install apache
apt install apache2 -y;
a2enmod rewrite proxy proxy_http;
systemctl restart apache2;

echo '<Directory /var/www/html/>' >> /etc/apache2/sites-enabled/000-default.conf;
echo -e '\t Options Indexes FollowSymLinks MultiViews' >> /etc/apache2/sites-enabled/000-default.conf;
echo -e '\t AllowOverride All' >> /etc/apache2/sites-enabled/000-default.conf;
echo -e '\t Require all granted' >> /etc/apache2/sites-enabled/000-default.conf;
echo '</Directory>' >> /etc/apache2/sites-enabled/000-default.conf;
touch /var/www/html/.htaccess;
systemctl restart apache2;

# Certbot install
apt install python3 python3-dev python3-venv libaugeas-dev gcc -y;
python3 -m venv /opt/certbot
/opt/certbot/bin/pip install --upgrade pip
/opt/certbot/bin/pip install certbot certbot-apache
ln -s /opt/certbot/bin/certbot /usr/local/bin/certbot