# Webapp

Aplicativo web para el registro de datos de posibles casos de Covid-19 o enfermedades que involucran temperaturas corporales altas, y para administración del dispositivo (conexión a internet y hotspot).

## Dependencias

- Sistema Operativo
  - Linux4Tegra (basado en Ubuntu 18.04), sistema operativo para la Jetson Nano Developer Kit
  - Raspberry Pi (Raspbian, basado en Debian), sistema operativo para la Raspberry Pi 3
- Interprete Python
  - Python >= 3.7
    - Flask
	- Bootstrap4.0
	- SQLAlchemy
	- Gunicorn
- Base de datos
  - MySQL
- Utilidades de Linux
  - Nginx
  - Netplan
  - Ufw
- Extra
  - Proyecto [Linux Wifi Hotspot](https://github.com/lakinduakash/linux-wifi-hotspot) (Para la creacion del AP / Hotspot)