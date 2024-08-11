# Usar una imagen base de Python
FROM python:3.9-slim-bullseye

# Establece la variable de entorno para desactivar el buffering de Python
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema y bibliotecas necesarias
RUN apt-get update && \
    apt-get install -y \
    libgtk-3-0 \
    libgtk-3-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    libmpv1 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y luego instala las dependencias
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el contenido del proyecto en el directorio de trabajo
COPY . .

# Exponer el puerto que Flet usara
EXPOSE 8551

# Comando para ejecutar la aplicación
CMD ["flet", "run", "--android"]
