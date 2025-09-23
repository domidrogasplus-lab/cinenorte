"""
Generador automático de guiones para videos de Cine Norte
"""

import openai
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging
from datetime import datetime

from config import API_KEYS, CONTENT_CONFIG, BRANDING
from src.content_analyzer import ContentItem

logger = logging.getLogger(__name__)

@dataclass
class ScriptSegment:
    """Segmento del guion con timing y elementos visuales"""
    text: str
    start_time: float
    end_time: float
    visual_cues: List[str]
    emphasis_words: List[str]
    background_music: str

@dataclass
class GeneratedScript:
    """Guion completo generado"""
    title: str
    content: ContentItem
    segments: List[ScriptSegment]
    total_duration: float
    hashtags: List[str]
    description: str
    thumbnail_prompts: List[str]
    raw_text: str

class ScriptGenerator:
    """Generador de guiones automático con IA"""
    
    def __init__(self):
        self.openai_api_key = API_KEYS.get("openai")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Plantillas de guion por tipo de contenido
        self.script_templates = {
            "movie": {
                "intro": "¡Hola cinéfilos! Soy Cine Norte y hoy les traigo un análisis de {title}",
                "structure": [
                    "intro_hook",
                    "plot_summary", 
                    "key_scenes",
                    "technical_aspects",
                    "verdict",
                    "outro"
                ]
            },
            "tv": {
                "intro": "¡Bienvenidos a Cine Norte! Hoy analizamos {title}",
                "structure": [
                    "intro_hook",
                    "series_overview",
                    "season_highlights",
                    "character_analysis", 
                    "verdict",
                    "outro"
                ]
            }
        }
    
    def generate_script(self, content: ContentItem, style: str = "engaging") -> GeneratedScript:
        """
        Genera un guion completo para el contenido
        
        Args:
            content: Información del contenido
            style: Estilo del guion ('engaging', 'dramatic', 'informative')
        """
        try:
            # Generar texto base del guion
            script_text = self._generate_script_text(content, style)
            
            # Dividir en segmentos con timing
            segments = self._create_script_segments(script_text, content)
            
            # Generar metadatos
            hashtags = self._generate_hashtags(content)
            description = self._generate_description(content, script_text)
            thumbnail_prompts = self._generate_thumbnail_prompts(content)
            
            # Calcular duración total
            total_duration = sum(segment.end_time - segment.start_time for segment in segments)
            
            return GeneratedScript(
                title=f"Análisis de {content.title} - Cine Norte",
                content=content,
                segments=segments,
                total_duration=total_duration,
                hashtags=hashtags,
                description=description,
                thumbnail_prompts=thumbnail_prompts,
                raw_text=script_text
            )
            
        except Exception as e:
            logger.error(f"Error generando guion: {e}")
            return self._create_fallback_script(content)
    
    def _generate_script_text(self, content: ContentItem, style: str) -> str:
        """Genera el texto base del guion usando OpenAI"""
        try:
            if not self.openai_api_key:
                return self._generate_fallback_script(content)
            
            # Construir prompt contextual
            prompt = self._build_script_prompt(content, style)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis cinematográfico y creador de contenido para YouTube. Tu estilo es dinámico, entretenido y sin spoilers importantes. Eres parte del canal Cine Norte."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error con OpenAI: {e}")
            return self._generate_fallback_script(content)
    
    def _build_script_prompt(self, content: ContentItem, style: str) -> str:
        """Construye el prompt para la generación del guion"""
        
        # Determinar duración objetivo
        target_duration = min(CONTENT_CONFIG["max_script_length"], 400)
        
        # Estructura base
        structure = self.script_templates.get(content.content_type, self.script_templates["movie"])
        
        prompt = f"""
Genera un guion de video para YouTube de máximo {target_duration} palabras sobre:

TÍTULO: {content.title}
TIPO: {'Película' if content.content_type == 'movie' else 'Serie'}
GÉNEROS: {', '.join(content.genres)}
SINOPSIS: {content.overview}
RATING: {content.rating}/10
DURACIÓN OBJETIVO: 2-3 minutos de video

ESTILO: {style}
CANAL: Cine Norte (análisis cinematográfico en español)

ESTRUCTURA REQUERIDA:
1. Hook inicial (10-15 segundos) - Captar atención inmediatamente
2. Resumen de la trama (30-45 segundos) - Sin spoilers importantes
3. Análisis de aspectos destacados (45-60 segundos) - Actuaciones, dirección, efectos
4. Veredicto personal (20-30 segundos) - Recomendación honesta
5. Cierre con call-to-action (10-15 segundos)

REGLAS IMPORTANTES:
- Usar un tono dinámico y entretenido
- Incluir frases impactantes para el texto en pantalla
- Evitar spoilers importantes
- Mencionar elementos técnicos relevantes
- Incluir referencias a otras películas/series cuando sea apropiado
- Usar lenguaje coloquial pero profesional
- Incluir transiciones fluidas entre secciones

FORMATO: Escribe el guion completo como un solo texto fluido, sin marcas de tiempo ni indicaciones técnicas.
"""
        
        return prompt
    
    def _create_script_segments(self, script_text: str, content: ContentItem) -> List[ScriptSegment]:
        """Divide el guion en segmentos con timing y elementos visuales"""
        segments = []
        
        # Dividir el texto en párrafos
        paragraphs = [p.strip() for p in script_text.split('\n\n') if p.strip()]
        
        current_time = 0.0
        words_per_minute = 150  # Velocidad de narración
        
        for i, paragraph in enumerate(paragraphs):
            # Calcular duración basada en palabras
            word_count = len(paragraph.split())
            duration = (word_count / words_per_minute) * 60
            
            # Generar elementos visuales
            visual_cues = self._generate_visual_cues(paragraph, content, i)
            emphasis_words = self._extract_emphasis_words(paragraph)
            background_music = self._select_background_music(content, i, len(paragraphs))
            
            segment = ScriptSegment(
                text=paragraph,
                start_time=current_time,
                end_time=current_time + duration,
                visual_cues=visual_cues,
                emphasis_words=emphasis_words,
                background_music=background_music
            )
            
            segments.append(segment)
            current_time += duration
        
        return segments
    
    def _generate_visual_cues(self, text: str, content: ContentItem, segment_index: int) -> List[str]:
        """Genera indicaciones visuales para el segmento"""
        cues = []
        
        # Cues basadas en contenido del texto
        if "acción" in text.lower() or "explosión" in text.lower():
            cues.append("transición_energética")
            cues.append("efectos_visuales_dinámicos")
        
        if "suspense" in text.lower() or "misterio" in text.lower():
            cues.append("iluminación_tenue")
            cues.append("movimiento_cámara_suave")
        
        if "drama" in text.lower() or "emotivo" in text.lower():
            cues.append("primer_plano")
            cues.append("colores_saturados")
        
        # Cues basadas en el segmento
        if segment_index == 0:  # Intro
            cues.extend(["logo_cine_norte", "efecto_revelador"])
        elif segment_index == len(text.split('\n\n')) - 1:  # Outro
            cues.extend(["logo_cine_norte", "call_to_action"])
        
        # Cues específicas del contenido
        if content.content_type == "movie":
            cues.append("poster_película")
        else:
            cues.append("poster_serie")
        
        return cues
    
    def _extract_emphasis_words(self, text: str) -> List[str]:
        """Extrae palabras clave para enfatizar visualmente"""
        # Palabras de impacto común en análisis cinematográfico
        impact_words = [
            "increíble", "espectacular", "sorprendente", "impactante",
            "brillante", "genial", "perfecto", "excelente", "magnífico",
            "terrible", "decepcionante", "aburrido", "confuso"
        ]
        
        words = text.lower().split()
        emphasis = [word for word in words if any(impact in word for impact in impact_words)]
        
        return emphasis[:5]  # Máximo 5 palabras de énfasis
    
    def _select_background_music(self, content: ContentItem, segment_index: int, total_segments: int) -> str:
        """Selecciona música de fondo apropiada"""
        # Música basada en género
        genre_music = {
            "Acción": "epic_action",
            "Terror": "dark_suspense", 
            "Drama": "emotional_drama",
            "Comedia": "light_upbeat",
            "Ciencia ficción": "futuristic_synth"
        }
        
        # Música basada en el segmento
        if segment_index == 0:
            return "intro_energetic"
        elif segment_index == total_segments - 1:
            return "outro_motivational"
        else:
            # Seleccionar basado en el primer género
            if content.genres:
                first_genre = content.genres[0]
                return genre_music.get(first_genre, "neutral_cinematic")
            return "neutral_cinematic"
    
    def _generate_hashtags(self, content: ContentItem) -> List[str]:
        """Genera hashtags optimizados para SEO"""
        hashtags = []
        
        # Hashtags base
        base_tags = ["#CineNorte", "#AnálisisCinematográfico", "#Reseña"]
        hashtags.extend(base_tags)
        
        # Hashtags por tipo
        if content.content_type == "movie":
            hashtags.extend(["#Película", "#Cine", "#ReseñaPelicula"])
        else:
            hashtags.extend(["#Serie", "#TV", "#ReseñaSerie"])
        
        # Hashtags por género
        for genre in content.genres[:3]:  # Máximo 3 géneros
            genre_tag = f"#{genre.replace(' ', '')}"
            hashtags.append(genre_tag)
        
        # Hashtags por plataforma (si está disponible)
        for platform in content.platforms[:2]:  # Máximo 2 plataformas
            platform_tag = f"#{platform.replace(' ', '').replace('+', 'Plus')}"
            hashtags.append(platform_tag)
        
        # Hashtags de tendencia
        trending_tags = ["#Streaming", "#Entretenimiento", "#CulturaPop"]
        hashtags.extend(trending_tags)
        
        return hashtags[:CONTENT_CONFIG.get("max_hashtags", 10)]
    
    def _generate_description(self, content: ContentItem, script_text: str) -> str:
        """Genera descripción para YouTube"""
        # Resumen corto del contenido
        summary = content.overview[:100] + "..." if len(content.overview) > 100 else content.overview
        
        description = f"""
🎬 ANÁLISIS COMPLETO: {content.title}

{summary}

⭐ RATING: {content.rating}/10
🎭 GÉNEROS: {', '.join(content.genres)}
📅 ESTRENO: {content.release_date}

{script_text[:200]}...

🔔 ¡SUSCRÍBETE para más análisis cinematográficos!
👍 ¡DALE LIKE si te gustó el video!
💬 ¡COMENTA tu opinión sobre {content.title}!

{', '.join(self._generate_hashtags(content))}

---
Cine Norte - Tu canal de análisis cinematográfico
"""
        
        return description
    
    def _generate_thumbnail_prompts(self, content: ContentItem) -> List[str]:
        """Genera prompts para crear miniaturas atractivas"""
        prompts = []
        
        # Prompt principal
        main_prompt = f"""
Cinematic thumbnail for {content.title} movie review:
- {content.title} text in bold red letters
- Dark cinematic background with {content.genres[0] if content.genres else 'dramatic'} atmosphere
- Professional movie poster style
- Cine Norte logo visible
- High contrast, eye-catching design
- {content.rating}/10 rating displayed
"""
        prompts.append(main_prompt)
        
        # Prompts alternativos
        if content.content_type == "movie":
            prompts.append(f"Movie poster style thumbnail: {content.title} with explosive action elements")
            prompts.append(f"Dramatic close-up style: {content.title} with intense lighting")
        else:
            prompts.append(f"TV series style thumbnail: {content.title} with character portraits")
            prompts.append(f"Season poster style: {content.title} with ensemble cast")
        
        return prompts
    
    def _generate_fallback_script(self, content: ContentItem) -> str:
        """Genera un guion básico sin IA como respaldo"""
        script = f"""
¡Hola cinéfilos! Soy Cine Norte y hoy les traigo un análisis de {content.title}.

{content.overview}

Esta {'película' if content.content_type == 'movie' else 'serie'} de {', '.join(content.genres[:2])} 
nos presenta una historia que mantiene al espectador en vilo desde el primer momento.

Los aspectos técnicos están muy bien logrados, con una dirección sólida y actuaciones convincentes. 
La cinematografía captura perfectamente la atmósfera que la historia requiere.

En general, {content.title} es una {'película' if content.content_type == 'movie' else 'serie'} 
que vale la pena ver, especialmente si eres fan del género {content.genres[0] if content.genres else 'drama'}.

¿Qué opinas de {content.title}? Déjamelo en los comentarios y no olvides suscribirte para más análisis cinematográficos.
"""
        return script
    
    def _create_fallback_script(self, content: ContentItem) -> GeneratedScript:
        """Crea un guion de respaldo en caso de error"""
        script_text = self._generate_fallback_script(content)
        segments = self._create_script_segments(script_text, content)
        
        return GeneratedScript(
            title=f"Análisis de {content.title} - Cine Norte",
            content=content,
            segments=segments,
            total_duration=sum(segment.end_time - segment.start_time for segment in segments),
            hashtags=self._generate_hashtags(content),
            description=self._generate_description(content, script_text),
            thumbnail_prompts=self._generate_thumbnail_prompts(content),
            raw_text=script_text
        )
    
    def save_script_to_file(self, script: GeneratedScript, filename: str = None) -> str:
        """Guarda el guion en un archivo de texto"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"guion_{script.content.title.replace(' ', '_')}_{timestamp}.txt"
        
        filepath = f"output/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"GUION: {script.title}\n")
            f.write("=" * 50 + "\n\n")
            f.write(script.raw_text)
            f.write("\n\n" + "=" * 50 + "\n")
            f.write("HASHTAGS:\n")
            f.write(", ".join(script.hashtags))
            f.write("\n\nDESCRIPCIÓN:\n")
            f.write(script.description)
        
        return filepath
