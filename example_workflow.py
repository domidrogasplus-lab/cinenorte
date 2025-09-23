#!/usr/bin/env python3
"""
Ejemplo de flujo completo Cine Norte
Demuestra cómo usar el sistema de automatización
"""

import os
import sys
import yaml
from pathlib import Path
from cine_norte_automation import CineNorteAutomation

def main():
    """Ejemplo de flujo completo"""
    print("🎬 Cine Norte Automation - Ejemplo de Flujo Completo")
    print("=" * 60)
    
    # Verificar que existe el archivo de configuración
    if not os.path.exists('config.yaml'):
        print("❌ Archivo config.yaml no encontrado")
        print("   Copia config.yaml.example a config.yaml y configura tus APIs")
        return
    
    # Inicializar sistema
    try:
        automation = CineNorteAutomation('config.yaml')
        print("✅ Sistema inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return
    
    # Ejemplo 1: Seleccionar contenido
    print("\n📋 Paso 1: Seleccionando contenido...")
    content_list = automation.select_content(platform="Netflix", limit=2)
    
    if not content_list:
        print("❌ No se encontró contenido")
        return
    
    print(f"✅ Encontrados {len(content_list)} contenidos:")
    for content in content_list:
        print(f"   • {content['title']} ({content['year']}) - {content['platform']}")
    
    # Ejemplo 2: Procesar primer contenido
    content = content_list[0]
    print(f"\n🎬 Paso 2: Procesando {content['title']}...")
    
    try:
        results = automation.run_full_workflow(content)
        
        # Mostrar resultados
        print(f"\n📊 Resultados para {content['title']}:")
        print(f"   ✅ Guion generado: {'✓' if results['script'] else '✗'}")
        print(f"   ✅ Audio generado: {'✓' if results['audio'] else '✗'}")
        print(f"   ✅ Subtítulos generados: {'✓' if results['subtitles'] else '✗'}")
        print(f"   ✅ Miniatura creada: {'✓' if results['thumbnail'] else '✗'}")
        print(f"   ✅ Videos creados: {len(results['videos'])} formatos")
        
        if results['seo']:
            print(f"\n🔍 Contenido SEO generado:")
            print(f"   📝 Títulos sugeridos:")
            for i, title in enumerate(results['seo']['titles'][:3], 1):
                print(f"      {i}. {title}")
            
            print(f"   #️⃣ Hashtags:")
            hashtags_text = " ".join(results['seo']['hashtags'][:5])
            print(f"      {hashtags_text}")
        
        # Mostrar archivos generados
        project_name = f"{automation.project_dir.name}_{content['title'].replace(' ', '_')}"
        project_path = automation.project_dir / project_name
        
        if project_path.exists():
            print(f"\n📁 Archivos generados en: {project_path}")
            for file_path in project_path.iterdir():
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"   • {file_path.name} ({size_mb:.1f} MB)")
        
        # Mostrar videos exportados
        export_name = f"{automation.exports_dir.name}_{content['title'].replace(' ', '_')}"
        export_path = automation.exports_dir / export_name
        
        if export_path.exists():
            print(f"\n🎥 Videos exportados en: {export_path}")
            for file_path in export_path.iterdir():
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"   • {file_path.name} ({size_mb:.1f} MB)")
        
    except Exception as e:
        print(f"❌ Error procesando contenido: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎉 Ejemplo completado!")
    print(f"   Revisa los archivos generados en las carpetas 'projects' y 'exports'")

def demo_individual_steps():
    """Demostrar pasos individuales del flujo"""
    print("\n🔧 Demostración de pasos individuales:")
    print("-" * 40)
    
    automation = CineNorteAutomation('config.yaml')
    
    # Contenido de ejemplo
    sample_content = {
        "id": 999,
        "title": "Película de Ejemplo",
        "year": 2023,
        "platform": "Netflix",
        "genres": ["Drama", "Thriller"],
        "synopsis": "Una historia emocionante que te mantendrá en el borde del asiento",
        "keywords": ["suspenso", "drama", "acción"]
    }
    
    print(f"📝 Generando guion para {sample_content['title']}...")
    script = automation.generate_script(sample_content)
    if script:
        print(f"   ✅ Guion generado ({len(script)} caracteres)")
        print(f"   📄 Primeras líneas: {script[:100]}...")
    
    print(f"\n🖼️ Creando miniatura para {sample_content['title']}...")
    thumbnail = automation.create_thumbnail(sample_content)
    if thumbnail:
        print(f"   ✅ Miniatura creada: {thumbnail}")
    
    print(f"\n🔍 Generando contenido SEO...")
    seo = automation.generate_seo_content(sample_content)
    if seo:
        print(f"   ✅ {len(seo['titles'])} títulos y {len(seo['hashtags'])} hashtags generados")

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'yaml', 'requests', 'openai', 'elevenlabs', 
        'whisper', 'moviepy', 'ffmpeg', 'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("   Instala con: pip install -r requirements.txt")
        return False
    
    print("   ✅ Todas las dependencias están instaladas")
    return True

if __name__ == "__main__":
    print("🎬 Cine Norte Automation - Ejemplo de Uso")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Instala las dependencias antes de continuar")
        sys.exit(1)
    
    # Verificar configuración
    if not os.path.exists('config.yaml'):
        print("\n❌ Archivo config.yaml no encontrado")
        print("   Crea el archivo de configuración con tus API keys")
        sys.exit(1)
    
    # Ejecutar ejemplo principal
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Ejemplo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    # Demostrar pasos individuales
    try:
        demo_individual_steps()
    except Exception as e:
        print(f"\n⚠️  Error en demostración individual: {e}")
    
    print(f"\n🎯 Próximos pasos:")
    print(f"   1. Configura tus API keys en config.yaml")
    print(f"   2. Ejecuta: python cine_norte_automation.py --help")
    print(f"   3. Procesa contenido: python cine_norte_automation.py --platform Netflix")
    print(f"   4. Revisa los archivos generados en 'projects' y 'exports'")
