# Usar Ubuntu como imagen base
FROM ubuntu:20.04

# Evitar preguntas al instalar paquetes en Debian
ARG DEBIAN_FRONTEND=noninteractive

# Actualizar sistema e instalar Python, pip y otras dependencias
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.8-dev \
    libgl1-mesa-glx \
    libx11-xcb1 \
    libfontconfig1 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip3 install --upgrade pip

# Instalar sip y pyqt5 antes del resto
RUN pip3 install sip==6.6.2 pyqt5

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y el código fuente al contenedor
COPY requirements.txt /app/
COPY . /app/

# Instala las dependencias de Python
RUN pip3 install sip==6.6.2
RUN pip3 install pyqt5
RUN pip3 install -r requirements.txt
RUN pip3 install ultralytics==8.0.230 opencv-python PyQt5 QT-PyQt-PySide-Custom-Widgets

# Expone el puerto que necesitas (si es una aplicación web o de servidor)
# EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python3", "main.py"]
