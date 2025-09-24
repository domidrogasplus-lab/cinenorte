"""
Generador de formatos múltiples para Cine Norte
Crea videos optimizados para diferentes plataformas (YouTube, TikTok, Instagram)
"""
import os
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import json
from datetime import datetime

# Importaciones para procesamiento de video
try:
    from moviepy.editor import *
    from moviepy.video.fx import resize, crop
    from moviepy.video.tools.drawing import color_gradient
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Instalando dependencias de formato...")
    os.system("pip install moviepy opencv-python pillow numpy")

from config import config

@dataclass
class FormatSpec:
    """Especificación de formato de video"""
    name: str
    width: int
    height: int
    aspect_ratio: str
    platform: str
    max_duration: int  # segundos
    recommended_fps: int
    bitrate: str
    description: str

@dataclass
class GeneratedFormat:
    """Formato generado"""
    format_type: str
    video_path: str
    thumbnail_path: str
    metadata: Dict
    optimization_score: float

class FormatGenerator:
    """Generador de formatos múltiples"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp()
        
        # Especificaciones de formatos
        self.formats = {
            "youtube": FormatSpec(
                name="YouTube",
                width=1920,
                height=1080,
                aspect_ratio="16:9",
                platform="youtube",
                max_duration=180,
                recommended_fps=24,
                bitrate="5000k",
                description="Formato estándar para YouTube, optimizado para desktop y TV"
            ),
            "tiktok": FormatSpec(
                name="TikTok",
                width=1080,
                height=1920,
                aspect_ratio="9:16",
                platform="tiktok",
                max_duration=60,
                recommended_fps=30,
                bitrate="3000k",
                description="Formato vertical para TikTok, optimizado para móviles"
            ),
            "instagram_reels": FormatSpec(
                name="Instagram Reels",
                width=1080,
                height=1920,
                aspect_ratio="9:16",
                platform="instagram",
                max_duration=90,
                recommended_fps=30,
                bitrate="3000k",
                description="Formato vertical para Instagram Reels"
            ),
            "instagram_square": FormatSpec(
                name="Instagram Square",
                width=1080,
                height=1080,
                aspect_ratio="1:1",
                platform="instagram",
                max_duration=60,
                recommended_fps=30,
                bitrate="2500k",
                description="Formato cuadrado para Instagram posts"
            ),
            "facebook": FormatSpec(
                name="Facebook",
                width=1920,
                height=1080,
                aspect_ratio="16:9",
                platform="facebook",
                max_duration=240,
                recommended_fps=24,
                bitrate="4000k",
                description="Formato para Facebook videos"
            ),
            "twitter": FormatSpec(
                name="Twitter",
                width=1280,
                height=720,
                aspect_ratio="16:9",
                platform="twitter",
                max_duration=140,
                recommended_fps=30,
                bitrate="2000k",
                description="Formato para Twitter videos"
            )
        }
    
    def generate_all_formats(self, source_video_path: str, script_title: str,
                           content_info: Dict) -> List[GeneratedFormat]:
        """
        Genera todos los formatos disponibles para un video
        
        Args:
            source_video_path: Ruta del video fuente
            script_title: Título del guion
            content_info: Información del contenido
            
        Returns:
            Lista de formatos generados
        """
        generated_formats = []
        
        for format_type, spec in self.formats.items():
            try:
                generated_format = self._generate_single_format(
                    source_video_path, 
                    format_type, 
                    spec, 
                    script_title,
                    content_info
                )
                
                if generated_format:
                    generated_formats.append(generated_format)
                    
            except Exception as e:
                self.logger.error(f"Error generando formato {format_type}: {e}")
                continue
        
        return generated_formats
    
    def _generate_single_format(self, source_video_path: str, format_type: str,
                               spec: FormatSpec, script_title: str,
                               content_info: Dict) -> Optional[GeneratedFormat]:
        """Genera un formato específico"""
        try:
            # Cargar video fuente
            source_video = VideoFileClip(source_video_path)
            
            # Ajustar duración si es necesario
            if source_video.duration > spec.max_duration:
                source_video = source_video.subclip(0, spec.max_duration)
            
            # Aplicar transformaciones específicas del formato
            transformed_video = self._apply_format_transformations(
                source_video, format_type, spec
            )
            
            # Optimizar para la plataforma
            optimized_video = self._optimize_for_platform(
                transformed_video, format_type, spec
            )
            
            # Exportar video
            video_path = self._export_format_video(
                optimized_video, format_type, script_title, spec
            )
            
            # Generar miniatura
            thumbnail_path = self._generate_thumbnail(
                optimized_video, format_type, script_title, content_info
            )
            
            # Calcular score de optimización
            optimization_score = self._calculate_optimization_score(
                optimized_video, format_type, spec
            )
            
            # Crear metadatos
            metadata = self._create_format_metadata(
                format_type, spec, content_info, optimization_score
            )
            
            return GeneratedFormat(
                format_type=format_type,
                video_path=video_path,
                thumbnail_path=thumbnail_path,
                metadata=metadata,
                optimization_score=optimization_score
            )
            
        except Exception as e:
            self.logger.error(f"Error generando formato {format_type}: {e}")
            return None
    
    def _apply_format_transformations(self, video: VideoClip, format_type: str,
                                    spec: FormatSpec) -> VideoClip:
        """Aplica transformaciones específicas del formato"""
        try:
            current_width, current_height = video.size
            target_width, target_height = spec.width, spec.height
            
            # Calcular factor de escala
            scale_factor = min(target_width / current_width, target_height / current_height)
            
            # Redimensionar manteniendo aspecto
            scaled_video = video.resize(scale_factor)
            
            # Aplicar transformaciones específicas por formato
            if format_type == "tiktok" or format_type == "instagram_reels":
                # Formato vertical - centrar y recortar
                transformed_video = self._create_vertical_format(scaled_video, spec)
            elif format_type == "instagram_square":
                # Formato cuadrado - centrar y recortar
                transformed_video = self._create_square_format(scaled_video, spec)
            else:
                # Formato horizontal - centrar y rellenar si es necesario
                transformed_video = self._create_horizontal_format(scaled_video, spec)
            
            return transformed_video
            
        except Exception as e:
            self.logger.error(f"Error aplicando transformaciones: {e}")
            return video
    
    def _create_vertical_format(self, video: VideoClip, spec: FormatSpec) -> VideoClip:
        """Crea formato vertical (9:16)"""
        try:
            # Centrar horizontalmente
            x_center = video.w // 2
            y_center = video.h // 2
            
            # Recortar para formato vertical
            cropped = video.crop(
                x_center=x_center,
                y_center=y_center,
                width=min(video.w, int(video.h * spec.width / spec.height)),
                height=min(video.h, int(video.w * spec.height / spec.width))
            )
            
            # Redimensionar al tamaño objetivo
            final_video = cropped.resize((spec.width, spec.height))
            
            return final_video
            
        except Exception as e:
            self.logger.error(f"Error creando formato vertical: {e}")
            return video
    
    def _create_square_format(self, video: VideoClip, spec: FormatSpec) -> VideoClip:
        """Crea formato cuadrado (1:1)"""
        try:
            # Usar la dimensión más pequeña
            min_dim = min(video.w, video.h)
            
            # Centrar y recortar cuadrado
            x_center = video.w // 2
            y_center = video.h // 2
            
            cropped = video.crop(
                x_center=x_center,
                y_center=y_center,
                width=min_dim,
                height=min_dim
            )
            
            # Redimensionar al tamaño objetivo
            final_video = cropped.resize((spec.width, spec.height))
            
            return final_video
            
        except Exception as e:
            self.logger.error(f"Error creando formato cuadrado: {e}")
            return video
    
    def _create_horizontal_format(self, video: VideoClip, spec: FormatSpec) -> VideoClip:
        """Crea formato horizontal (16:9)"""
        try:
            # Redimensionar manteniendo aspecto
            final_video = video.resize((spec.width, spec.height))
            
            return final_video
            
        except Exception as e:
            self.logger.error(f"Error creando formato horizontal: {e}")
            return video
    
    def _optimize_for_platform(self, video: VideoClip, format_type: str,
                              spec: FormatSpec) -> VideoClip:
        """Optimiza video para plataforma específica"""
        try:
            # Ajustar FPS
            if video.fps != spec.recommended_fps:
                video = video.set_fps(spec.recommended_fps)
            
            # Aplicar optimizaciones específicas por plataforma
            if format_type == "tiktok":
                # Optimizaciones para TikTok
                video = self._optimize_for_tiktok(video)
            elif format_type == "instagram_reels":
                # Optimizaciones para Instagram Reels
                video = self._optimize_for_instagram_reels(video)
            elif format_type == "youtube":
                # Optimizaciones para YouTube
                video = self._optimize_for_youtube(video)
            
            return video
            
        except Exception as e:
            self.logger.error(f"Error optimizando para plataforma: {e}")
            return video
    
    def _optimize_for_tiktok(self, video: VideoClip) -> VideoClip:
        """Optimizaciones específicas para TikTok"""
        try:
            # Aumentar contraste y saturación para móviles
            # (En implementación real, se usarían efectos de color)
            
            # Agregar transiciones más rápidas
            # (En implementación real, se ajustarían los cortes)
            
            return video
            
        except Exception as e:
            self.logger.error(f"Error optimizando para TikTok: {e}")
            return video
    
    def _optimize_for_instagram_reels(self, video: VideoClip) -> VideoClip:
        """Optimizaciones específicas para Instagram Reels"""
        try:
            # Optimizar para feed de Instagram
            # (En implementación real, se aplicarían filtros específicos)
            
            return video
            
        except Exception as e:
            self.logger.error(f"Error optimizando para Instagram: {e}")
            return video
    
    def _optimize_for_youtube(self, video: VideoClip) -> VideoClip:
        """Optimizaciones específicas para YouTube"""
        try:
            # Optimizar para reproducción en diferentes dispositivos
            # (En implementación real, se ajustaría la calidad)
            
            return video
            
        except Exception as e:
            self.logger.error(f"Error optimizando para YouTube: {e}")
            return video
    
    def _export_format_video(self, video: VideoClip, format_type: str,
                           script_title: str, spec: FormatSpec) -> str:
        """Exporta video en formato específico"""
        try:
            # Crear nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cine_norte_{script_title.replace(' ', '_')}_{format_type}_{timestamp}.mp4"
            output_path = os.path.join(self.temp_dir, filename)
            
            # Configuración de exportación
            codec = 'libx264'
            audio_codec = 'aac'
            temp_audiofile = f'temp-audio-{format_type}.m4a'
            
            # Exportar con configuración específica
            video.write_videofile(
                output_path,
                codec=codec,
                audio_codec=audio_codec,
                temp_audiofile=temp_audiofile,
                remove_temp=True,
                fps=spec.recommended_fps,
                bitrate=spec.bitrate
            )
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error exportando formato {format_type}: {e}")
            return None
    
    def _generate_thumbnail(self, video: VideoClip, format_type: str,
                          script_title: str, content_info: Dict) -> str:
        """Genera miniatura para el formato"""
        try:
            # Obtener frame representativo
            frame_time = min(video.duration * 0.3, 10)  # 30% del video o 10 segundos
            frame = video.get_frame(frame_time)
            
            # Crear imagen base
            img = Image.fromarray(frame.astype('uint8'))
            
            # Redimensionar según formato
            spec = self.formats[format_type]
            img = img.resize((spec.width, spec.height), Image.Resampling.LANCZOS)
            
            # Agregar overlay de Cine Norte
            img = self._add_cine_norte_overlay(img, script_title, format_type)
            
            # Guardar miniatura
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            thumbnail_filename = f"thumbnail_{script_title.replace(' ', '_')}_{format_type}_{timestamp}.jpg"
            thumbnail_path = os.path.join(self.temp_dir, thumbnail_filename)
            img.save(thumbnail_path, "JPEG", quality=95)
            
            return thumbnail_path
            
        except Exception as e:
            self.logger.error(f"Error generando miniatura: {e}")
            return None
    
    def _add_cine_norte_overlay(self, img: Image.Image, title: str, format_type: str) -> Image.Image:
        """Agrega overlay de Cine Norte a la miniatura"""
        try:
            # Crear overlay
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Configurar fuente
            font_size = min(img.width, img.height) // 20
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Dibujar fondo semi-transparente
            text_bbox = draw.textbbox((0, 0), "CINE NORTE", font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Posición del overlay
            x = (img.width - text_width) // 2
            y = img.height - text_height - 20
            
            # Dibujar fondo
            draw.rectangle(
                [x - 10, y - 10, x + text_width + 10, y + text_height + 10],
                fill=(10, 10, 10, 180)
            )
            
            # Dibujar texto
            draw.text((x, y), "CINE NORTE", font=font, fill=(229, 9, 20, 255))
            
            # Combinar con imagen original
            img_rgba = img.convert('RGBA')
            final_img = Image.alpha_composite(img_rgba, overlay)
            
            return final_img.convert('RGB')
            
        except Exception as e:
            self.logger.error(f"Error agregando overlay: {e}")
            return img
    
    def _calculate_optimization_score(self, video: VideoClip, format_type: str,
                                    spec: FormatSpec) -> float:
        """Calcula score de optimización para el formato"""
        try:
            score = 0.0
            
            # Score por duración (0-30 puntos)
            duration_score = min(30, (spec.max_duration - video.duration) / spec.max_duration * 30)
            score += max(0, duration_score)
            
            # Score por resolución (0-25 puntos)
            width, height = video.size
            resolution_score = min(25, (width * height) / (spec.width * spec.height) * 25)
            score += resolution_score
            
            # Score por FPS (0-20 puntos)
            fps_score = min(20, video.fps / spec.recommended_fps * 20)
            score += fps_score
            
            # Score por aspecto (0-25 puntos)
            aspect_ratio = width / height
            target_aspect = spec.width / spec.height
            aspect_score = 25 - abs(aspect_ratio - target_aspect) * 25
            score += max(0, aspect_score)
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error calculando score: {e}")
            return 0.0
    
    def _create_format_metadata(self, format_type: str, spec: FormatSpec,
                               content_info: Dict, optimization_score: float) -> Dict:
        """Crea metadatos para el formato"""
        return {
            "format_type": format_type,
            "platform": spec.platform,
            "dimensions": f"{spec.width}x{spec.height}",
            "aspect_ratio": spec.aspect_ratio,
            "max_duration": spec.max_duration,
            "recommended_fps": spec.recommended_fps,
            "bitrate": spec.bitrate,
            "optimization_score": optimization_score,
            "description": spec.description,
            "content_title": content_info.get("title", ""),
            "content_platform": content_info.get("platform", ""),
            "generated_at": datetime.now().isoformat()
        }
    
    def get_format_specs(self) -> Dict[str, FormatSpec]:
        """Obtiene especificaciones de todos los formatos"""
        return self.formats.copy()
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.error(f"Error limpiando archivos temporales: {e}")

# Instancia global del generador
format_generator = FormatGenerator()
