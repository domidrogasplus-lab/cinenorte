"""
Generador de guiones con IA para Cine Norte
Crea guiones optimizados para videos de redes sociales
"""
import openai
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re
from config import config
from content_analyzer import ContentInfo

@dataclass
class ScriptSection:
    """Sección de un guion"""
    type: str  # 'intro', 'hook', 'plot', 'analysis', 'outro'
    content: str
    duration_seconds: int
    visual_cues: List[str]
    emotion: str  # 'excitement', 'suspense', 'drama', 'comedy'
    emphasis_words: List[str]

@dataclass
class GeneratedScript:
    """Guion generado completo"""
    title: str
    content: ContentInfo
    sections: List[ScriptSection]
    total_duration: int
    word_count: int
    target_platform: str
    hashtags: List[str]
    title_suggestions: List[str]
    visual_style: str
    music_suggestion: str
    raw_text: str

class ScriptGenerator:
    """Generador de guiones con IA"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.logger = logging.getLogger(__name__)
        
    def generate_script(self, content: ContentInfo, target_platform: str = "youtube", 
                       duration_target: int = 120, style: str = "dynamic") -> GeneratedScript:
        """
        Genera un guion completo para el contenido
        
        Args:
            content: Información del contenido
            target_platform: Plataforma objetivo (youtube, tiktok, instagram)
            duration_target: Duración objetivo en segundos
            style: Estilo del guion (dynamic, dramatic, comedic, analytical)
        """
        try:
            # Generar prompt base
            prompt = self._create_base_prompt(content, target_platform, duration_target, style)
            
            # Generar guion con OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            script_text = response.choices[0].message.content
            
            # Procesar y estructurar el guion
            sections = self._parse_script_sections(script_text, content)
            
            # Generar metadatos adicionales
            hashtags = self._generate_hashtags(content, target_platform)
            title_suggestions = self._generate_title_suggestions(content, target_platform)
            visual_style = self._determine_visual_style(content, style)
            music_suggestion = self._suggest_music(content, style)
            
            # Calcular duración total
            total_duration = sum(section.duration_seconds for section in sections)
            
            return GeneratedScript(
                title=content.title,
                content=content,
                sections=sections,
                total_duration=total_duration,
                word_count=len(script_text.split()),
                target_platform=target_platform,
                hashtags=hashtags,
                title_suggestions=title_suggestions,
                visual_style=visual_style,
                music_suggestion=music_suggestion,
                raw_text=script_text
            )
            
        except Exception as e:
            self.logger.error(f"Error generando guion: {e}")
            return self._create_fallback_script(content, target_platform)
    
    def _get_system_prompt(self) -> str:
        """Prompt del sistema para la IA"""
        return """
        Eres un experto editor audiovisual y creador de contenido para Cine Norte, 
        una marca especializada en análisis cinematográfico para redes sociales.
        
        Tu misión es crear guiones dinámicos, atractivos y optimizados para engagement
        que mantengan la identidad de marca de Cine Norte.
        
        Características de Cine Norte:
        - Paleta de colores: Rojo #E50914, Negro #0A0A0A, Plateado #C0C0C0
        - Estilo: Cinematográfico, profesional, con toque de misterio
        - Audiencia: Cinéfilos, amantes del entretenimiento, usuarios de redes sociales
        - Duración: Máximo 3 minutos por video
        
        Reglas importantes:
        1. NO reveles spoilers importantes de la trama
        2. Mantén un tono dinámico y emocionante
        3. Incluye elementos visuales y de audio específicos
        4. Optimiza para la plataforma objetivo
        5. Usa lenguaje natural y conversacional
        6. Incluye call-to-actions para engagement
        """
    
    def _create_base_prompt(self, content: ContentInfo, target_platform: str, 
                           duration_target: int, style: str) -> str:
        """Crea el prompt base para la generación"""
        
        platform_instructions = {
            "youtube": "Optimizado para YouTube: guion más largo, análisis detallado, intros/outros elaborados",
            "tiktok": "Optimizado para TikTok: guion corto y directo, hooks inmediatos, ritmo acelerado",
            "instagram": "Optimizado para Instagram: visual, estético, historias en highlights"
        }
        
        style_instructions = {
            "dynamic": "Estilo dinámico: ritmo rápido, cortes frecuentes, mucha energía",
            "dramatic": "Estilo dramático: pausas estratégicas, énfasis emocional, tensión",
            "comedic": "Estilo cómico: humor sutil, comentarios ingeniosos, tono ligero",
            "analytical": "Estilo analítico: enfoque en técnica, dirección, actuaciones"
        }
        
        return f"""
        Crea un guion para un video de Cine Norte sobre:
        
        TÍTULO: {content.title}
        TIPO: {content.content_type.upper()}
        GÉNERO: {', '.join(content.genre)}
        PLATAFORMA: {content.platform}
        RATING: {content.rating}/10
        SINOPSIS: {content.overview}
        FECHA DE ESTRENO: {content.release_date}
        DURACIÓN OBJETIVO: {duration_target} segundos
        
        INSTRUCCIONES ESPECÍFICAS:
        - Plataforma: {platform_instructions.get(target_platform, 'General')}
        - Estilo: {style_instructions.get(style, 'Dinámico')}
        - Duración máxima: 3 minutos
        - Idioma: Español (México)
        - Sin spoilers importantes
        
        ESTRUCTURA REQUERIDA:
        1. INTRO (5-10 seg): Hook inmediato + presentación Cine Norte
        2. HOOK (10-15 seg): Elemento más atractivo sin spoilers
        3. PLOT (60-90 seg): Resumen de trama con análisis
        4. ANÁLISIS (30-45 seg): Aspectos técnicos o temáticos
        5. OUTRO (10-15 seg): Call-to-action + despedida
        
        Para cada sección incluye:
        - Texto del guion
        - Duración estimada en segundos
        - Indicaciones visuales específicas
        - Palabras clave para énfasis
        - Emoción objetivo
        
        Formato de respuesta en JSON estructurado.
        """
    
    def _parse_script_sections(self, script_text: str, content: ContentInfo) -> List[ScriptSection]:
        """Parsea el texto del guion en secciones estructuradas"""
        sections = []
        
        # Intentar extraer JSON estructurado
        try:
            # Buscar JSON en el texto
            json_match = re.search(r'\{.*\}', script_text, re.DOTALL)
            if json_match:
                script_data = json.loads(json_match.group())
                return self._parse_json_sections(script_data)
        except:
            pass
        
        # Fallback: parsear texto plano
        return self._parse_text_sections(script_text, content)
    
    def _parse_json_sections(self, script_data: Dict) -> List[ScriptSection]:
        """Parsea secciones desde JSON estructurado"""
        sections = []
        
        for section_data in script_data.get("sections", []):
            section = ScriptSection(
                type=section_data.get("type", "plot"),
                content=section_data.get("content", ""),
                duration_seconds=section_data.get("duration_seconds", 30),
                visual_cues=section_data.get("visual_cues", []),
                emotion=section_data.get("emotion", "neutral"),
                emphasis_words=section_data.get("emphasis_words", [])
            )
            sections.append(section)
        
        return sections
    
    def _parse_text_sections(self, script_text: str, content: ContentInfo) -> List[ScriptSection]:
        """Parsea secciones desde texto plano"""
        sections = []
        
        # Dividir por secciones comunes
        section_patterns = [
            (r'(?:INTRO|INTRODUCCIÓN)', 'intro'),
            (r'(?:HOOK|GANCHO)', 'hook'),
            (r'(?:PLOT|TRAMA|SINOPSIS)', 'plot'),
            (r'(?:ANÁLISIS|ANALISIS)', 'analysis'),
            (r'(?:OUTRO|CIERRE|CONCLUSIÓN)', 'outro')
        ]
        
        current_section = "plot"
        current_content = []
        
        lines = script_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Verificar si es inicio de nueva sección
            section_found = False
            for pattern, section_type in section_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Guardar sección anterior
                    if current_content:
                        sections.append(self._create_section_from_text(
                            current_section, '\n'.join(current_content), content
                        ))
                    
                    # Iniciar nueva sección
                    current_section = section_type
                    current_content = []
                    section_found = True
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Agregar última sección
        if current_content:
            sections.append(self._create_section_from_text(
                current_section, '\n'.join(current_content), content
            ))
        
        return sections
    
    def _create_section_from_text(self, section_type: str, content: str, 
                                 content_info: ContentInfo) -> ScriptSection:
        """Crea una sección desde texto plano"""
        
        # Calcular duración estimada (150 palabras por minuto)
        word_count = len(content.split())
        duration = max(10, int((word_count / 150) * 60))
        
        # Determinar emoción basada en el tipo de sección
        emotion_map = {
            "intro": "excitement",
            "hook": "suspense", 
            "plot": "drama",
            "analysis": "neutral",
            "outro": "excitement"
        }
        
        # Generar indicaciones visuales básicas
        visual_cues = self._generate_visual_cues(section_type, content_info)
        
        # Extraer palabras de énfasis
        emphasis_words = self._extract_emphasis_words(content)
        
        return ScriptSection(
            type=section_type,
            content=content,
            duration_seconds=duration,
            visual_cues=visual_cues,
            emotion=emotion_map.get(section_type, "neutral"),
            emphasis_words=emphasis_words
        )
    
    def _generate_visual_cues(self, section_type: str, content_info: ContentInfo) -> List[str]:
        """Genera indicaciones visuales para cada sección"""
        cues = []
        
        if section_type == "intro":
            cues.extend([
                "Logo Cine Norte animado",
                "Efecto de luces de reflector",
                "Transición dinámica"
            ])
        elif section_type == "hook":
            cues.extend([
                "Clip más impactante del tráiler",
                "Texto en pantalla con título",
                "Efecto de zoom dramático"
            ])
        elif section_type == "plot":
            cues.extend([
                "Montaje de escenas clave",
                "Texto descriptivo superpuesto",
                "Transiciones suaves"
            ])
        elif section_type == "analysis":
            cues.extend([
                "Split screen con comparaciones",
                "Gráficos informativos",
                "Efectos de partículas"
            ])
        elif section_type == "outro":
            cues.extend([
                "Logo Cine Norte final",
                "Call-to-action visual",
                "Fade out elegante"
            ])
        
        return cues
    
    def _extract_emphasis_words(self, content: str) -> List[str]:
        """Extrae palabras clave para énfasis en audio"""
        # Palabras que requieren énfasis
        emphasis_patterns = [
            r'\b(?:increíble|espectacular|impresionante|sorprendente)\b',
            r'\b(?:nunca|siempre|definitivamente|absolutamente)\b',
            r'\b(?:¡.*!)\b',  # Exclamaciones
            r'\b(?:más|mejor|peor|único|especial)\b'
        ]
        
        emphasis_words = []
        for pattern in emphasis_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            emphasis_words.extend(matches)
        
        return list(set(emphasis_words))[:5]  # Máximo 5 palabras
    
    def _generate_hashtags(self, content: ContentInfo, target_platform: str) -> List[str]:
        """Genera hashtags optimizados"""
        hashtags = config.HASHTAGS_BASE.copy()
        
        # Agregar hashtags específicos del contenido
        hashtags.extend([
            f"#{content.title.replace(' ', '')}",
            f"#{content.platform.replace(' ', '')}",
            f"#{content.content_type.upper()}"
        ])
        
        # Agregar hashtags por género
        for genre in content.genre[:3]:  # Máximo 3 géneros
            hashtags.append(f"#{genre.replace(' ', '')}")
        
        # Hashtags específicos por plataforma
        platform_hashtags = {
            "youtube": ["#YouTube", "#CineNorte", "#AnálisisCinematográfico"],
            "tiktok": ["#TikTok", "#FYP", "#CineTok"],
            "instagram": ["#Instagram", "#Reels", "#CineNorte"]
        }
        
        hashtags.extend(platform_hashtags.get(target_platform, []))
        
        return hashtags[:15]  # Máximo 15 hashtags
    
    def _generate_title_suggestions(self, content: ContentInfo, target_platform: str) -> List[str]:
        """Genera sugerencias de títulos optimizados"""
        base_title = content.title
        
        suggestions = [
            f"¿Vale la pena ver {base_title}? | Análisis Cine Norte",
            f"{base_title}: Todo lo que necesitas saber",
            f"Mi opinión sobre {base_title} | Sin spoilers",
            f"{base_title} - Reseña completa en 3 minutos",
            f"¿{base_title} es tan buena como dicen? | Cine Norte"
        ]
        
        # Ajustar para TikTok (más cortos)
        if target_platform == "tiktok":
            suggestions = [
                f"{base_title} en 60 segundos",
                f"Mi veredicto: {base_title}",
                f"{base_title} - ¿Sí o no?",
                f"Todo sobre {base_title}",
                f"{base_title} - Sin spoilers"
            ]
        
        return suggestions[:5]
    
    def _determine_visual_style(self, content: ContentInfo, style: str) -> str:
        """Determina el estilo visual recomendado"""
        if "Acción" in content.genre or "Ciencia Ficción" in content.genre:
            return "high_energy"
        elif "Drama" in content.genre or "Romance" in content.genre:
            return "cinematic"
        elif "Terror" in content.genre or "Suspenso" in content.genre:
            return "dark_mysterious"
        elif "Comedia" in content.genre:
            return "bright_playful"
        else:
            return "professional"
    
    def _suggest_music(self, content: ContentInfo, style: str) -> str:
        """Sugiere música de fondo"""
        if "Acción" in content.genre:
            return "epic_action"
        elif "Drama" in content.genre:
            return "emotional_drama"
        elif "Terror" in content.genre:
            return "tense_horror"
        elif "Comedia" in content.genre:
            return "light_comedy"
        else:
            return "cinematic_ambient"
    
    def _create_fallback_script(self, content: ContentInfo, target_platform: str) -> GeneratedScript:
        """Crea un guion de respaldo si falla la IA"""
        intro_text = f"¡Hola cinéfilos! Bienvenidos a Cine Norte. Hoy analizamos {content.title}."
        plot_text = f"{content.overview[:200]}..."
        outro_text = "¿Qué opinas de esta película? Déjanos tu comentario y suscríbete para más análisis."
        
        sections = [
            ScriptSection("intro", intro_text, 10, ["Logo Cine Norte"], "excitement", ["cinéfilos"]),
            ScriptSection("plot", plot_text, 60, ["Montaje de escenas"], "drama", []),
            ScriptSection("outro", outro_text, 15, ["Call-to-action"], "excitement", ["comentario"])
        ]
        
        return GeneratedScript(
            title=content.title,
            content=content,
            sections=sections,
            total_duration=85,
            word_count=len(intro_text + plot_text + outro_text.split()),
            target_platform=target_platform,
            hashtags=config.HASHTAGS_BASE[:10],
            title_suggestions=[f"Análisis de {content.title}"],
            visual_style="professional",
            music_suggestion="cinematic_ambient",
            raw_text=intro_text + "\n\n" + plot_text + "\n\n" + outro_text
        )
    
    def export_script_to_txt(self, script: GeneratedScript, filename: str = None) -> str:
        """Exporta el guion a archivo .txt"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"guion_{script.title.replace(' ', '_')}_{timestamp}.txt"
        
        content = f"""
GUION CINE NORTE
================
Título: {script.title}
Plataforma: {script.target_platform}
Duración: {script.total_duration} segundos
Palabras: {script.word_count}

HASHTAGS:
{', '.join(script.hashtags)}

TÍTULOS SUGERIDOS:
{chr(10).join(f"- {title}" for title in script.title_suggestions)}

ESTILO VISUAL: {script.visual_style}
MÚSICA: {script.music_suggestion}

GUION:
======

"""
        
        for i, section in enumerate(script.sections, 1):
            content += f"""
SECCIÓN {i}: {section.type.upper()}
Duración: {section.duration_seconds}s
Emoción: {section.emotion}
Indicaciones visuales: {', '.join(section.visual_cues)}

{section.content}

"""
        
        # Guardar archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename

# Instancia global del generador
script_generator = ScriptGenerator()
