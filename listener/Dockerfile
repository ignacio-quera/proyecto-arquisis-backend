# Usar la imagen base de Python
FROM python:3.8

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /listener

# Copiar el archivo de Python y el archivo de credenciales al contenedor
COPY topic_handler.py .
COPY .env .
COPY requirements.txt .


# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_listener.py .
# Ejecutar el archivo Python al iniciar el contenedor
CMD ["python", "mqtt_listener.py"]