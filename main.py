"""
Cine Norte - Sistema de Generación de Contenido Automatizado
Interfaz principal del sistema
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

# Importar módulos del sistema
from src.content_analyzer import ContentAnalyzer, ContentItem
from src.script_generator import ScriptGenerator, GeneratedScript
from src.voice_generator import VoiceGenerator
from src.video_editor import VideoEditor, VideoProject
from src.multi_format_generator import MultiFormatGenerator
from src.ai_optimizer import AIOptimizer, ImpactAnalysis
from src.thumbnail_generator import ThumbnailGenerator, SEOData

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/cine_norte.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CineNorteSystem:
    """Sistema principal de Cine Norte"""
    
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
        self.script_generator = ScriptGenerator()
        self.voice_generator = VoiceGenerator()
        self.video_editor = VideoEditor()
        self.multi_format_generator = MultiFormatGenerator()
        self.ai_optimizer = AIOptimizer()
        self.thumbnail_generator = ThumbnailGenerator()
        
        logger.info("Sistema Cine Norte inicializado exitosamente")
    
    def generate_content(self, content_query: str = None, content_type: str = "movie", 
                        style: str = "engaging") -> Dict[str, str]:
        """
        Genera contenido completo para Cine Norte
        
        Args:
            content_query: Búsqueda específica de contenido (opcional)
            content_type: Tipo de contenido ('movie' o 'tv')
            style: Estilo del guion ('engaging', 'dramatic', 'informative')
            
        Returns:
            Diccionario con rutas de archivos generados
        """
        try:
            logger.info(f"Iniciando generación de contenido: {content_query or 'recomendado'}")
            
            # 1. Seleccionar contenido
            content = self._select_content(content_query, content_type)
            if not content:
                raise Exception("No se pudo seleccionar contenido")
            
            logger.info(f"Contenido seleccionado: {content.title}")
            
            # 2. Generar guion
            script = self.script_generator.generate_script(content, style)
            logger.info("Guion generado exitosamente")
            
            # 3. Generar voz
            voice_path = self.voice_generator.generate_voice_from_script(script.raw_text)
            logger.info("Voz generada exitosamente")
            
            # 4. Generar subtítulos
            subtitles = self.voice_generator.generate_subtitles(voice_path, script.raw_text)
            logger.info("Subtítulos generados exitosamente")
            
            # 5. Crear proyecto de video
            video_project = self.video_editor.create_video_project(script)
            logger.info("Proyecto de video creado exitosamente")
            
            # 6. Generar videos en múltiples formatos
            video_paths = self.multi_format_generator.generate_all_formats(video_project)
            logger.info("Videos en múltiples formatos generados exitosamente")
            
            # 7. Generar miniaturas
            thumbnail_paths = self.multi_format_generator.generate_thumbnails(video_project)
            logger.info("Miniaturas generadas exitosamente")
            
            # 8. Análisis de impacto con IA
            impact_analysis = self.ai_optimizer.analyze_content_impact(video_project)
            logger.info("Análisis de impacto completado")
            
            # 9. Generar datos SEO
            seo_data = self.thumbnail_generator.generate_seo_data(script)
            logger.info("Datos SEO generados exitosamente")
            
            # 10. Guardar archivos de texto
            script_path = self.script_generator.save_script_to_file(script)
            
            # Guardar subtítulos
            subtitles_srt = self.voice_generator.save_subtitles_srt(subtitles, "output/subtitles.srt")
            subtitles_vtt = self.voice_generator.save_subtitles_vtt(subtitles, "output/subtitles.vtt")
            
            # Guardar reporte de análisis
            analysis_report = self.ai_optimizer.save_analysis_report(
                impact_analysis, "output/analysis_report.json"
            )
            
            # Compilar resultados
            results = {
                "content": {
                    "title": content.title,
                    "type": content.content_type,
                    "rating": content.rating,
                    "genres": content.genres
                },
                "files": {
                    "script": script_path,
                    "voice": voice_path,
                    "subtitles_srt": subtitles_srt,
                    "subtitles_vtt": subtitles_vtt,
                    "analysis_report": analysis_report
                },
                "videos": video_paths,
                "thumbnails": thumbnail_paths,
                "seo_data": {
                    "title": seo_data.title,
                    "description": seo_data.description,
                    "keywords": seo_data.keywords,
                    "hashtags": seo_data.hashtags,
                    "tags": seo_data.tags
                },
                "analysis": {
                    "overall_score": impact_analysis.overall_score,
                    "engagement_score": impact_analysis.engagement_score,
                    "viral_potential": impact_analysis.viral_potential,
                    "seo_score": impact_analysis.seo_score,
                    "visual_appeal": impact_analysis.visual_appeal
                }
            }
            
            logger.info("Generación de contenido completada exitosamente")
            return results
            
        except Exception as e:
            logger.error(f"Error generando contenido: {e}")
            return {"error": str(e)}
    
    def _select_content(self, content_query: str = None, content_type: str = "movie") -> Optional[ContentItem]:
        """Selecciona contenido para analizar"""
        try:
            if content_query:
                # Buscar contenido específico
                results = self.content_analyzer.search_content(content_query, content_type)
                if results:
                    return results[0]
            
            # Obtener contenido recomendado
            recommended = self.content_analyzer.get_recommended_content(limit=5)
            if recommended:
                return recommended[0]
            
            # Obtener contenido trending como respaldo
            trending = self.content_analyzer.get_trending_content(content_type, "week")
            if trending:
                return trending[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error seleccionando contenido: {e}")
            return None
    
    def generate_batch_content(self, count: int = 5, content_type: str = "movie") -> List[Dict[str, str]]:
        """
        Genera múltiples contenidos en lote
        
        Args:
            count: Número de contenidos a generar
            content_type: Tipo de contenido
            
        Returns:
            Lista de resultados de generación
        """
        try:
            logger.info(f"Iniciando generación en lote: {count} contenidos")
            
            results = []
            
            # Obtener lista de contenidos
            contents = self.content_analyzer.get_recommended_content(limit=count)
            
            for i, content in enumerate(contents):
                try:
                    logger.info(f"Generando contenido {i+1}/{count}: {content.title}")
                    
                    result = self.generate_content(
                        content_query=content.title,
                        content_type=content.content_type
                    )
                    
                    results.append(result)
                    
                except Exception as e:
                    logger.error(f"Error generando contenido {i+1}: {e}")
                    results.append({"error": str(e), "content": content.title})
            
            logger.info(f"Generación en lote completada: {len(results)} contenidos")
            return results
            
        except Exception as e:
            logger.error(f"Error en generación en lote: {e}")
            return []
    
    def optimize_existing_content(self, script_path: str) -> Dict[str, str]:
        """
        Optimiza contenido existente
        
        Args:
            script_path: Ruta del guion existente
            
        Returns:
            Diccionario con sugerencias de optimización
        """
        try:
            logger.info(f"Optimizando contenido existente: {script_path}")
            
            # Cargar guion existente
            with open(script_path, 'r', encoding='utf-8') as f:
                script_text = f.read()
            
            # Crear objeto de guion temporal
            # (En una implementación real, esto sería más sofisticado)
            temp_script = GeneratedScript(
                title="Contenido a optimizar",
                content=None,
                segments=[],
                total_duration=0,
                hashtags=[],
                description="",
                thumbnail_prompts=[],
                raw_text=script_text
            )
            
            # Generar sugerencias de optimización
            suggestions = self.ai_optimizer.generate_optimization_suggestions(
                VideoProject(
                    title="Optimización",
                    script=temp_script,
                    elements=[],
                    background_music="",
                    intro_clip="",
                    outro_clip="",
                    duration=0
                )
            )
            
            # Guardar sugerencias
            suggestions_path = "output/optimization_suggestions.json"
            with open(suggestions_path, 'w', encoding='utf-8') as f:
                import json
                json.dump([{
                    "type": s.type,
                    "priority": s.priority,
                    "description": s.description,
                    "impact": s.impact,
                    "implementation": s.implementation
                } for s in suggestions], f, indent=2, ensure_ascii=False)
            
            logger.info("Optimización completada exitosamente")
            return {
                "suggestions": suggestions_path,
                "count": len(suggestions)
            }
            
        except Exception as e:
            logger.error(f"Error optimizando contenido: {e}")
            return {"error": str(e)}
    
    def get_system_status(self) -> Dict[str, str]:
        """Obtiene el estado del sistema"""
        try:
            status = {
                "timestamp": datetime.now().isoformat(),
                "content_analyzer": "OK" if self.content_analyzer else "ERROR",
                "script_generator": "OK" if self.script_generator else "ERROR",
                "voice_generator": "OK" if self.voice_generator else "ERROR",
                "video_editor": "OK" if self.video_editor else "ERROR",
                "multi_format_generator": "OK" if self.multi_format_generator else "ERROR",
                "ai_optimizer": "OK" if self.ai_optimizer else "ERROR",
                "thumbnail_generator": "OK" if self.thumbnail_generator else "ERROR"
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error obteniendo estado del sistema: {e}")
            return {"error": str(e)}

def main():
    """Función principal"""
    try:
        print("🎬 CINE NORTE - Sistema de Generación de Contenido Automatizado")
        print("=" * 60)
        
        # Inicializar sistema
        system = CineNorteSystem()
        
        # Mostrar estado del sistema
        status = system.get_system_status()
        print("\n📊 Estado del Sistema:")
        for component, state in status.items():
            if component != "timestamp":
                emoji = "✅" if state == "OK" else "❌"
                print(f"  {emoji} {component}: {state}")
        
        # Menú interactivo
        while True:
            print("\n" + "=" * 60)
            print("📋 MENÚ PRINCIPAL")
            print("=" * 60)
            print("1. 🎬 Generar contenido individual")
            print("2. 📦 Generar contenido en lote")
            print("3. 🔧 Optimizar contenido existente")
            print("4. 📊 Ver estado del sistema")
            print("5. ❌ Salir")
            print("=" * 60)
            
            choice = input("\nSelecciona una opción (1-5): ").strip()
            
            if choice == "1":
                # Generar contenido individual
                print("\n🎬 GENERAR CONTENIDO INDIVIDUAL")
                print("-" * 40)
                
                content_query = input("Búsqueda específica (opcional): ").strip()
                content_type = input("Tipo (movie/tv) [movie]: ").strip() or "movie"
                style = input("Estilo (engaging/dramatic/informative) [engaging]: ").strip() or "engaging"
                
                print("\n⏳ Generando contenido...")
                result = system.generate_content(content_query, content_type, style)
                
                if "error" in result:
                    print(f"❌ Error: {result['error']}")
                else:
                    print("✅ Contenido generado exitosamente!")
                    print(f"📝 Título: {result['content']['title']}")
                    print(f"⭐ Rating: {result['content']['rating']}/10")
                    print(f"📊 Score general: {result['analysis']['overall_score']:.2f}")
                    print(f"📁 Archivos generados en: output/")
            
            elif choice == "2":
                # Generar contenido en lote
                print("\n📦 GENERAR CONTENIDO EN LOTE")
                print("-" * 40)
                
                count = input("Número de contenidos [5]: ").strip()
                count = int(count) if count.isdigit() else 5
                content_type = input("Tipo (movie/tv) [movie]: ").strip() or "movie"
                
                print(f"\n⏳ Generando {count} contenidos...")
                results = system.generate_batch_content(count, content_type)
                
                successful = sum(1 for r in results if "error" not in r)
                print(f"✅ Generación completada: {successful}/{count} exitosos")
                print(f"📁 Archivos generados en: output/")
            
            elif choice == "3":
                # Optimizar contenido existente
                print("\n🔧 OPTIMIZAR CONTENIDO EXISTENTE")
                print("-" * 40)
                
                script_path = input("Ruta del guion: ").strip()
                
                if os.path.exists(script_path):
                    print("\n⏳ Analizando contenido...")
                    result = system.optimize_existing_content(script_path)
                    
                    if "error" in result:
                        print(f"❌ Error: {result['error']}")
                    else:
                        print(f"✅ Optimización completada!")
                        print(f"💡 Sugerencias generadas: {result['count']}")
                        print(f"📁 Archivo: {result['suggestions']}")
                else:
                    print("❌ Archivo no encontrado")
            
            elif choice == "4":
                # Ver estado del sistema
                print("\n📊 ESTADO DEL SISTEMA")
                print("-" * 40)
                
                status = system.get_system_status()
                for component, state in status.items():
                    if component != "timestamp":
                        emoji = "✅" if state == "OK" else "❌"
                        print(f"{emoji} {component}: {state}")
                
                print(f"\n🕒 Última actualización: {status.get('timestamp', 'N/A')}")
            
            elif choice == "5":
                # Salir
                print("\n👋 ¡Hasta luego! Gracias por usar Cine Norte")
                break
            
            else:
                print("❌ Opción inválida. Por favor, selecciona 1-5.")
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego! Gracias por usar Cine Norte")
    except Exception as e:
        logger.error(f"Error en función principal: {e}")
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    main()
