#!/bin/bash

RDS_DB_HOST=$1
RDS_DB_PASSWD=$2
export AWS_ACCESS_KEY_ID=$3
export AWS_SECRET_ACCESS_KEY=$4
export AWS_DEFAULT_REGION=$5


apt update -y && apt install -y nginx mysql-client-5.7 \
	php-fpm php-mysql php-curl php-gd php-intl php-mbstring \
	php-soap php-xml php-xmlrpc php-zip dos2unix 

systemctl enable nginx	
systemctl restart php7.2-fpm
 
cat << 'EOF' > /etc/nginx/sites-available/wordpress
server {
        listen 80;
        root /var/www/wordpress;
        index index.php index.html index.htm index.nginx-debian.html;
        server_name myawsblog.xyz;

        if ($http_x_forwarded_proto != 'https') {
                rewrite ^ https://$host$request_uri? permanent;
	}


        location / {
                try_files $uri $uri/ /index.php$is_args$args;
        }

        location ~ \.php$ {
                if ($http_x_forwarded_proto = 'https') {
                    set $fe_https 'on';
                }
                fastcgi_param HTTPS $fe_https;
                include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
        }
        location = /favicon.ico { log_not_found off; access_log off; }
        location = /robots.txt { log_not_found off; access_log off; allow all; }
        location ~* \.(css|gif|ico|jpeg|jpg|js|png)$ {
                expires max;
                log_not_found off;
        }

        location ~ /\.ht {
                deny all;
        }
}
EOF

ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/
rm /etc/nginx/sites-available/default
rm /etc/nginx/sites-enabled/default
systemctl start nginx
systemctl reload nginx
systemctl enable nginx

mysql -u wordpress -p${RDS_DB_PASSWD} -h ${RDS_DB_HOST} -D wordpressdb -e "GRANT ALL ON wordpress.* TO 'wordpress'@'${RDS_DB_HOST}' IDENTIFIED BY '${RDS_DB_PASSWD}';"
mysql -u wordpress -p${RDS_DB_PASSWD} -h ${RDS_DB_HOST} -D wordpressdb -e "FLUSH PRIVILEGES;"

pushd /tmp
curl -LO https://wordpress.org/latest.tar.gz
tar xzvf latest.tar.gz

cp /tmp/wordpress/wp-config-sample.php /tmp/wordpress/wp-config.php
cp -a /tmp/wordpress/. /var/www/wordpress
chown -R www-data:www-data /var/www/wordpress

pushd /var/www/wordpress
sed -i '/AUTH_KEY/,/NONCE_SALT/d' wp-config.php
sed -i 49r<(curl -s https://api.wordpress.org/secret-key/1.1/salt/) wp-config.php
sed -i "s/database_name_here/wordpressdb/g" wp-config.php
sed -i "s/username_here/wordpress/g" wp-config.php
sed -i "s/password_here/${RDS_DB_PASSWD}/g" wp-config.php
sed -i "s/localhost/${RDS_DB_HOST}/g" wp-config.php
sed -i 39r<(echo "define('FS_METHOD', 'direct');") wp-config.php
dos2unix wp-config.php
systemctl restart nginx
