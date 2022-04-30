# Webapp

## Instalacion virtualenv y mysql

	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install python3.7
	sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
	sudo apt-get install python3-pip
	sudo pip3 install virtualenv
    sudo apt-get install python-dev python3.7-dev libmysqlclient.dev
    apt-get install mysql-server

## Configurar autenticación de mysql

    sudo mysql -u root -p
    > USE mysql;
    > UPDATE user SET plugin="mysql_native_password" WHERE user="root";
    > SELECT user, plugin FROM user;
    > FLUSH PRIVILEGES;
    > exit;

## Crear base de datos

    mysql -u root
    > CREATE DATABASE webapp_db;
    > exit;

## Crear entorno

	virtualenv -p /usr/bin/python3.7 nombre-entorno

- Activar entorno

		source nombre-entorno/bin/activate

- Desactivar entorno

		deactivate

## Paquetes

	pip install -r requirements.txt

## Iniciar con flask-script

	python manage.py runserver

## Nginx y Gunicorn

	sudo apt-get install nginx

## Iniciar con gunicorn

	gunicorn --bind 0.0.0.0:5000 wsgi:app

## Crear servicio para la app

- Crear /etc/systemd/system/app.service

- Iniciar servicio y crear socket

		sudo systemctl start app

- Habilitar servicio para que inicie al arrancar el equipo

		sudo systemctl enable app

## Crear servidor nginx

- Crear /etc/nginx/sites-available/app

- Crear enlace 

		sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

- Reiniciar nginx

		sudo systemctl restart nginx

- Abrir servidor nginx

		sudo ufw allow 'Nginx Full'
