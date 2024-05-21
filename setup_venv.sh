#!/bin/bash

# Verificar que pip esté instalado
if ! command -v pip3 &> /dev/null; then
    echo "pip3 no está instalado. Instalando pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Verificar que virtualenv esté instalado
if ! pip3 show virtualenv &> /dev/null; then
    echo "virtualenv no está instalado. Instalando virtualenv..."
    pip3 install virtualenv
fi

# Nombre del entorno virtual
VENV_NAME="env"

# Verificar si ya existe un entorno virtual con el nombre especificado
if [ -d "$VENV_NAME" ]; then
    echo "El entorno virtual '$VENV_NAME' ya existe."
else
    # Crear el entorno virtual
    echo "Creando el entorno virtual '$VENV_NAME'..."
    python3 -m virtualenv $VENV_NAME
fi

# Activar el entorno virtual
echo "Activando el entorno virtual '$VENV_NAME'..."
source $VENV_NAME/bin/activate

# Instalar las dependencias desde requirements.txt si el archivo existe
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "Archivo requirements.txt no encontrado. Asegúrate de tenerlo en el directorio actual."
fi

# Instalar bibliotecas adicionales específicas
echo "Instalando ultralytics, opencv-python, PyQt5, y QT-PyQt-PySide-Custom-Widgets..."
pip install ultralytics==8.0.230 opencv-python PyQt5 QT-PyQt-PySide-Custom-Widgets sip==6.6.2 pyqt5 PySide6


echo "Configuración completa. El entorno virtual está listo para usar."
