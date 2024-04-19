# Usar la imagen base de Python
FROM python:3.8

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /mqtt

# Copiar el archivo de Python y el archivo de credenciales al contenedor
COPY mqtt_publisher.py .
COPY .env .
COPY requirements.txt .

# Revisa que se haya copiado la carpeta "app" al directorio de trabajo del contenedor
RUN ls -a

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el archivo Python al iniciar el contenedor
CMD ["python", "mqtt_publisher.py"]