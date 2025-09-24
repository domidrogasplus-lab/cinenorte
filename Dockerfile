# Dockerfile para Cine Norte
FROM python:3.9-slim

# Metadatos
LABEL maintainer="Cine Norte Team <soporte@cinenorte.com>"
LABEL description="Generador Automatizado de Contenido Audiovisual"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libice6 \
    libx11-6 \
    libxau6 \
    libxdmcp6 \
    libxext6 \
    libxss1 \
    libxt6 \
    libgthread-2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libatspi2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxss1 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p output temp assets

# Configurar permisos
RUN chmod +x run.py

# Exponer puerto
EXPOSE 8501

# Comando de inicio
CMD ["python", "run.py"]
