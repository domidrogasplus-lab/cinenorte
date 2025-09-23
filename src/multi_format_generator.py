"""
Generador de videos en múltiples formatos para diferentes plataformas
"""

import os
import tempfile
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path

# Video processing
import cv2
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, TextClip
from moviepy.video.fx import resize, crop
from PIL import Image, ImageDraw, ImageFont

from config import VIDEO_CONFIG, BRANDING
from src.video_editor import VideoProject

logger = logging.getLogger(__name__)

@dataclass
class FormatSpecs:
    """Especificaciones de formato de video"""
    name: str
    width: int
    height: int
    ratio: str
    platform: str
    orientation: str  # 'landscape', 'portrait', 'square'
    safe_areas: Dict[str, int]  # Áreas seguras para texto

class MultiFormatGenerator:
    """Generador de videos en múltiples formatos"""
    
    def __init__(self):
        self.formats = self._initialize_formats()
        self.temp_dir = Path("temp/formats")
        self.temp_dir.mkdir(exist_ok=True)
    
    def _initialize_formats(self) -> Dict[str, FormatSpecs]:
        """Inicializa las especificaciones de formatos"""
        return {
            "youtube": FormatSpecs(
                name="YouTube",
                width=1920,
                height=1080,
                ratio="16:9",
                platform="YouTube",
                orientation="landscape",
                safe_areas={"top": 100, "bottom": 100, "left": 100, "right": 100}
            ),
            "tiktok": FormatSpecs(
                name="TikTok",
                width=1080,
                height=1920,
                ratio="9:16",
                platform="TikTok",
                orientation="portrait",
                safe_areas={"top": 200, "bottom": 200, "left": 50, "right": 50}
            ),
            "instagram_reel": FormatSpecs(
                name="Instagram Reel",
                width=1080,
                height=1920,
                ratio="9:16",
                platform="Instagram",
                orientation="portrait",
                safe_areas={"top": 200, "bottom": 200, "left": 50, "right": 50}
            ),
            "instagram_post": FormatSpecs(
                name="Instagram Post",
                width=1080,
                height=1080,
                ratio="1:1",
                platform="Instagram",
                orientation="square",
                safe_areas={"top": 100, "bottom": 100, "left": 100, "right": 100}
            ),
            "facebook": FormatSpecs(
                name="Facebook",
                width=1920,
                height=1080,
                ratio="16:9",
                platform="Facebook",
                orientation="landscape",
                safe_areas={"top": 100, "bottom": 100, "left": 100, "right": 100}
            ),
            "twitter": FormatSpecs(
                name="Twitter",
                width=1280,
                height=720,
                ratio="16:9",
                platform="Twitter",
                orientation="landscape",
                safe_areas={"top": 80, "bottom": 80, "left": 80, "right": 80}
            )
        }
    
    def generate_all_formats(self, project: VideoProject, base_output_dir: str = "output") -> Dict[str, str]:
        """
        Genera videos en todos los formatos disponibles
        
        Args:
            project: Proyecto de video base
            base_output_dir: Directorio base de salida
            
        Returns:
            Diccionario con rutas de archivos generados por formato
        """
        output_paths = {}
        base_dir = Path(base_output_dir)
        base_dir.mkdir(exist_ok=True)
        
        # Crear subdirectorios por formato
        for format_name in self.formats.keys():
            format_dir = base_dir / format_name
            format_dir.mkdir(exist_ok=True)
        
        # Generar cada formato
        for format_name, format_specs in self.formats.items():
            try:
                output_path = self.generate_format(project, format_name, base_output_dir)
                if output_path:
                    output_paths[format_name] = output_path
                    logger.info(f"Formato {format_name} generado: {output_path}")
                else:
                    logger.error(f"Error generando formato {format_name}")
                    
            except Exception as e:
                logger.error(f"Error generando formato {format_name}: {e}")
        
        return output_paths
    
    def generate_format(self, project: VideoProject, format_name: str, output_dir: str = "output") -> str:
        """
        Genera video en formato específico
        
        Args:
            project: Proyecto de video
            format_name: Nombre del formato
            output_dir: Directorio de salida
            
        Returns:
            Ruta del archivo generado
        """
        try:
            if format_name not in self.formats:
                raise ValueError(f"Formato {format_name} no soportado")
            
            format_specs = self.formats[format_name]
            
            # Crear directorio de salida
            format_dir = Path(output_dir) / format_name
            format_dir.mkdir(exist_ok=True)
            
            # Generar nombre de archivo
            safe_title = self._sanitize_filename(project.title)
            filename = f"{safe_title}_{format_name}.mp4"
            output_path = format_dir / filename
            
            # Crear video en formato específico
            if format_specs.orientation == "portrait":
                video_clip = self._create_portrait_video(project, format_specs)
            elif format_specs.orientation == "square":
                video_clip = self._create_square_video(project, format_specs)
            else:  # landscape
                video_clip = self._create_landscape_video(project, format_specs)
            
            # Renderizar video
            video_clip.write_videofile(
                str(output_path),
                fps=VIDEO_CONFIG["fps"],
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generando formato {format_name}: {e}")
            return ""
    
    def _create_landscape_video(self, project: VideoProject, format_specs: FormatSpecs) -> VideoFileClip:
        """Crea video en formato landscape (16:9)"""
        try:
            # Crear clip base
            duration = project.duration
            base_clip = ColorClip(
                size=(format_specs.width, format_specs.height),
                color=self._hex_to_rgb(BRANDING["colors"]["secondary"]),
                duration=duration
            )
            
            # Agregar elementos adaptados al formato
            clips = [base_clip]
            
            # Título principal
            title_clip = self._create_title_clip(project.title, format_specs, duration)
            clips.append(title_clip)
            
            # Elementos de contenido
            content_clips = self._create_content_clips(project, format_specs)
            clips.extend(content_clips)
            
            # Logo Cine Norte
            logo_clip = self._create_logo_clip(format_specs, duration)
            clips.append(logo_clip)
            
            return CompositeVideoClip(clips)
            
        except Exception as e:
            logger.error(f"Error creando video landscape: {e}")
            return self._create_fallback_clip(format_specs)
    
    def _create_portrait_video(self, project: VideoProject, format_specs: FormatSpecs) -> VideoFileClip:
        """Crea video en formato portrait (9:16) para TikTok/Instagram Reels"""
        try:
            # Crear clip base
            duration = project.duration
            base_clip = ColorClip(
                size=(format_specs.width, format_specs.height),
                color=self._hex_to_rgb(BRANDING["colors"]["secondary"]),
                duration=duration
            )
            
            clips = [base_clip]
            
            # Para formato vertical, reorganizar elementos
            # Título en la parte superior
            title_clip = self._create_vertical_title_clip(project.title, format_specs, duration)
            clips.append(title_clip)
            
            # Contenido principal en el centro
            content_clips = self._create_vertical_content_clips(project, format_specs)
            clips.extend(content_clips)
            
            # Hashtags en la parte inferior
            hashtags_clip = self._create_hashtags_clip(project.script.hashtags, format_specs, duration)
            clips.append(hashtags_clip)
            
            # Logo en esquina
            logo_clip = self._create_corner_logo_clip(format_specs, duration)
            clips.append(logo_clip)
            
            return CompositeVideoClip(clips)
            
        except Exception as e:
            logger.error(f"Error creando video portrait: {e}")
            return self._create_fallback_clip(format_specs)
    
    def _create_square_video(self, project: VideoProject, format_specs: FormatSpecs) -> VideoFileClip:
        """Crea video en formato cuadrado (1:1) para Instagram posts"""
        try:
            # Crear clip base
            duration = project.duration
            base_clip = ColorClip(
                size=(format_specs.width, format_specs.height),
                color=self._hex_to_rgb(BRANDING["colors"]["secondary"]),
                duration=duration
            )
            
            clips = [base_clip]
            
            # Título centrado
            title_clip = self._create_square_title_clip(project.title, format_specs, duration)
            clips.append(title_clip)
            
            # Contenido adaptado para cuadrado
            content_clips = self._create_square_content_clips(project, format_specs)
            clips.extend(content_clips)
            
            # Logo centrado
            logo_clip = self._create_center_logo_clip(format_specs, duration)
            clips.append(logo_clip)
            
            return CompositeVideoClip(clips)
            
        except Exception as e:
            logger.error(f"Error creando video square: {e}")
            return self._create_fallback_clip(format_specs)
    
    def _create_title_clip(self, title: str, format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de título para formato landscape"""
        try:
            # Calcular tamaño de fuente basado en el formato
            font_size = self._calculate_font_size(format_specs, "title")
            
            clip = TextClip(
                title,
                fontsize=font_size,
                color=BRANDING["colors"]["primary"],
                font='Arial-Bold',
                method='caption',
                size=(format_specs.width - 200, 100)
            ).set_position(('center', 50)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando título: {e}")
            return TextClip("", fontsize=48, color="white").set_duration(1)
    
    def _create_vertical_title_clip(self, title: str, format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de título para formato vertical"""
        try:
            font_size = self._calculate_font_size(format_specs, "title")
            
            clip = TextClip(
                title,
                fontsize=font_size,
                color=BRANDING["colors"]["primary"],
                font='Arial-Bold',
                method='caption',
                size=(format_specs.width - 100, 150)
            ).set_position(('center', 50)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando título vertical: {e}")
            return TextClip("", fontsize=48, color="white").set_duration(1)
    
    def _create_square_title_clip(self, title: str, format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de título para formato cuadrado"""
        try:
            font_size = self._calculate_font_size(format_specs, "title")
            
            clip = TextClip(
                title,
                fontsize=font_size,
                color=BRANDING["colors"]["primary"],
                font='Arial-Bold',
                method='caption',
                size=(format_specs.width - 200, 120)
            ).set_position(('center', 50)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando título cuadrado: {e}")
            return TextClip("", fontsize=48, color="white").set_duration(1)
    
    def _create_content_clips(self, project: VideoProject, format_specs: FormatSpecs) -> List[TextClip]:
        """Crea clips de contenido para formato landscape"""
        clips = []
        
        try:
            # Crear clips para cada segmento del guion
            for i, segment in enumerate(project.script.segments):
                if i >= 3:  # Limitar a 3 segmentos para evitar sobrecarga
                    break
                
                font_size = self._calculate_font_size(format_specs, "content")
                
                clip = TextClip(
                    segment.text[:200] + "..." if len(segment.text) > 200 else segment.text,
                    fontsize=font_size,
                    color=BRANDING["colors"]["accent"],
                    font='Arial',
                    method='caption',
                    size=(format_specs.width - 400, 200)
                ).set_position((200, 200 + i * 250)).set_start(segment.start_time).set_end(segment.end_time)
                
                clips.append(clip)
            
            return clips
            
        except Exception as e:
            logger.error(f"Error creando clips de contenido: {e}")
            return []
    
    def _create_vertical_content_clips(self, project: VideoProject, format_specs: FormatSpecs) -> List[TextClip]:
        """Crea clips de contenido para formato vertical"""
        clips = []
        
        try:
            # Para formato vertical, mostrar menos texto pero más grande
            for i, segment in enumerate(project.script.segments):
                if i >= 2:  # Solo 2 segmentos para vertical
                    break
                
                font_size = self._calculate_font_size(format_specs, "content")
                
                # Texto más corto para formato vertical
                text = segment.text[:100] + "..." if len(segment.text) > 100 else segment.text
                
                clip = TextClip(
                    text,
                    fontsize=font_size,
                    color=BRANDING["colors"]["accent"],
                    font='Arial',
                    method='caption',
                    size=(format_specs.width - 100, 300)
                ).set_position(('center', 250 + i * 400)).set_start(segment.start_time).set_end(segment.end_time)
                
                clips.append(clip)
            
            return clips
            
        except Exception as e:
            logger.error(f"Error creando clips de contenido vertical: {e}")
            return []
    
    def _create_square_content_clips(self, project: VideoProject, format_specs: FormatSpecs) -> List[TextClip]:
        """Crea clips de contenido para formato cuadrado"""
        clips = []
        
        try:
            # Para formato cuadrado, contenido muy condensado
            for i, segment in enumerate(project.script.segments):
                if i >= 2:  # Solo 2 segmentos para cuadrado
                    break
                
                font_size = self._calculate_font_size(format_specs, "content")
                
                # Texto muy corto para formato cuadrado
                text = segment.text[:80] + "..." if len(segment.text) > 80 else segment.text
                
                clip = TextClip(
                    text,
                    fontsize=font_size,
                    color=BRANDING["colors"]["accent"],
                    font='Arial',
                    method='caption',
                    size=(format_specs.width - 200, 200)
                ).set_position(('center', 200 + i * 250)).set_start(segment.start_time).set_end(segment.end_time)
                
                clips.append(clip)
            
            return clips
            
        except Exception as e:
            logger.error(f"Error creando clips de contenido cuadrado: {e}")
            return []
    
    def _create_hashtags_clip(self, hashtags: List[str], format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de hashtags para formato vertical"""
        try:
            hashtags_text = " ".join(hashtags[:5])  # Máximo 5 hashtags
            
            clip = TextClip(
                hashtags_text,
                fontsize=24,
                color=BRANDING["colors"]["primary"],
                font='Arial',
                method='caption',
                size=(format_specs.width - 100, 100)
            ).set_position(('center', format_specs.height - 150)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando clip de hashtags: {e}")
            return TextClip("", fontsize=24, color="white").set_duration(1)
    
    def _create_logo_clip(self, format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de logo para formato landscape"""
        try:
            clip = TextClip(
                "CINE NORTE",
                fontsize=36,
                color=BRANDING["colors"]["accent"],
                font='Arial-Bold'
            ).set_position((50, format_specs.height - 100)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando logo: {e}")
            return TextClip("", fontsize=36, color="white").set_duration(1)
    
    def _create_corner_logo_clip(self, format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de logo para esquina en formato vertical"""
        try:
            clip = TextClip(
                "CINE NORTE",
                fontsize=24,
                color=BRANDING["colors"]["accent"],
                font='Arial-Bold'
            ).set_position((50, 50)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando logo de esquina: {e}")
            return TextClip("", fontsize=24, color="white").set_duration(1)
    
    def _create_center_logo_clip(self, format_specs: FormatSpecs, duration: float) -> TextClip:
        """Crea clip de logo centrado para formato cuadrado"""
        try:
            clip = TextClip(
                "CINE NORTE",
                fontsize=32,
                color=BRANDING["colors"]["accent"],
                font='Arial-Bold'
            ).set_position(('center', format_specs.height - 100)).set_duration(duration)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error creando logo centrado: {e}")
            return TextClip("", fontsize=32, color="white").set_duration(1)
    
    def _calculate_font_size(self, format_specs: FormatSpecs, element_type: str) -> int:
        """Calcula tamaño de fuente basado en el formato y tipo de elemento"""
        base_sizes = {
            "title": {"youtube": 72, "tiktok": 48, "instagram_post": 60, "facebook": 72, "twitter": 60},
            "content": {"youtube": 48, "tiktok": 32, "instagram_post": 40, "facebook": 48, "twitter": 40}
        }
        
        platform = format_specs.platform.lower()
        if platform in base_sizes[element_type]:
            return base_sizes[element_type][platform]
        
        # Tamaño por defecto basado en orientación
        if format_specs.orientation == "portrait":
            return base_sizes[element_type]["tiktok"]
        elif format_specs.orientation == "square":
            return base_sizes[element_type]["instagram_post"]
        else:
            return base_sizes[element_type]["youtube"]
    
    def _create_fallback_clip(self, format_specs: FormatSpecs) -> VideoFileClip:
        """Crea clip de respaldo en caso de error"""
        try:
            clip = ColorClip(
                size=(format_specs.width, format_specs.height),
                color=self._hex_to_rgb(BRANDING["colors"]["secondary"]),
                duration=10
            )
            
            text_clip = TextClip(
                "CINE NORTE",
                fontsize=48,
                color=BRANDING["colors"]["primary"],
                font='Arial-Bold'
            ).set_position('center').set_duration(10)
            
            return CompositeVideoClip([clip, text_clip])
            
        except Exception as e:
            logger.error(f"Error creando clip de respaldo: {e}")
            return ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=10)
    
    def _hex_to_rgb(self, hex_color):
        """Convierte color hex a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza nombre de archivo"""
        import re
        # Remover caracteres no válidos
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Limitar longitud
        filename = filename[:50]
        return filename
    
    def generate_thumbnails(self, project: VideoProject, output_dir: str = "output") -> Dict[str, str]:
        """
        Genera miniaturas para cada formato
        
        Args:
            project: Proyecto de video
            output_dir: Directorio de salida
            
        Returns:
            Diccionario con rutas de miniaturas por formato
        """
        thumbnails = {}
        
        try:
            for format_name, format_specs in self.formats.items():
                thumbnail_path = self._create_thumbnail(project, format_specs, output_dir)
                if thumbnail_path:
                    thumbnails[format_name] = thumbnail_path
                    
        except Exception as e:
            logger.error(f"Error generando miniaturas: {e}")
        
        return thumbnails
    
    def _create_thumbnail(self, project: VideoProject, format_specs: FormatSpecs, output_dir: str) -> str:
        """Crea miniatura para formato específico"""
        try:
            # Crear imagen base
            img = Image.new('RGB', (format_specs.width, format_specs.height), 
                          self._hex_to_rgb(BRANDING["colors"]["secondary"]))
            draw = ImageDraw.Draw(img)
            
            # Cargar fuente
            try:
                title_font = ImageFont.truetype("arial.ttf", 72)
                subtitle_font = ImageFont.truetype("arial.ttf", 36)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Título principal
            title = project.title
            bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = bbox[2] - bbox[0]
            title_x = (format_specs.width - title_width) // 2
            title_y = format_specs.height // 2 - 50
            
            # Sombra del título
            draw.text((title_x + 3, title_y + 3), title, fill=(0, 0, 0), font=title_font)
            # Título principal
            draw.text((title_x, title_y), title, fill=self._hex_to_rgb(BRANDING["colors"]["primary"]), font=title_font)
            
            # Subtítulo
            subtitle = "Análisis Cinematográfico"
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = bbox[2] - bbox[0]
            subtitle_x = (format_specs.width - subtitle_width) // 2
            subtitle_y = title_y + 80
            
            draw.text((subtitle_x, subtitle_y), subtitle, fill=self._hex_to_rgb(BRANDING["colors"]["accent"]), font=subtitle_font)
            
            # Logo Cine Norte
            logo_text = "CINE NORTE"
            bbox = draw.textbbox((0, 0), logo_text, font=subtitle_font)
            logo_width = bbox[2] - bbox[0]
            logo_x = (format_specs.width - logo_width) // 2
            logo_y = format_specs.height - 100
            
            draw.text((logo_x, logo_y), logo_text, fill=self._hex_to_rgb(BRANDING["colors"]["accent"]), font=subtitle_font)
            
            # Guardar miniatura
            format_dir = Path(output_dir) / format_name
            format_dir.mkdir(exist_ok=True)
            
            thumbnail_path = format_dir / f"thumbnail_{format_specs.name.lower().replace(' ', '_')}.png"
            img.save(thumbnail_path, "PNG")
            
            return str(thumbnail_path)
            
        except Exception as e:
            logger.error(f"Error creando miniatura para {format_specs.name}: {e}")
            return ""
