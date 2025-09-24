"""
Generador de miniaturas para Cine Norte
Crea miniaturas optimizadas para diferentes plataformas
"""
import os
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import json
from datetime import datetime
import math

# Importaciones para generación de miniaturas
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import cv2
    import numpy as np
    from moviepy.editor import VideoFileClip
except ImportError:
    print("Instalando dependencias de miniaturas...")
    os.system("pip install pillow opencv-python moviepy numpy")

from config import config

@dataclass
class ThumbnailSpec:
    """Especificación de miniatura"""
    platform: str
    width: int
    height: int
    aspect_ratio: str
    text_size: int
    overlay_opacity: float
    description: str

@dataclass
class GeneratedThumbnail:
    """Miniatura generada"""
    platform: str
    image_path: str
    thumbnail_spec: ThumbnailSpec
    text_overlay: str
    color_scheme: Dict[str, str]
    optimization_score: float

class ThumbnailGenerator:
    """Generador de miniaturas para Cine Norte"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp()
        
        # Especificaciones de miniaturas por plataforma
        self.thumbnail_specs = {
            "youtube": ThumbnailSpec(
                platform="YouTube",
                width=1280,
                height=720,
                aspect_ratio="16:9",
                text_size=48,
                overlay_opacity=0.8,
                description="Miniatura estándar para YouTube"
            ),
            "tiktok": ThumbnailSpec(
                platform="TikTok",
                width=1080,
                height=1920,
                aspect_ratio="9:16",
                text_size=36,
                overlay_opacity=0.7,
                description="Miniatura vertical para TikTok"
            ),
            "instagram": ThumbnailSpec(
                platform="Instagram",
                width=1080,
                height=1080,
                aspect_ratio="1:1",
                text_size=42,
                overlay_opacity=0.75,
                description="Miniatura cuadrado para Instagram"
            ),
            "facebook": ThumbnailSpec(
                platform="Facebook",
                width=1200,
                height=630,
                aspect_ratio="1.91:1",
                text_size=44,
                overlay_opacity=0.8,
                description="Miniatura para Facebook"
            ),
            "twitter": ThumbnailSpec(
                platform="Twitter",
                width=1200,
                height=675,
                aspect_ratio="16:9",
                text_size=40,
                overlay_opacity=0.8,
                description="Miniatura para Twitter"
            )
        }
        
        # Esquemas de color predefinidos
        self.color_schemes = {
            "cinematic": {
                "primary": "#E50914",
                "secondary": "#C0C0C0", 
                "background": "#0A0A0A",
                "text": "#FFFFFF",
                "accent": "#FFD700"
            },
            "dramatic": {
                "primary": "#8B0000",
                "secondary": "#808080",
                "background": "#1A1A1A",
                "text": "#FFFFFF",
                "accent": "#FF4500"
            },
            "action": {
                "primary": "#FF0000",
                "secondary": "#FFA500",
                "background": "#000000",
                "text": "#FFFFFF",
                "accent": "#00FFFF"
            },
            "mystery": {
                "primary": "#4B0082",
                "secondary": "#9370DB",
                "background": "#2F2F2F",
                "text": "#FFFFFF",
                "accent": "#FFD700"
            }
        }
    
    def generate_thumbnails(self, video_path: str, content_info: Dict,
                          title: str, style: str = "cinematic") -> List[GeneratedThumbnail]:
        """
        Genera miniaturas para todas las plataformas
        
        Args:
            video_path: Ruta del video fuente
            content_info: Información del contenido
            title: Título del contenido
            style: Estilo visual (cinematic, dramatic, action, mystery)
            
        Returns:
            Lista de miniaturas generadas
        """
        generated_thumbnails = []
        
        for platform, spec in self.thumbnail_specs.items():
            try:
                thumbnail = self._generate_single_thumbnail(
                    video_path, content_info, title, platform, spec, style
                )
                
                if thumbnail:
                    generated_thumbnails.append(thumbnail)
                    
            except Exception as e:
                self.logger.error(f"Error generando miniatura para {platform}: {e}")
                continue
        
        return generated_thumbnails
    
    def _generate_single_thumbnail(self, video_path: str, content_info: Dict,
                                 title: str, platform: str, spec: ThumbnailSpec,
                                 style: str) -> Optional[GeneratedThumbnail]:
        """Genera una miniatura específica"""
        try:
            # Obtener esquema de color
            color_scheme = self.color_schemes.get(style, self.color_schemes["cinematic"])
            
            # Extraer frame del video
            base_image = self._extract_video_frame(video_path, spec)
            
            # Aplicar efectos visuales
            enhanced_image = self._apply_visual_effects(base_image, content_info, style)
            
            # Crear overlay de texto
            text_overlay = self._create_text_overlay(title, content_info, spec, color_scheme)
            
            # Combinar imagen base con overlay
            final_image = self._combine_image_and_overlay(enhanced_image, text_overlay, spec)
            
            # Agregar elementos de marca Cine Norte
            branded_image = self._add_cine_norte_branding(final_image, spec, color_scheme)
            
            # Guardar miniatura
            thumbnail_path = self._save_thumbnail(branded_image, platform, title)
            
            # Calcular score de optimización
            optimization_score = self._calculate_optimization_score(
                branded_image, platform, content_info
            )
            
            return GeneratedThumbnail(
                platform=platform,
                image_path=thumbnail_path,
                thumbnail_spec=spec,
                text_overlay=title,
                color_scheme=color_scheme,
                optimization_score=optimization_score
            )
            
        except Exception as e:
            self.logger.error(f"Error generando miniatura {platform}: {e}")
            return None
    
    def _extract_video_frame(self, video_path: str, spec: ThumbnailSpec) -> Image.Image:
        """Extrae frame representativo del video"""
        try:
            # Cargar video
            cap = cv2.VideoCapture(video_path)
            
            # Obtener frame en el 30% del video
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            target_frame = int(total_frames * 0.3)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            
            cap.release()
            
            if ret:
                # Convertir BGR a RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                
                # Redimensionar según especificación
                image = image.resize((spec.width, spec.height), Image.Resampling.LANCZOS)
                
                return image
            else:
                # Crear imagen de respaldo
                return self._create_fallback_image(spec)
                
        except Exception as e:
            self.logger.error(f"Error extrayendo frame: {e}")
            return self._create_fallback_image(spec)
    
    def _create_fallback_image(self, spec: ThumbnailSpec) -> Image.Image:
        """Crea imagen de respaldo si falla la extracción"""
        # Crear imagen con gradiente
        image = Image.new('RGB', (spec.width, spec.height), (10, 10, 10))
        draw = ImageDraw.Draw(image)
        
        # Dibujar gradiente simple
        for y in range(spec.height):
            color_value = int(255 * (y / spec.height))
            draw.line([(0, y), (spec.width, y)], fill=(color_value, 0, 0))
        
        return image
    
    def _apply_visual_effects(self, image: Image.Image, content_info: Dict, style: str) -> Image.Image:
        """Aplica efectos visuales según el estilo"""
        try:
            # Aplicar filtros según el estilo
            if style == "dramatic":
                # Aumentar contraste y saturación
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.3)
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.2)
                
            elif style == "action":
                # Aumentar nitidez y brillo
                image = image.filter(ImageFilter.SHARPEN)
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.1)
                
            elif style == "mystery":
                # Aplicar desaturación parcial
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(0.7)
                # Agregar viñeta
                image = self._add_vignette(image)
            
            # Aplicar viñeta sutil a todos los estilos
            image = self._add_subtle_vignette(image)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error aplicando efectos visuales: {e}")
            return image
    
    def _add_vignette(self, image: Image.Image) -> Image.Image:
        """Agrega efecto de viñeta"""
        width, height = image.size
        
        # Crear máscara de viñeta
        mask = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(mask)
        
        # Dibujar elipse oscura en el centro
        center_x, center_y = width // 2, height // 2
        radius_x, radius_y = width // 2, height // 2
        
        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                max_distance = math.sqrt(radius_x ** 2 + radius_y ** 2)
                
                if distance < max_distance:
                    alpha = int(255 * (distance / max_distance))
                    mask.putpixel((x, y), alpha)
        
        # Aplicar máscara
        image.putalpha(mask)
        
        return image
    
    def _add_subtle_vignette(self, image: Image.Image) -> Image.Image:
        """Agrega viñeta sutil"""
        width, height = image.size
        
        # Crear overlay con gradiente radial
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Dibujar gradiente radial sutil
        center_x, center_y = width // 2, height // 2
        max_radius = max(width, height) // 2
        
        for radius in range(max_radius, 0, -10):
            alpha = int(30 * (1 - radius / max_radius))
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                fill=(0, 0, 0, alpha)
            )
        
        # Combinar con imagen original
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        image = Image.alpha_composite(image, overlay)
        return image.convert('RGB')
    
    def _create_text_overlay(self, title: str, content_info: Dict, spec: ThumbnailSpec,
                           color_scheme: Dict[str, str]) -> Image.Image:
        """Crea overlay de texto"""
        try:
            # Crear imagen transparente
            overlay = Image.new('RGBA', (spec.width, spec.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Configurar fuentes
            try:
                title_font = ImageFont.truetype("arial.ttf", spec.text_size)
                subtitle_font = ImageFont.truetype("arial.ttf", spec.text_size // 2)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Preparar texto
            title_text = self._format_title_text(title, spec.width)
            subtitle_text = self._get_subtitle_text(content_info)
            
            # Calcular posiciones
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            # Posición del título (centro inferior)
            title_x = (spec.width - title_width) // 2
            title_y = spec.height - title_height - 100
            
            # Dibujar fondo del título
            padding = 20
            draw.rectangle(
                [title_x - padding, title_y - padding, 
                 title_x + title_width + padding, title_y + title_height + padding],
                fill=(0, 0, 0, int(255 * spec.overlay_opacity))
            )
            
            # Dibujar título
            draw.text((title_x, title_y), title_text, font=title_font, 
                     fill=color_scheme["text"])
            
            # Dibujar subtítulo si hay espacio
            if title_y > 150:
                subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
                subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
                subtitle_x = (spec.width - subtitle_width) // 2
                subtitle_y = title_y - 50
                
                draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font,
                         fill=color_scheme["secondary"])
            
            return overlay
            
        except Exception as e:
            self.logger.error(f"Error creando overlay de texto: {e}")
            return Image.new('RGBA', (spec.width, spec.height), (0, 0, 0, 0))
    
    def _format_title_text(self, title: str, max_width: int) -> str:
        """Formatea el título para que quepa en la miniatura"""
        # Dividir título en líneas si es muy largo
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            
            # Estimar ancho del texto (aproximado)
            estimated_width = len(test_line) * 20  # Aproximación
            
            if estimated_width <= max_width - 100:  # Dejar margen
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines[:3])  # Máximo 3 líneas
    
    def _get_subtitle_text(self, content_info: Dict) -> str:
        """Obtiene texto del subtítulo"""
        platform = content_info.get("platform", "")
        content_type = content_info.get("content_type", "")
        
        if content_type == "movie":
            return f"Película en {platform}"
        elif content_type == "tv":
            return f"Serie en {platform}"
        else:
            return f"Contenido en {platform}"
    
    def _combine_image_and_overlay(self, base_image: Image.Image, overlay: Image.Image,
                                 spec: ThumbnailSpec) -> Image.Image:
        """Combina imagen base con overlay"""
        try:
            # Convertir imagen base a RGBA si es necesario
            if base_image.mode != 'RGBA':
                base_image = base_image.convert('RGBA')
            
            # Combinar imágenes
            combined = Image.alpha_composite(base_image, overlay)
            
            return combined.convert('RGB')
            
        except Exception as e:
            self.logger.error(f"Error combinando imágenes: {e}")
            return base_image
    
    def _add_cine_norte_branding(self, image: Image.Image, spec: ThumbnailSpec,
                               color_scheme: Dict[str, str]) -> Image.Image:
        """Agrega branding de Cine Norte"""
        try:
            # Crear overlay de marca
            branding_overlay = Image.new('RGBA', (spec.width, spec.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(branding_overlay)
            
            # Configurar fuente
            try:
                brand_font = ImageFont.truetype("arial.ttf", spec.text_size // 3)
            except:
                brand_font = ImageFont.load_default()
            
            # Texto de marca
            brand_text = "CINE NORTE"
            brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
            brand_width = brand_bbox[2] - brand_bbox[0]
            brand_height = brand_bbox[3] - brand_bbox[1]
            
            # Posición (esquina superior derecha)
            brand_x = spec.width - brand_width - 20
            brand_y = 20
            
            # Dibujar fondo de marca
            padding = 10
            draw.rectangle(
                [brand_x - padding, brand_y - padding,
                 brand_x + brand_width + padding, brand_y + brand_height + padding],
                fill=(0, 0, 0, 200)
            )
            
            # Dibujar texto de marca
            draw.text((brand_x, brand_y), brand_text, font=brand_font,
                     fill=color_scheme["primary"])
            
            # Agregar línea decorativa
            line_y = brand_y + brand_height + 5
            draw.line([brand_x, line_y, brand_x + brand_width, line_y],
                     fill=color_scheme["accent"], width=2)
            
            # Combinar con imagen
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            final_image = Image.alpha_composite(image, branding_overlay)
            return final_image.convert('RGB')
            
        except Exception as e:
            self.logger.error(f"Error agregando branding: {e}")
            return image
    
    def _save_thumbnail(self, image: Image.Image, platform: str, title: str) -> str:
        """Guarda la miniatura generada"""
        try:
            # Crear nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thumbnail_{title.replace(' ', '_')}_{platform}_{timestamp}.jpg"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Guardar con alta calidad
            image.save(filepath, "JPEG", quality=95, optimize=True)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error guardando miniatura: {e}")
            return None
    
    def _calculate_optimization_score(self, image: Image.Image, platform: str,
                                    content_info: Dict) -> float:
        """Calcula score de optimización de la miniatura"""
        try:
            score = 0.0
            
            # Score por contraste (0-25 puntos)
            contrast_score = self._analyze_contrast(image)
            score += contrast_score * 25
            
            # Score por legibilidad del texto (0-25 puntos)
            readability_score = self._analyze_text_readability(image)
            score += readability_score * 25
            
            # Score por composición (0-25 puntos)
            composition_score = self._analyze_composition(image)
            score += composition_score * 25
            
            # Score por branding (0-25 puntos)
            branding_score = self._analyze_branding_presence(image)
            score += branding_score * 25
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error calculando score: {e}")
            return 50.0
    
    def _analyze_contrast(self, image: Image.Image) -> float:
        """Analiza contraste de la imagen"""
        try:
            # Convertir a escala de grises
            gray = image.convert('L')
            
            # Calcular histograma
            histogram = gray.histogram()
            
            # Calcular contraste (diferencia entre píxeles claros y oscuros)
            total_pixels = sum(histogram)
            weighted_sum = sum(i * histogram[i] for i in range(256))
            mean = weighted_sum / total_pixels
            
            # Calcular desviación estándar como medida de contraste
            variance = sum(histogram[i] * (i - mean) ** 2 for i in range(256)) / total_pixels
            std_dev = math.sqrt(variance)
            
            # Normalizar a 0-1
            return min(std_dev / 128, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error analizando contraste: {e}")
            return 0.5
    
    def _analyze_text_readability(self, image: Image.Image) -> float:
        """Analiza legibilidad del texto"""
        try:
            # Convertir a escala de grises
            gray = image.convert('L')
            
            # Buscar áreas con texto (bordes y contornos)
            # Esto es una implementación simplificada
            # En producción se usaría OCR o detección de texto
            
            # Análisis de bordes como proxy de legibilidad
            import numpy as np
            img_array = np.array(gray)
            
            # Calcular gradientes
            grad_x = np.abs(np.gradient(img_array, axis=1))
            grad_y = np.abs(np.gradient(img_array, axis=0))
            
            # Promedio de gradientes como medida de definición
            avg_gradient = (np.mean(grad_x) + np.mean(grad_y)) / 2
            
            # Normalizar
            return min(avg_gradient / 50, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error analizando legibilidad: {e}")
            return 0.5
    
    def _analyze_composition(self, image: Image.Image) -> float:
        """Analiza composición de la imagen"""
        try:
            width, height = image.size
            
            # Regla de tercios
            # Verificar si hay elementos importantes en los puntos de intersección
            third_x = width // 3
            third_y = height // 3
            
            # Análisis simplificado de distribución de contenido
            # En producción se haría análisis más sofisticado
            
            # Verificar balance de colores
            colors = image.getcolors(maxcolors=256*256*256)
            if colors:
                # Calcular diversidad de colores
                color_diversity = len(colors) / 1000  # Normalizar
                return min(color_diversity, 1.0)
            
            return 0.5
            
        except Exception as e:
            self.logger.error(f"Error analizando composición: {e}")
            return 0.5
    
    def _analyze_branding_presence(self, image: Image.Image) -> float:
        """Analiza presencia del branding"""
        try:
            # Buscar colores de marca en la imagen
            colors = image.getcolors(maxcolors=256*256*256)
            
            if not colors:
                return 0.0
            
            # Colores de marca Cine Norte
            brand_colors = [
                (229, 9, 20),    # #E50914
                (192, 192, 192), # #C0C0C0
                (10, 10, 10)     # #0A0A0A
            ]
            
            brand_pixel_count = 0
            total_pixels = sum(count for count, color in colors)
            
            for count, color in colors:
                for brand_color in brand_colors:
                    # Tolerancia de color
                    if all(abs(c - bc) < 30 for c, bc in zip(color, brand_color)):
                        brand_pixel_count += count
                        break
            
            return min(brand_pixel_count / total_pixels * 10, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error analizando branding: {e}")
            return 0.5
    
    def get_thumbnail_specs(self) -> Dict[str, ThumbnailSpec]:
        """Obtiene especificaciones de miniaturas"""
        return self.thumbnail_specs.copy()
    
    def get_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Obtiene esquemas de color disponibles"""
        return self.color_schemes.copy()
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.error(f"Error limpiando archivos temporales: {e}")

# Instancia global del generador
thumbnail_generator = ThumbnailGenerator()
