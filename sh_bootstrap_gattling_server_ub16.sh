#!/bin/bash
sudo apt-get update -y

# install PHP and MySQL
sudo apt-get install git ifstat inetutils-traceroute traceroute telnet curl python python-pip python3 python3-pip libapache2-mod-python libapache2-mod-php php-mysql -y
sudo apt-get install mysql-client -y
sudo pip install requests flask ConfigParser mysql-connector-python flask-restful ast mysql-connector-python-rf
sudo pip3 install requests
sudo apt-get remove apache2 -y 

#Make dirs
sudo mkdir /APP/
cd /APP/
sudo rm -rf /APP/*

sudo git clone  https://github.com/MourIdri/flaskgattling.git
sudo chmod -R 777 /APP/*

sudo chown -R www-data:www-data /APP/*

sudo chmod -R 755 /APP/*
sudo chmod a+rwx /APP/*
sudo chmod a+rwx /APP/*


cd /APP/flaskgattling/server/
cp /APP/flaskgattling/server/rc.local /etc/rc.local
chmod 777 /etc/rc.local
sudo python restarter.py &echo "Script restarter.py done app has been started as a thread "