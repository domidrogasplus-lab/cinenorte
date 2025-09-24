"""
Editor audiovisual con branding Cine Norte
Crea videos profesionales con identidad visual consistente
"""
import os
import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import tempfile
import json
from datetime import datetime
import math

# Importaciones para edición de video
try:
    from moviepy.editor import *
    from moviepy.video.fx import resize, crop, fadein, fadeout
    from moviepy.video.tools.drawing import color_gradient
    from moviepy.audio.fx import volumex, audio_fadein, audio_fadeout
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import cv2
except ImportError:
    print("Instalando dependencias de video...")
    os.system("pip install moviepy pillow opencv-python numpy")

from config import config
from script_generator import GeneratedScript, ScriptSection
from voice_synthesizer import SubtitleCue

@dataclass
class VideoElement:
    """Elemento de video (clip, texto, imagen, etc.)"""
    type: str  # 'video', 'image', 'text', 'audio', 'effect'
    content: str  # Ruta del archivo o texto
    start_time: float
    end_time: float
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (1920, 1080)
    opacity: float = 1.0
    effects: List[str] = None

@dataclass
class VideoStyle:
    """Estilo visual del video"""
    background_color: str
    primary_color: str
    secondary_color: str
    font_family: str
    font_size: int
    transition_style: str
    animation_style: str

