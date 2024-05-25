# Guía de Despliegue de la Aplicación con Serverless/SAM

Este es un breve tutorial para desplegar tu aplicación utilizando Serverless Application Model (SAM). SAM es una extensión del CloudFormation que facilita la creación de aplicaciones serverless en AWS.
## Paso 1: Configuración del Entorno

Asegúrate de tener instalado y configurado:

    AWS CLI
    SAM CLI
    Credenciales de AWS configuradas localmente

## Paso 2: Preparación del Proyecto

    Clona este repositorio a tu máquina local.
    Asegúrate de tener un archivo template.yaml que describe tu infraestructura y funciones Lambda.

## Paso 3: Construcción del Proyecto

Desde la raíz del proyecto, ejecuta el siguiente comando para construir tu aplicación:



`sam build`

Este comando compilará tu aplicación y la preparará para el despliegue.
## Paso 4: Despliegue de la Aplicación

Ejecuta el siguiente comando para desplegar tu aplicación en AWS:



`sam deploy --guided`

Este comando iniciará un asistente interactivo que te guiará a través del proceso de despliegue. Deberás proporcionar información como el nombre del stack, región de AWS, etc.
## Paso 5: Prueba de la Aplicación

Una vez que el despliegue se complete con éxito, prueba tu aplicación accediendo a los recursos creados en AWS, como API Gateway, Lambda, etc.