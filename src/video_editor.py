"""
Editor audiovisual con branding Cine Norte
"""

import os
import tempfile
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path
import numpy as np

# Video processing
import cv2
from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip, 
    TextClip, ImageClip, ColorClip, concatenate_videoclips
)
from moviepy.video.fx import resize, crop, fadein, fadeout
from moviepy.audio.fx import volumex

# Image processing
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns

from config import BRANDING, VIDEO_CONFIG, CONTENT_CONFIG
from src.script_generator import GeneratedScript, ScriptSegment

logger = logging.getLogger(__name__)

@dataclass
class VideoElement:
    """Elemento visual del video"""
    type: str  # 'text', 'image', 'video', 'overlay'
    content: str
    start_time: float
    end_time: float
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (100, 100)
    style: Dict = None

@dataclass
class VideoProject:
    """Proyecto de video completo"""
    title: str
    script: GeneratedScript
    elements: List[VideoElement]
    background_music: str
    intro_clip: str
    outro_clip: str
    duration: float

class VideoEditor:
    """Editor audiovisual con branding Cine Norte"""
    
    def __init__(self):
        self.branding = BRANDING
        self.video_config = VIDEO_CONFIG
        self.temp_dir = Path("temp/video")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Crear assets de branding
        self._create_branding_assets()
    
    def _create_branding_assets(self):
        """Crea assets visuales del branding Cine Norte"""
        try:
            # Crear logo Cine Norte
            self._create_logo()
            
            # Crear intro animado
            self._create_intro_animation()
            
            # Crear outro
            self._create_outro_animation()
            
            logger.info("Assets de branding creados exitosamente")
            
        except Exception as e:
            logger.error(f"Error creando assets de branding: {e}")
    
    def _create_logo(self):
        """Crea el logo de Cine Norte"""
        try:
            # Dimensiones del logo
            width, height = 400, 200
            
            # Crear imagen base
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Cargar fuente (usar fuente por defecto si no hay disponible)
            try:
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Dibujar fondo con gradiente
            self._draw_gradient_background(draw, width, height)
            
            # Dibujar texto "CINE NORTE"
            text = "CINE NORTE"
            bbox = draw.textbbox((0, 0), text, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2 - 20
            
            # Sombra del texto
            draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 180), font=font_large)
            
            # Texto principal
            draw.text((x, y), text, fill=self._hex_to_rgb(self.branding["colors"]["primary"]), font=font_large)
            
            # Línea decorativa
            line_y = y + text_height + 10
            draw.rectangle([x - 10, line_y, x + text_width + 10, line_y + 3], 
                         fill=self._hex_to_rgb(self.branding["colors"]["accent"]))
            
            # Guardar logo
            logo_path = self.temp_dir / "cine_norte_logo.png"
            img.save(logo_path, "PNG")
            
            self.logo_path = str(logo_path)
            
        except Exception as e:
            logger.error(f"Error creando logo: {e}")
            self.logo_path = None
    
    def _draw_gradient_background(self, draw, width, height):
        """Dibuja un fondo con gradiente"""
        for y in range(height):
            # Gradiente de negro a rojo oscuro
            ratio = y / height
            r = int(10 + (229 * ratio * 0.3))
            g = int(10 + (9 * ratio * 0.3))
            b = int(10 + (20 * ratio * 0.3))
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    def _hex_to_rgb(self, hex_color):
        """Convierte color hex a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _create_intro_animation(self):
        """Crea la animación de intro"""
        try:
            # Crear frames para la animación
            frames = []
            duration = CONTENT_CONFIG["intro_duration"]
            fps = self.video_config["fps"]
            total_frames = int(duration * fps)
            
            for frame_num in range(total_frames):
                # Crear frame base
                width, height = 1920, 1080
                img = Image.new('RGB', (width, height), self._hex_to_rgb(self.branding["colors"]["secondary"]))
                draw = ImageDraw.Draw(img)
                
                # Efecto de luces tipo reflector
                progress = frame_num / total_frames
                
                # Dibujar luces circulares
                for i in range(3):
                    light_x = width // 4 + (width // 2) * i
                    light_y = height // 2
                    light_radius = int(200 * (1 + 0.5 * np.sin(progress * 4 * np.pi + i)))
                    
                    # Crear gradiente radial para la luz
                    for r in range(light_radius, 0, -5):
                        alpha = int(255 * (1 - r / light_radius) * (1 - progress * 0.5))
                        color = (*self._hex_to_rgb(self.branding["colors"]["primary"]), alpha)
                        
                        # Simular gradiente con círculos concéntricos
                        draw.ellipse([light_x - r, light_y - r, light_x + r, light_y + r], 
                                   fill=color[:3])
                
                # Agregar logo al final
                if progress > 0.7:
                    if self.logo_path and os.path.exists(self.logo_path):
                        logo = Image.open(self.logo_path)
                        logo = logo.resize((400, 200))
                        
                        # Posición centrada
                        logo_x = (width - 400) // 2
                        logo_y = (height - 200) // 2
                        
                        # Efecto de aparición
                        alpha = int(255 * ((progress - 0.7) / 0.3))
                        logo.putalpha(alpha)
                        
                        img.paste(logo, (logo_x, logo_y), logo)
                
                frames.append(img)
            
            # Guardar como GIF o crear video
            intro_path = self.temp_dir / "intro_animation.gif"
            frames[0].save(intro_path, save_all=True, append_images=frames[1:], 
                          duration=int(1000/fps), loop=0)
            
            self.intro_path = str(intro_path)
            
        except Exception as e:
            logger.error(f"Error creando intro: {e}")
            self.intro_path = None
    
    def _create_outro_animation(self):
        """Crea la animación de outro"""
        try:
            # Crear outro simple con logo y call-to-action
            width, height = 1920, 1080
            img = Image.new('RGB', (width, height), self._hex_to_rgb(self.branding["colors"]["secondary"]))
            draw = ImageDraw.Draw(img)
            
            # Cargar fuente
            try:
                font_large = ImageFont.truetype("arial.ttf", 72)
                font_medium = ImageFont.truetype("arial.ttf", 48)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
            
            # Texto principal
            text = "¡SUSCRÍBETE!"
            bbox = draw.textbbox((0, 0), text, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 2 - 100
            
            draw.text((x, y), text, fill=self._hex_to_rgb(self.branding["colors"]["primary"]), font=font_large)
            
            # Texto secundario
            subtext = "Para más análisis cinematográficos"
            bbox = draw.textbbox((0, 0), subtext, font=font_medium)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y += 100
            
            draw.text((x, y), subtext, fill=self._hex_to_rgb(self.branding["colors"]["accent"]), font=font_medium)
            
            # Agregar logo
            if self.logo_path and os.path.exists(self.logo_path):
                logo = Image.open(self.logo_path)
                logo = logo.resize((300, 150))
                logo_x = (width - 300) // 2
                logo_y = y + 80
                img.paste(logo, (logo_x, logo_y), logo)
            
            outro_path = self.temp_dir / "outro_frame.png"
            img.save(outro_path, "PNG")
            
            self.outro_path = str(outro_path)
            
        except Exception as e:
            logger.error(f"Error creando outro: {e}")
            self.outro_path = None
    
    def create_video_project(self, script: GeneratedScript) -> VideoProject:
        """Crea un proyecto de video completo"""
        try:
            # Crear elementos visuales basados en el guion
            elements = self._create_visual_elements(script)
            
            # Seleccionar música de fondo
            background_music = self._select_background_music(script)
            
            # Crear proyecto
            project = VideoProject(
                title=script.title,
                script=script,
                elements=elements,
                background_music=background_music,
                intro_clip=self.intro_path,
                outro_clip=self.outro_path,
                duration=script.total_duration
            )
            
            return project
            
        except Exception as e:
            logger.error(f"Error creando proyecto de video: {e}")
            return None
    
    def _create_visual_elements(self, script: GeneratedScript) -> List[VideoElement]:
        """Crea elementos visuales para el video"""
        elements = []
        
        for i, segment in enumerate(script.segments):
            # Crear elemento de texto principal
            text_element = VideoElement(
                type="text",
                content=segment.text,
                start_time=segment.start_time,
                end_time=segment.end_time,
                position=(100, 100),
                size=(800, 200),
                style={
                    "font_size": 48,
                    "color": self.branding["colors"]["accent"],
                    "background": self.branding["colors"]["primary"],
                    "animation": "fade_in_out"
                }
            )
            elements.append(text_element)
            
            # Agregar elementos visuales específicos
            for cue in segment.visual_cues:
                if cue == "poster_película" and script.content.poster_url:
                    poster_element = VideoElement(
                        type="image",
                        content=script.content.poster_url,
                        start_time=segment.start_time,
                        end_time=segment.end_time,
                        position=(1200, 100),
                        size=(300, 450)
                    )
                    elements.append(poster_element)
                
                elif cue == "efecto_revelador":
                    effect_element = VideoElement(
                        type="overlay",
                        content="light_reveal",
                        start_time=segment.start_time,
                        end_time=segment.start_time + 1.0,
                        position=(0, 0),
                        size=(1920, 1080)
                    )
                    elements.append(effect_element)
        
        return elements
    
    def _select_background_music(self, script: GeneratedScript) -> str:
        """Selecciona música de fondo apropiada"""
        # Por ahora retorna una ruta de música de ejemplo
        # En una implementación real, esto seleccionaría de una librería de música
        return "assets/music/cinematic_background.mp3"
    
    def render_video(self, project: VideoProject, output_path: str, format_type: str = "youtube") -> str:
        """
        Renderiza el video final
        
        Args:
            project: Proyecto de video
            output_path: Ruta de salida
            format_type: 'youtube', 'tiktok', 'instagram'
        """
        try:
            # Obtener configuración de formato
            format_config = self.video_config["formats"][format_type]
            
            # Crear clips de video
            clips = []
            
            # Intro
            if project.intro_clip and os.path.exists(project.intro_clip):
                intro_clip = self._create_intro_clip(project.intro_clip, format_config)
                clips.append(intro_clip)
            
            # Contenido principal
            main_clip = self._create_main_content_clip(project, format_config)
            clips.append(main_clip)
            
            # Outro
            if project.outro_clip and os.path.exists(project.outro_clip):
                outro_clip = self._create_outro_clip(project.outro_clip, format_config)
                clips.append(outro_clip)
            
            # Combinar clips
            final_video = concatenate_videoclips(clips)
            
            # Ajustar formato final
            final_video = self._adjust_video_format(final_video, format_config)
            
            # Renderizar
            final_video.write_videofile(
                output_path,
                fps=self.video_config["fps"],
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            logger.info(f"Video renderizado exitosamente: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error renderizando video: {e}")
            return ""
    
    def _create_intro_clip(self, intro_path: str, format_config: Dict) -> VideoFileClip:
        """Crea clip de intro"""
        try:
            # Por ahora crear un clip de color sólido
            duration = CONTENT_CONFIG["intro_duration"]
            clip = ColorClip(
                size=(format_config["width"], format_config["height"]),
                color=self._hex_to_rgb(self.branding["colors"]["secondary"]),
                duration=duration
            )
            
            # Agregar texto de intro
            intro_text = TextClip(
                "CINE NORTE",
                fontsize=72,
                color=self.branding["colors"]["primary"],
                font='Arial-Bold'
            ).set_position('center').set_duration(duration)
            
            return CompositeVideoClip([clip, intro_text])
            
        except Exception as e:
            logger.error(f"Error creando intro: {e}")
            return ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=3)
    
    def _create_main_content_clip(self, project: VideoProject, format_config: Dict) -> VideoFileClip:
        """Crea el clip de contenido principal"""
        try:
            # Crear clip base
            duration = project.duration
            base_clip = ColorClip(
                size=(format_config["width"], format_config["height"]),
                color=self._hex_to_rgb(self.branding["colors"]["secondary"]),
                duration=duration
            )
            
            # Agregar elementos visuales
            visual_clips = [base_clip]
            
            for element in project.elements:
                if element.type == "text":
                    text_clip = self._create_text_clip(element, format_config)
                    visual_clips.append(text_clip)
                elif element.type == "image":
                    image_clip = self._create_image_clip(element, format_config)
                    visual_clips.append(image_clip)
            
            return CompositeVideoClip(visual_clips)
            
        except Exception as e:
            logger.error(f"Error creando contenido principal: {e}")
            return ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=10)
    
    def _create_text_clip(self, element: VideoElement, format_config: Dict) -> TextClip:
        """Crea clip de texto"""
        try:
            clip = TextClip(
                element.content,
                fontsize=element.style.get("font_size", 48),
                color=element.style.get("color", "#FFFFFF"),
                font='Arial-Bold',
                method='caption',
                size=(element.size[0], element.size[1])
            ).set_position(element.position).set_start(element.start_time).set_end(element.end_time)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando clip de texto: {e}")
            return TextClip("", fontsize=48, color="white").set_duration(1)
    
    def _create_image_clip(self, element: VideoElement, format_config: Dict) -> ImageClip:
        """Crea clip de imagen"""
        try:
            # Descargar imagen si es URL
            if element.content.startswith("http"):
                # Implementar descarga de imagen
                pass
            
            clip = ImageClip(element.content).resize(element.size).set_position(element.position).set_start(element.start_time).set_end(element.end_time)
            return clip
            
        except Exception as e:
            logger.error(f"Error creando clip de imagen: {e}")
            return ImageClip("assets/placeholder.png").set_duration(1)
    
    def _create_outro_clip(self, outro_path: str, format_config: Dict) -> VideoFileClip:
        """Crea clip de outro"""
        try:
            duration = CONTENT_CONFIG["outro_duration"]
            clip = ColorClip(
                size=(format_config["width"], format_config["height"]),
                color=self._hex_to_rgb(self.branding["colors"]["secondary"]),
                duration=duration
            )
            
            # Agregar texto de outro
            outro_text = TextClip(
                "¡SUSCRÍBETE!",
                fontsize=72,
                color=self.branding["colors"]["primary"],
                font='Arial-Bold'
            ).set_position('center').set_duration(duration)
            
            return CompositeVideoClip([clip, outro_text])
            
        except Exception as e:
            logger.error(f"Error creando outro: {e}")
            return ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=3)
    
    def _adjust_video_format(self, video_clip, format_config: Dict) -> VideoFileClip:
        """Ajusta el video al formato específico"""
        try:
            target_width = format_config["width"]
            target_height = format_config["height"]
            
            # Redimensionar manteniendo aspecto
            video_clip = video_clip.resize((target_width, target_height))
            
            return video_clip
            
        except Exception as e:
            logger.error(f"Error ajustando formato: {e}")
            return video_clip
