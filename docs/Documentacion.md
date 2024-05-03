# Diagrama UML

El sistema permite manejar información relacionada con vuelos y pasajes, a través de una API. Para poder gestionar y transmitir los datos, se utilizan los servicios AWS, Docker y MQTT. 

Particularmente, la API Gateway maneja las solicitudes, autenticadas mediante Lambda y Auth0. Dichas solicitudes son servidas por el S3 y distribuidas por el Cloudfront. Las solicitudes al API de vuelos son manejadas por Docker en EC2, con Ngnix. Los datos de estos vuelos se almacenen en la base de datos Flights DB, y se accede a ellos a travpes de la Flights API. Además, se utiliza MQTT para la comunicación en tiempo real. 

## Componentes

- Cloudfront.
- API Gateway: es el punto de entrada para las solicitudes al backend, dirigiendo las solicitudes a los servicios, apoyándose en una función Lambda y conectándose con una instancia EC2.
- Lambda (Auth0): gestiona la autentificación y autorización. 
- S3: almacena el frontend de la aplicación.
- EC2: ejecuta la API de vuelos, conteniendo al Docker.
- Docker: contiene la aplicación del backend, incluyendo la base de datos (Flights DB) y la interfaz (Flights API).
- Nginx: funciona como proxy inverso.
- MQTT publisher and subscriber: maneja la publicación y suscripción a mensajes. 
- Flights broker MQTT: broker que gestiona y coordina todos los mensajes. 


# CI 

El pipeline se activa en eventos de push y pull_request hacia la rama main. Esto permite asegurar que antes de fusionar nuevo código con la rama principal, se cumplan los estándares de calidad y las pruebas pasen correctamente. 

El workflow contiene dos jobs principales: build y test. Ambos se ejecutan en máquinas virtuales de Ubunutu, en su última versión disponible. 

- Build: el job se encarga de verificar la integridad del código al instalar dependencias y realizar un análisis estático usando EsLint. Primero, se utiliza la acción checkout para clonar el código del repositorio en el runner, luego se instalan las dependencias y de corre un Lint en el backend.
- Test: el job asegura que todos los tests unitarios pasen. Al igual que en el caso anterior, primero se clona el repositorio usando un checkout code. Luego, se configura Python en el runner y se instalan las dependencias. Finalmente, se ejecutan los tests utilizando pytest. 

# Documentación para configuración local
s
En primer lugar, se debe clonar el repositorio e instalar las dependencias. 

Para el archivo .env se debe colocar:

DB_USER=angegazitua
DB_PASSWORD=cachaguA9.
DB_HOST=db
DB_PORT=5432
DB_NAME=db_development_flights_e0

Para el archivo .env en la carpeta publisher se deben colocar:

HOST=broker.iic2173.org
PORT=9000
USER=students
PASSWORD=iic2173-2024-1-students
URL_API=http://localhost:8000/

El dominio corresponde a angegazituae0.me.

Para acceder al servidor, se deben seguir los siguientes pasos:

Se debe ejecutar en el terminal donde está la carpeta donde se encuentra el archivo servidorarqui-angegazitua.pem:

1. Abra un cliente SSH.
2. Localice el archivo de clave privada. La clave utilizada para lanzar esta instancia es servidorarqui-angegazitua.pem
3. Ejecute este comando, si es necesario, para garantizar que la clave no se pueda ver públicamente. chmod 400 "servidorarqui-angegazitua.pem"
4. Conéctese a la instancia mediante su DNS público: ec2-18-221-235-186.us-east-2.compute.amazonaws.com

Ejemplo:
ssh -i "servidorarqui-angegazitua.pem" ubuntu@ec2-18-221-235-186.us-east-2.compute.amazonaws.com

Usuario IAM:
URL de inicio de sesión de la consola:

https://851725438542.signin.aws.amazon.com/console
Nombre de usuario: angegazituac
Contraseña: 03gE6{-8
En el link se ingresa el nombre de usuario y contraseña. Con cada inicio de sesión pide un cambio de contraseña.


Para un correcto funcionamiento es importante despejar las puertos 8000, 8001, 8002 y 9000.

Ejecutar la aplicación: `python3 uvicorn  app/main:app 0.0.0.0 :8000  `
Ejecutar tests: `pytest`
Levantar Docker: `docker-compose up --build -d `