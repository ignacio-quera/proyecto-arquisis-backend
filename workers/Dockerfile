# Dockerfile para producer
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /opt/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Actualiza pip
RUN pip install --upgrade pip

# Copia y instala las dependencias
COPY requirements.txt /opt/requirements.txt
RUN chmod +x /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

# Copia el código fuente
COPY . /opt/
