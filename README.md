# 2024-1 / IIC2173 - E0 | Flight Lists Async

**María Angélica Gazitúa**

## Consideraciones Generales

La aplicación fue echa a través de FastAPI para Python, junto al uso Postgresql para la base de datos y Nginx para configurar el reverse proxy.

En la base de datos se crean dos tablas: 
- *`{Flight}`*
- *`{Airport}`*

Donde la primera guarada toda la información correspondiente a los vuelos recibidos y *`{Airport}`* guarda el id de cada aeropuerto junto a su nombre. 

Para el archivo `.env` se deben colocar las siguientes cosas: 

`DB_USER=angegazitua`

`DB_PASSWORD=cachaguA9.`

`DB_HOST=db`

`DB_PORT=5432`

`DB_NAME=db_development_flights_e0`

El archivo dodne se encuetra la configuración de Nginx es `api.conf`

## Requisitos

Todos los requesitos funcionales y no funcionales fueron logrados, así como dockerizar y los requisitos variables. 

### Requisitos funcionales 
- RF1 ✅
- RF2 ✅ --> El *`{:identifier}`* utilizado es el id que se le asigna a cada vuelo cuando son creados. Es posible verlo cuando se despliega toda la información de ***flights***
- RF3 ✅
- RF4 ✅

### Requisitos no funcionales
- RNF1 ✅
- RNF2 ✅
- RNF3 ✅ --> se utilizó dominio .me
- RNF4 ✅
- RNF5 ✅ --> Base de datos Postgres
- RNF6 ✅

### Docker-Compose
- RNF1 ✅
- RNF2 ✅
- RNF3 ✅

### Variables

Se implementó el requisito HTTPS: 
- RNF1 ✅
- RNF2 ✅
- RNF3 ✅

También se implementó el balanceo de carga con NGINX: 
- RF1 ✅
- RF2 ✅ --> Los nombres de los dos containers adicionales son fastapi_app_2 y fastapi_app_3

## Nombre dominio 

angegazituae0.me

## Acceso al servidor
Para acceder al servidor se debe ejecutar en el terminal donde está la carpeta donde se encuentra el archivo servidorarqui-angegazitua.pem:

1. Abra un cliente SSH.

2. Localice el archivo de clave privada. La clave utilizada para lanzar esta instancia es servidorarqui-angegazitua.pem

3. Ejecute este comando, si es necesario, para garantizar que la clave no se pueda ver públicamente.
 chmod 400 "servidorarqui-angegazitua.pem"

4. Conéctese a la instancia mediante su DNS público:
 ec2-18-221-235-186.us-east-2.compute.amazonaws.com

Ejemplo:

ssh -i "servidorarqui-angegazitua.pem" ubuntu@ec2-18-221-235-186.us-east-2.compute.amazonaws.com


## Usuario IAM

URL de inicio de sesión de la consola: 
- https://851725438542.signin.aws.amazon.com/console
- Nombre de usuario: angegazituac
- Contraseña: 03gE6\{-8

En el link se ingresa el nombre de usuario y contraseña. Con cada inicio de sesión pide un cambio de contraseña.