class CineNorteVideoEditor:
    """Editor de video con branding Cine Norte"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp()
        
        # Estilos predefinidos
        self.styles = {
            "cinematic": VideoStyle(
                background_color="#0A0A0A",
                primary_color="#E50914", 
                secondary_color="#C0C0C0",
                font_family="Arial Black",
                font_size=48,
                transition_style="fade",
                animation_style="smooth"
            ),
            "dynamic": VideoStyle(
                background_color="#000000",
                primary_color="#E50914",
                secondary_color="#FFFFFF", 
                font_family="Impact",
                font_size=52,
                transition_style="slide",
                animation_style="bounce"
            ),
            "dramatic": VideoStyle(
                background_color="#1A1A1A",
                primary_color="#E50914",
                secondary_color="#808080",
                font_family="Times New Roman",
                font_size=44,
                transition_style="dissolve",
                animation_style="elegant"
            )
        }
        
        self.current_style = self.styles["cinematic"]
        
    def create_video(self, script: GeneratedScript, audio_path: str, 
                    subtitles: List[SubtitleCue], format_type: str = "youtube",
                    style: str = "cinematic") -> str:
        """
        Crea un video completo con branding Cine Norte
        
        Args:
            script: Guion generado
            audio_path: Ruta del archivo de audio
            subtitles: Lista de subtítulos
            format_type: Formato de salida (youtube, tiktok, instagram)
            style: Estilo visual (cinematic, dynamic, dramatic)
            
        Returns:
            Ruta del video final generado
        """
        try:
            # Configurar estilo
            if style in self.styles:
                self.current_style = self.styles[style]
            
            # Obtener dimensiones según formato
            width, height = config.FORMATS.get(format_type, (1920, 1080))
            
            # Crear elementos del video
            video_elements = self._create_video_elements(script, audio_path, subtitles, width, height)
            
            # Crear clips de video
            video_clips = self._create_video_clips(video_elements, width, height)
            
            # Combinar clips
            final_video = self._combine_video_clips(video_clips, audio_path, width, height)
            
            # Aplicar efectos finales
            final_video = self._apply_final_effects(final_video, format_type)
            
            # Exportar video
            output_path = self._export_video(final_video, script.title, format_type)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creando video: {e}")
            return None
    
    def _create_video_elements(self, script: GeneratedScript, audio_path: str,
                              subtitles: List[SubtitleCue], width: int, height: int) -> List[VideoElement]:
        """Crea elementos visuales del video"""
        elements = []
        
        # Crear intro con logo Cine Norte
        intro_element = self._create_intro_element(script, width, height)
        if intro_element:
            elements.append(intro_element)
        
        # Crear elementos para cada sección del guion
        for i, section in enumerate(script.sections):
            section_elements = self._create_section_elements(section, i, width, height)
            elements.extend(section_elements)
        
        # Crear outro
        outro_element = self._create_outro_element(script, width, height)
        if outro_element:
            elements.append(outro_element)
        
        # Agregar subtítulos como elementos de texto
        subtitle_elements = self._create_subtitle_elements(subtitles, width, height)
        elements.extend(subtitle_elements)
        
        return elements
    
    def _create_intro_element(self, script: GeneratedScript, width: int, height: int) -> VideoElement:
        """Crea elemento de introducción con logo"""
        try:
            # Crear logo animado
            logo_path = self._create_animated_logo("CINE NORTE", width, height)
            
            return VideoElement(
                type="video",
                content=logo_path,
                start_time=0.0,
                end_time=5.0,
                position=(0, 0),
                size=(width, height),
                effects=["fade_in", "zoom_in"]
            )
        except Exception as e:
            self.logger.error(f"Error creando intro: {e}")
            return None
    
    def _create_section_elements(self, section: ScriptSection, section_index: int,
                                width: int, height: int) -> List[VideoElement]:
        """Crea elementos visuales para una sección del guion"""
        elements = []
        
        # Crear fondo dinámico
        background_element = self._create_background_element(section, width, height)
        if background_element:
            elements.append(background_element)
        
        # Crear título de sección
        title_element = self._create_section_title(section, section_index, width, height)
        if title_element:
            elements.append(title_element)
        
        # Crear elementos visuales específicos por tipo de sección
        if section.type == "hook":
            hook_elements = self._create_hook_elements(section, width, height)
            elements.extend(hook_elements)
        elif section.type == "plot":
            plot_elements = self._create_plot_elements(section, width, height)
            elements.extend(plot_elements)
        elif section.type == "analysis":
            analysis_elements = self._create_analysis_elements(section, width, height)
            elements.extend(analysis_elements)
        
        return elements
    
    def _create_background_element(self, section: ScriptSection, width: int, height: int) -> VideoElement:
        """Crea elemento de fondo dinámico"""
        try:
            # Crear gradiente de fondo
            background_path = self._create_gradient_background(width, height, section.emotion)
            
            return VideoElement(
                type="video",
                content=background_path,
                start_time=0.0,
                end_time=section.duration_seconds,
                position=(0, 0),
                size=(width, height),
                opacity=0.8
            )
        except Exception as e:
            self.logger.error(f"Error creando fondo: {e}")
            return None
    
    def _create_section_title(self, section: ScriptSection, section_index: int,
                             width: int, height: int) -> VideoElement:
        """Crea título de sección"""
        try:
            # Crear texto animado
            title_text = self._get_section_title_text(section.type)
            title_path = self._create_animated_text(
                title_text, 
                width, 
                height,
                self.current_style.primary_color,
                position="top"
            )
            
            return VideoElement(
                type="video",
                content=title_path,
                start_time=0.0,
                end_time=3.0,
                position=(0, 0),
                size=(width, height),
                effects=["slide_in_top", "fade_out"]
            )
        except Exception as e:
            self.logger.error(f"Error creando título de sección: {e}")
            return None
    
    def _create_hook_elements(self, section: ScriptSection, width: int, height: int) -> List[VideoElement]:
        """Crea elementos visuales para sección hook"""
        elements = []
        
        # Crear texto de impacto
        impact_text = self._extract_impact_phrases(section.content)
        for i, phrase in enumerate(impact_text[:3]):  # Máximo 3 frases
            text_element = self._create_animated_text(
                phrase,
                width,
                height,
                self.current_style.secondary_color,
                position="center",
                animation="zoom_pulse"
            )
            
            elements.append(VideoElement(
                type="video",
                content=text_element,
                start_time=i * 2.0,
                end_time=(i * 2.0) + 2.0,
                position=(0, 0),
                size=(width, height),
                effects=["zoom_pulse", "fade_in_out"]
            ))
        
        return elements
    
    def _create_plot_elements(self, section: ScriptSection, width: int, height: int) -> List[VideoElement]:
        """Crea elementos visuales para sección plot"""
        elements = []
        
        # Crear montaje de imágenes relacionadas
        # (En implementación real, se descargarían imágenes del contenido)
        montage_path = self._create_content_montage(section, width, height)
        
        if montage_path:
            elements.append(VideoElement(
                type="video",
                content=montage_path,
                start_time=0.0,
                end_time=section.duration_seconds,
                position=(0, 0),
                size=(width, height),
                opacity=0.6
            ))
        
        return elements
    
    def _create_analysis_elements(self, section: ScriptSection, width: int, height: int) -> List[VideoElement]:
        """Crea elementos visuales para sección análisis"""
        elements = []
        
        # Crear gráficos informativos
        info_graphics = self._create_info_graphics(section, width, height)
        elements.extend(info_graphics)
        
        return elements
    
    def _create_outro_element(self, script: GeneratedScript, width: int, height: int) -> VideoElement:
        """Crea elemento de cierre"""
        try:
            outro_path = self._create_outro_sequence(script, width, height)
            
            return VideoElement(
                type="video",
                content=outro_path,
                start_time=0.0,
                end_time=5.0,
                position=(0, 0),
                size=(width, height),
                effects=["fade_out", "zoom_out"]
            )
        except Exception as e:
            self.logger.error(f"Error creando outro: {e}")
            return None
    
    def _create_subtitle_elements(self, subtitles: List[SubtitleCue], width: int, height: int) -> List[VideoElement]:
        """Crea elementos de subtítulos"""
        elements = []
        
        for subtitle in subtitles:
            # Convertir tiempo a segundos
            start_seconds = self._time_to_seconds(subtitle.start_time)
            end_seconds = self._time_to_seconds(subtitle.end_time)
            
            # Crear subtítulo visual
            subtitle_path = self._create_subtitle_visual(subtitle.text, width, height)
            
            elements.append(VideoElement(
                type="video",
                content=subtitle_path,
                start_time=start_seconds,
                end_time=end_seconds,
                position=(0, int(height * 0.8)),  # Posición inferior
                size=(width, int(height * 0.2)),
                opacity=0.9
            ))
        
        return elements
    
    def _create_animated_logo(self, text: str, width: int, height: int) -> str:
        """Crea logo animado de Cine Norte"""
        try:
            # Crear imagen base
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Configurar fuente
            font_size = min(width, height) // 8
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Obtener dimensiones del texto
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Posición centrada
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Dibujar texto con efecto de gradiente
            self._draw_gradient_text(draw, text, (x, y), font, 
                                   self.current_style.primary_color, 
                                   self.current_style.secondary_color)
            
            # Agregar efectos de luz
            self._add_light_effects(img, width, height)
            
            # Guardar imagen
            logo_path = os.path.join(self.temp_dir, "logo.png")
            img.save(logo_path)
            
            # Crear video animado del logo
            return self._create_logo_animation(logo_path, width, height)
            
        except Exception as e:
            self.logger.error(f"Error creando logo animado: {e}")
            return None
    
    def _create_gradient_background(self, width: int, height: int, emotion: str) -> str:
        """Crea fondo con gradiente según emoción"""
        try:
            # Colores según emoción
            color_schemes = {
                "excitement": [("#E50914", "#FF6B6B"), ("#0A0A0A", "#1A1A1A")],
                "suspense": [("#1A1A1A", "#2A2A2A"), ("#E50914", "#8B0000")],
                "drama": [("#2A2A2A", "#3A3A3A"), ("#C0C0C0", "#808080")],
                "neutral": [("#0A0A0A", "#1A1A1A"), ("#E50914", "#C0C0C0")]
            }
            
            colors = color_schemes.get(emotion, color_schemes["neutral"])
            
            # Crear gradiente
            gradient = color_gradient(
                (width, height),
                colors[0],
                colors[1],
                p1=(0, 0),
                p2=(width, height)
            )
            
            # Guardar como video
            background_path = os.path.join(self.temp_dir, f"background_{emotion}.mp4")
            gradient.write_videofile(background_path, fps=24, duration=1)
            
            return background_path
            
        except Exception as e:
            self.logger.error(f"Error creando fondo gradiente: {e}")
            return None
    
    def _create_animated_text(self, text: str, width: int, height: int, 
                            color: str, position: str = "center",
                            animation: str = "fade_in") -> str:
        """Crea texto animado"""
        try:
            # Crear clip de texto
            txt_clip = TextClip(
                text,
                fontsize=min(width, height) // 20,
                color=color,
                font='Arial-Bold'
            ).set_duration(3)
            
            # Posicionar texto
            if position == "center":
                txt_clip = txt_clip.set_position('center')
            elif position == "top":
                txt_clip = txt_clip.set_position(('center', height // 4))
            elif position == "bottom":
                txt_clip = txt_clip.set_position(('center', height * 3 // 4))
            
            # Aplicar animación
            if animation == "zoom_pulse":
                txt_clip = txt_clip.resize(lambda t: 1 + 0.1 * np.sin(t * 2))
            elif animation == "slide_in_top":
                txt_clip = txt_clip.set_position(lambda t: ('center', -height + t * height // 3))
            
            # Crear composición
            composition = CompositeVideoClip([txt_clip], size=(width, height))
            
            # Guardar video
            text_path = os.path.join(self.temp_dir, f"text_{hash(text)}.mp4")
            composition.write_videofile(text_path, fps=24)
            
            return text_path
            
        except Exception as e:
            self.logger.error(f"Error creando texto animado: {e}")
            return None
    
    def _create_video_clips(self, elements: List[VideoElement], width: int, height: int) -> List[VideoClip]:
        """Convierte elementos en clips de video"""
        clips = []
        
        for element in elements:
            try:
                if element.type == "video":
                    clip = VideoFileClip(element.content)
                elif element.type == "image":
                    clip = ImageClip(element.content)
                elif element.type == "text":
                    clip = TextClip(element.content, fontsize=24, color='white')
                else:
                    continue
                
                # Ajustar duración
                clip = clip.set_duration(element.end_time - element.start_time)
                
                # Ajustar posición y tamaño
                clip = clip.set_position(element.position).resize(element.size)
                
                # Aplicar opacidad
                if element.opacity < 1.0:
                    clip = clip.set_opacity(element.opacity)
                
                # Aplicar efectos
                if element.effects:
                    clip = self._apply_effects(clip, element.effects)
                
                clips.append(clip)
                
            except Exception as e:
                self.logger.error(f"Error creando clip: {e}")
                continue
        
        return clips
    
    def _combine_video_clips(self, clips: List[VideoClip], audio_path: str, 
                            width: int, height: int) -> VideoClip:
        """Combina todos los clips en un video final"""
        try:
            if not clips:
                # Crear clip vacío si no hay clips
                final_video = ColorClip(size=(width, height), color=(0, 0, 0), duration=1)
            else:
                # Combinar clips
                final_video = CompositeVideoClip(clips, size=(width, height))
            
            # Agregar audio
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                final_video = final_video.set_audio(audio_clip)
            
            return final_video
            
        except Exception as e:
            self.logger.error(f"Error combinando clips: {e}")
            return None
    
    def _apply_final_effects(self, video: VideoClip, format_type: str) -> VideoClip:
        """Aplica efectos finales al video"""
        try:
            # Fade in/out
            video = video.fadein(1).fadeout(1)
            
            # Ajustar para formato específico
            if format_type == "tiktok":
                # Optimizar para TikTok (vertical)
                video = video.resize(height=1920).crop(x_center=video.w//2, width=1080)
            elif format_type == "instagram":
                # Optimizar para Instagram (cuadrado)
                min_dim = min(video.w, video.h)
                video = video.resize(height=min_dim).crop(x_center=video.w//2, width=min_dim)
            
            return video
            
        except Exception as e:
            self.logger.error(f"Error aplicando efectos finales: {e}")
            return video
    
    def _export_video(self, video: VideoClip, title: str, format_type: str) -> str:
        """Exporta el video final"""
        try:
            # Crear nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cine_norte_{title.replace(' ', '_')}_{format_type}_{timestamp}.mp4"
            output_path = os.path.join(self.temp_dir, filename)
            
            # Configuración de exportación
            codec = 'libx264'
            audio_codec = 'aac'
            temp_audiofile = 'temp-audio.m4a'
            
            # Exportar video
            video.write_videofile(
                output_path,
                codec=codec,
                audio_codec=audio_codec,
                temp_audiofile=temp_audiofile,
                remove_temp=True,
                fps=24,
                bitrate="5000k"
            )
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error exportando video: {e}")
            return None
    
    # Métodos auxiliares
    def _get_section_title_text(self, section_type: str) -> str:
        """Obtiene texto del título según tipo de sección"""
        titles = {
            "intro": "CINE NORTE",
            "hook": "¡ATENCIÓN!",
            "plot": "LA HISTORIA",
            "analysis": "ANÁLISIS",
            "outro": "¡SUSCRÍBETE!"
        }
        return titles.get(section_type, section_type.upper())
    
    def _extract_impact_phrases(self, text: str) -> List[str]:
        """Extrae frases de impacto del texto"""
        # Buscar frases con signos de exclamación o palabras clave
        import re
        phrases = re.findall(r'[^.!?]*[!¡][^.!?]*', text)
        if not phrases:
            # Si no hay exclamaciones, tomar primeras oraciones
            sentences = re.split(r'[.!?]+', text)
            phrases = [s.strip() for s in sentences[:3] if s.strip()]
        return phrases[:3]
    
    def _time_to_seconds(self, time_str: str) -> float:
        """Convierte tiempo en formato HH:MM:SS.mmm a segundos"""
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except:
            return 0.0
    
    def _apply_effects(self, clip: VideoClip, effects: List[str]) -> VideoClip:
        """Aplica efectos a un clip"""
        for effect in effects:
            if effect == "fade_in":
                clip = clip.fadein(0.5)
            elif effect == "fade_out":
                clip = clip.fadeout(0.5)
            elif effect == "zoom_in":
                clip = clip.resize(lambda t: 1 + 0.1 * t)
            elif effect == "zoom_out":
                clip = clip.resize(lambda t: 1.1 - 0.1 * t)
        
        return clip
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.error(f"Error limpiando archivos temporales: {e}")

# Instancia global del editor
video_editor = CineNorteVideoEditor()
