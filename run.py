#!/usr/bin/env python3
"""
Script de inicio para Cine Norte
Ejecuta la aplicación con configuración automática
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'streamlit', 'requests', 'beautifulsoup4', 'openai', 
        'moviepy', 'Pillow', 'numpy', 'pandas', 'python-dotenv',
        'gtts', 'pydub', 'opencv-python', 'scikit-image', 
        'matplotlib', 'seaborn', 'textblob', 'transformers', 'torch'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Faltan dependencias: {', '.join(missing_packages)}")
        print("📦 Instalando dependencias faltantes...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias. Ejecuta manualmente:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ Todas las dependencias están instaladas")
    
    return True

def check_config():
    """Verifica la configuración del sistema"""
    print("⚙️ Verificando configuración...")
    
    # Verificar archivo .env
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️ Archivo .env no encontrado. Creando desde plantilla...")
        try:
            with open('env_example.txt', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✅ Archivo .env creado. Configura tus claves de API.")
        except FileNotFoundError:
            print("❌ No se encontró env_example.txt")
            return False
    
    # Verificar directorios necesarios
    directories = ['output', 'temp', 'assets']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Configuración verificada")
    return True

def check_apis():
    """Verifica las claves de API"""
    print("🔑 Verificando claves de API...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        tmdb_key = os.getenv('TMDB_API_KEY')
        
        if not openai_key:
            print("⚠️ OPENAI_API_KEY no configurada. Algunas funciones estarán limitadas.")
        else:
            print("✅ OpenAI API configurada")
        
        if not tmdb_key:
            print("⚠️ TMDB_API_KEY no configurada. El análisis de contenido estará limitado.")
        else:
            print("✅ TMDB API configurada")
        
        return True
        
    except ImportError:
        print("❌ python-dotenv no instalado")
        return False

def start_application():
    """Inicia la aplicación Streamlit"""
    print("🚀 Iniciando Cine Norte...")
    print("🌐 La aplicación se abrirá en tu navegador")
    print("📱 URL: http://localhost:8501")
    print("⏹️ Presiona Ctrl+C para detener la aplicación")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'main_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego! Cine Norte se ha detenido.")
    except Exception as e:
        print(f"❌ Error iniciando la aplicación: {e}")

def main():
    """Función principal"""
    print("🎬 CINE NORTE - Generador Automatizado de Contenido")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar configuración
    if not check_config():
        sys.exit(1)
    
    # Verificar APIs
    check_apis()
    
    print("\n✅ Sistema listo para usar")
    print("🎯 Funcionalidades disponibles:")
    print("   • Análisis de contenido de streaming")
    print("   • Generación de guiones con IA")
    print("   • Síntesis de voz y subtítulos")
    print("   • Creación de videos con branding")
    print("   • Formatos múltiples para redes sociales")
    print("   • Optimización con IA")
    print("   • Generación de miniaturas")
    
    # Preguntar si continuar
    response = input("\n¿Continuar? (s/n): ").lower().strip()
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        start_application()
    else:
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
