# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece la variable de entorno para desactivar el buffering de Python
ENV PYTHONUNBUFFERED 1

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y luego instala las dependencias
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el contenido del proyecto en el directorio de trabajo
COPY . .

COPY .env .env

# Expone el puerto en el que la aplicacion correra
EXPOSE 5000

# Comando para ejecutar la aplicacion Flask
CMD ["python", "app.py"]
