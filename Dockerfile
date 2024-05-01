# Usamos Ubuntu como base
FROM ubuntu:20.04

# Evita preguntas al instalar paquetes en Debian
ARG DEBIAN_FRONTEND=noninteractive

# Actualiza el sistema y instala Python y pip
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.8-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y el código fuente al contenedor
COPY requirements.txt /app/
COPY . /app/

# Instala las dependencias de Python
RUN pip3 install -r requirements.txt
RUN pip3 install ultralytics==8.0.230 opencv-python PyQt5 QT-PyQt-PySide-Custom-Widgets

# Expone el puerto que necesitas (si es una aplicación web o de servidor)
# EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python3", "main.py"]
