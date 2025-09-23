"""
Script de configuración para Cine Norte
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """Crea los directorios necesarios"""
    directories = [
        "output",
        "output/videos",
        "output/thumbnails", 
        "output/scripts",
        "output/audio",
        "output/subtitles",
        "temp",
        "temp/audio",
        "temp/video",
        "temp/thumbnails",
        "temp/formats",
        "assets",
        "assets/music",
        "assets/fonts",
        "assets/images",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def install_dependencies():
    """Instala las dependencias de Python"""
    try:
        print("📦 Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_minimal.txt"])
        print("✅ Dependencias instaladas exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    return True

def create_env_file():
    """Crea el archivo .env si no existe"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        env_example.rename(env_file)
        print("✅ Archivo .env creado desde env.example")
        print("⚠️  Recuerda configurar tus API keys en el archivo .env")
    elif env_file.exists():
        print("✅ Archivo .env ya existe")
    else:
        print("⚠️  No se encontró env.example, crea manualmente el archivo .env")

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    else:
        print(f"✅ Versión de Python: {sys.version}")
        return True

def main():
    """Función principal de configuración"""
    print("🎬 CINE NORTE - Configuración del Sistema")
    print("=" * 50)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear directorios
    print("\n📁 Creando directorios...")
    create_directories()
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias...")
    if not install_dependencies():
        print("❌ Error en la instalación. Revisa los logs.")
        sys.exit(1)
    
    # Crear archivo .env
    print("\n⚙️  Configurando variables de entorno...")
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 50)
    print("\n📋 Próximos pasos:")
    print("1. Configura tus API keys en el archivo .env")
    print("2. Ejecuta: python main.py")
    print("3. ¡Disfruta generando contenido con Cine Norte!")
    print("\n🎬 ¡Bienvenido a Cine Norte!")

if __name__ == "__main__":
    main()
