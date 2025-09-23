"""
Generador de miniaturas y metadatos SEO para Cine Norte
"""

import os
import tempfile
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from config import BRANDING, SEO_CONFIG
from src.script_generator import GeneratedScript
from src.content_analyzer import ContentItem

logger = logging.getLogger(__name__)

@dataclass
class ThumbnailDesign:
    """Diseño de miniatura"""
    title: str
    subtitle: str
    background_image: str
    overlay_color: str
    text_color: str
    accent_color: str
    style: str  # 'cinematic', 'modern', 'vintage', 'minimal'
    elements: List[str]  # Elementos adicionales

@dataclass
class SEOData:
    """Datos SEO optimizados"""
    title: str
    description: str
    keywords: List[str]
    hashtags: List[str]
    tags: List[str]
    category: str
    language: str

class ThumbnailGenerator:
    """Generador de miniaturas y metadatos SEO"""
    
    def __init__(self):
        self.branding = BRANDING
        self.seo_config = SEO_CONFIG
        self.temp_dir = Path("temp/thumbnails")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Cargar fuentes
        self._load_fonts()
        
        # Inicializar estilos de miniatura
        self._initialize_thumbnail_styles()
    
    def _load_fonts(self):
        """Carga fuentes para las miniaturas"""
        try:
            # Intentar cargar fuentes del sistema
            self.title_font = self._load_font("arial.ttf", 72)
            self.subtitle_font = self._load_font("arial.ttf", 36)
            self.accent_font = self._load_font("arial.ttf", 48)
            
            logger.info("Fuentes cargadas exitosamente")
            
        except Exception as e:
            logger.error(f"Error cargando fuentes: {e}")
            # Usar fuentes por defecto
            self.title_font = ImageFont.load_default()
            self.subtitle_font = ImageFont.load_default()
            self.accent_font = ImageFont.load_default()
    
    def _load_font(self, font_name: str, size: int) -> ImageFont:
        """Carga una fuente específica"""
        try:
            return ImageFont.truetype(font_name, size)
        except:
            return ImageFont.load_default()
    
    def _initialize_thumbnail_styles(self):
        """Inicializa estilos de miniatura"""
        self.thumbnail_styles = {
            "cinematic": {
                "background_style": "gradient_dark",
                "text_style": "bold_white",
                "overlay_style": "dark_red",
                "accent_elements": ["film_strip", "spotlight"]
            },
            "modern": {
                "background_style": "solid_color",
                "text_style": "clean_white",
                "overlay_style": "minimal",
                "accent_elements": ["geometric_shapes"]
            },
            "vintage": {
                "background_style": "texture",
                "text_style": "serif_bold",
                "overlay_style": "sepia",
                "accent_elements": ["vintage_frame"]
            },
            "minimal": {
                "background_style": "clean",
                "text_style": "simple",
                "overlay_style": "none",
                "accent_elements": []
            }
        }
    
    def generate_thumbnail(self, script: GeneratedScript, style: str = "cinematic", 
                         format_type: str = "youtube") -> str:
        """
        Genera miniatura para el contenido
        
        Args:
            script: Guion generado
            style: Estilo de miniatura
            format_type: Tipo de formato (youtube, tiktok, instagram)
            
        Returns:
            Ruta de la miniatura generada
        """
        try:
            # Obtener especificaciones del formato
            format_specs = self._get_format_specs(format_type)
            
            # Crear diseño de miniatura
            design = self._create_thumbnail_design(script, style)
            
            # Generar imagen base
            thumbnail_image = self._create_base_image(format_specs, design)
            
            # Aplicar elementos visuales
            thumbnail_image = self._apply_visual_elements(thumbnail_image, design, format_specs)
            
            # Aplicar texto
            thumbnail_image = self._apply_text_elements(thumbnail_image, design, format_specs)
            
            # Aplicar branding
            thumbnail_image = self._apply_branding(thumbnail_image, format_specs)
            
            # Guardar miniatura
            output_path = self._save_thumbnail(thumbnail_image, script, format_type)
            
            logger.info(f"Miniatura generada: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generando miniatura: {e}")
            return self._create_fallback_thumbnail(script, format_type)
    
    def _get_format_specs(self, format_type: str) -> Dict:
        """Obtiene especificaciones del formato"""
        specs = {
            "youtube": {"width": 1280, "height": 720, "ratio": "16:9"},
            "tiktok": {"width": 1080, "height": 1920, "ratio": "9:16"},
            "instagram": {"width": 1080, "height": 1080, "ratio": "1:1"},
            "facebook": {"width": 1200, "height": 630, "ratio": "1.91:1"},
            "twitter": {"width": 1200, "height": 675, "ratio": "16:9"}
        }
        
        return specs.get(format_type, specs["youtube"])
    
    def _create_thumbnail_design(self, script: GeneratedScript, style: str) -> ThumbnailDesign:
        """Crea el diseño de la miniatura"""
        try:
            content = script.content
            
            # Título principal
            title = self._optimize_title_for_thumbnail(script.title)
            
            # Subtítulo
            subtitle = f"Análisis de {content.title}"
            
            # Imagen de fondo
            background_image = self._select_background_image(content)
            
            # Colores
            colors = self._select_colors(style, content.genres)
            
            # Elementos adicionales
            elements = self._select_accent_elements(style, content)
            
            return ThumbnailDesign(
                title=title,
                subtitle=subtitle,
                background_image=background_image,
                overlay_color=colors["overlay"],
                text_color=colors["text"],
                accent_color=colors["accent"],
                style=style,
                elements=elements
            )
            
        except Exception as e:
            logger.error(f"Error creando diseño: {e}")
            return self._create_fallback_design(script)
    
    def _optimize_title_for_thumbnail(self, title: str) -> str:
        """Optimiza el título para la miniatura"""
        try:
            # Acortar título si es muy largo
            if len(title) > 40:
                # Buscar punto de corte natural
                words = title.split()
                if len(words) > 6:
                    title = " ".join(words[:6]) + "..."
                else:
                    title = title[:37] + "..."
            
            # Añadir palabras de impacto si no las tiene
            impact_words = ["ANÁLISIS", "RESEÑA", "REACCIÓN", "SPOILERS"]
            if not any(word in title.upper() for word in impact_words):
                title = f"ANÁLISIS: {title}"
            
            return title.upper()
            
        except Exception as e:
            logger.error(f"Error optimizando título: {e}")
            return title[:40]
    
    def _select_background_image(self, content: ContentItem) -> str:
        """Selecciona imagen de fondo apropiada"""
        try:
            # Usar poster de la película/serie si está disponible
            if content.poster_url and content.poster_url.startswith("http"):
                return content.poster_url
            
            # Usar backdrop si está disponible
            if content.backdrop_url and content.backdrop_url.startswith("http"):
                return content.backdrop_url
            
            # Usar imagen genérica basada en género
            return self._get_generic_background(content.genres)
            
        except Exception as e:
            logger.error(f"Error seleccionando imagen de fondo: {e}")
            return ""
    
    def _get_generic_background(self, genres: List[str]) -> str:
        """Obtiene imagen de fondo genérica basada en géneros"""
        try:
            # Mapeo de géneros a colores de fondo
            genre_colors = {
                "Acción": "#8B0000",  # Rojo oscuro
                "Terror": "#2F2F2F",  # Gris oscuro
                "Drama": "#4B0082",   # Índigo
                "Comedia": "#FFD700",  # Dorado
                "Ciencia ficción": "#000080",  # Azul marino
                "Aventura": "#228B22",  # Verde bosque
                "Romance": "#FF69B4",  # Rosa caliente
                "Thriller": "#800080"  # Púrpura
            }
            
            # Usar el primer género disponible
            if genres:
                first_genre = genres[0]
                return genre_colors.get(first_genre, "#2F2F2F")
            
            return "#2F2F2F"  # Color por defecto
            
        except Exception as e:
            logger.error(f"Error obteniendo fondo genérico: {e}")
            return "#2F2F2F"
    
    def _select_colors(self, style: str, genres: List[str]) -> Dict[str, str]:
        """Selecciona colores para la miniatura"""
        try:
            style_config = self.thumbnail_styles.get(style, self.thumbnail_styles["cinematic"])
            
            # Colores base del branding
            base_colors = {
                "overlay": self.branding["colors"]["secondary"],
                "text": self.branding["colors"]["accent"],
                "accent": self.branding["colors"]["primary"]
            }
            
            # Ajustar colores según el estilo
            if style == "cinematic":
                base_colors["overlay"] = "#000000"  # Negro puro
                base_colors["text"] = "#FFFFFF"     # Blanco puro
            elif style == "modern":
                base_colors["overlay"] = "#1A1A1A"  # Negro suave
                base_colors["text"] = "#F0F0F0"     # Blanco suave
            elif style == "vintage":
                base_colors["overlay"] = "#2C1810"  # Marrón oscuro
                base_colors["text"] = "#F4E4BC"     # Beige
            
            return base_colors
            
        except Exception as e:
            logger.error(f"Error seleccionando colores: {e}")
            return {
                "overlay": self.branding["colors"]["secondary"],
                "text": self.branding["colors"]["accent"],
                "accent": self.branding["colors"]["primary"]
            }
    
    def _select_accent_elements(self, style: str, content: ContentItem) -> List[str]:
        """Selecciona elementos de acento para la miniatura"""
        try:
            style_config = self.thumbnail_styles.get(style, self.thumbnail_styles["cinematic"])
            elements = style_config.get("accent_elements", [])
            
            # Añadir elementos específicos del contenido
            if content.rating >= 8.0:
                elements.append("high_rating")
            if "Acción" in content.genres:
                elements.append("explosion_effect")
            if "Terror" in content.genres:
                elements.append("dark_aura")
            if "Ciencia ficción" in content.genres:
                elements.append("futuristic_elements")
            
            return elements
            
        except Exception as e:
            logger.error(f"Error seleccionando elementos: {e}")
            return []
    
    def _create_base_image(self, format_specs: Dict, design: ThumbnailDesign) -> Image.Image:
        """Crea la imagen base de la miniatura"""
        try:
            width = format_specs["width"]
            height = format_specs["height"]
            
            # Crear imagen base
            if design.background_image and design.background_image.startswith("http"):
                # Descargar imagen de fondo
                base_image = self._download_background_image(design.background_image, width, height)
            else:
                # Crear imagen sólida
                base_image = self._create_solid_background(width, height, design.overlay_color)
            
            return base_image
            
        except Exception as e:
            logger.error(f"Error creando imagen base: {e}")
            return self._create_fallback_background(format_specs)
    
    def _download_background_image(self, image_url: str, width: int, height: int) -> Image.Image:
        """Descarga y procesa imagen de fondo"""
        try:
            # Descargar imagen
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Abrir imagen
            image = Image.open(io.BytesIO(response.content))
            
            # Redimensionar manteniendo aspecto
            image = self._resize_image(image, width, height)
            
            # Aplicar filtros
            image = self._apply_background_filters(image)
            
            return image
            
        except Exception as e:
            logger.error(f"Error descargando imagen: {e}")
            return self._create_solid_background(width, height, "#2F2F2F")
    
    def _resize_image(self, image: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """Redimensiona imagen manteniendo aspecto"""
        try:
            # Calcular nuevo tamaño manteniendo aspecto
            img_ratio = image.width / image.height
            target_ratio = target_width / target_height
            
            if img_ratio > target_ratio:
                # Imagen más ancha, ajustar por altura
                new_height = target_height
                new_width = int(target_height * img_ratio)
            else:
                # Imagen más alta, ajustar por ancho
                new_width = target_width
                new_height = int(target_width / img_ratio)
            
            # Redimensionar
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Recortar al centro
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height
            
            return image.crop((left, top, right, bottom))
            
        except Exception as e:
            logger.error(f"Error redimensionando imagen: {e}")
            return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    def _apply_background_filters(self, image: Image.Image) -> Image.Image:
        """Aplica filtros a la imagen de fondo"""
        try:
            # Aumentar contraste
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            # Reducir saturación
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(0.8)
            
            # Aplicar desenfoque sutil
            image = image.filter(ImageFilter.GaussianBlur(radius=1))
            
            return image
            
        except Exception as e:
            logger.error(f"Error aplicando filtros: {e}")
            return image
    
    def _create_solid_background(self, width: int, height: int, color: str) -> Image.Image:
        """Crea fondo sólido"""
        try:
            # Convertir color hex a RGB
            rgb_color = self._hex_to_rgb(color)
            
            # Crear imagen
            image = Image.new('RGB', (width, height), rgb_color)
            
            # Aplicar gradiente si es necesario
            image = self._apply_gradient(image, color)
            
            return image
            
        except Exception as e:
            logger.error(f"Error creando fondo sólido: {e}")
            return Image.new('RGB', (width, height), (47, 47, 47))
    
    def _apply_gradient(self, image: Image.Image, base_color: str) -> Image.Image:
        """Aplica gradiente a la imagen"""
        try:
            width, height = image.size
            draw = ImageDraw.Draw(image)
            
            # Crear gradiente vertical
            rgb_color = self._hex_to_rgb(base_color)
            
            for y in range(height):
                # Calcular intensidad del gradiente
                intensity = 1.0 - (y / height) * 0.3
                
                # Ajustar color
                r = int(rgb_color[0] * intensity)
                g = int(rgb_color[1] * intensity)
                b = int(rgb_color[2] * intensity)
                
                # Dibujar línea
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            return image
            
        except Exception as e:
            logger.error(f"Error aplicando gradiente: {e}")
            return image
    
    def _apply_visual_elements(self, image: Image.Image, design: ThumbnailDesign, 
                             format_specs: Dict) -> Image.Image:
        """Aplica elementos visuales a la miniatura"""
        try:
            draw = ImageDraw.Draw(image)
            width, height = image.size
            
            # Aplicar overlay
            overlay = Image.new('RGBA', (width, height), self._hex_to_rgba(design.overlay_color, 0.6))
            image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
            
            # Aplicar elementos de acento
            for element in design.elements:
                if element == "film_strip":
                    image = self._add_film_strip(image)
                elif element == "spotlight":
                    image = self._add_spotlight_effect(image)
                elif element == "high_rating":
                    image = self._add_rating_badge(image, "8.5/10")
                elif element == "explosion_effect":
                    image = self._add_explosion_effect(image)
                elif element == "dark_aura":
                    image = self._add_dark_aura(image)
                elif element == "futuristic_elements":
                    image = self._add_futuristic_elements(image)
            
            return image
            
        except Exception as e:
            logger.error(f"Error aplicando elementos visuales: {e}")
            return image
    
    def _add_film_strip(self, image: Image.Image) -> Image.Image:
        """Añade efecto de tira de película"""
        try:
            width, height = image.size
            draw = ImageDraw.Draw(image)
            
            # Dibujar perforaciones en los bordes
            hole_size = 8
            hole_spacing = 20
            
            # Perforaciones superiores
            for x in range(0, width, hole_spacing):
                draw.ellipse([x, 5, x + hole_size, 5 + hole_size], fill=(0, 0, 0))
            
            # Perforaciones inferiores
            for x in range(0, width, hole_spacing):
                draw.ellipse([x, height - 15, x + hole_size, height - 7], fill=(0, 0, 0))
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo tira de película: {e}")
            return image
    
    def _add_spotlight_effect(self, image: Image.Image) -> Image.Image:
        """Añade efecto de reflector"""
        try:
            width, height = image.size
            
            # Crear overlay con efecto de luz
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Dibujar círculo de luz
            center_x, center_y = width // 2, height // 2
            radius = min(width, height) // 3
            
            # Crear gradiente radial
            for r in range(radius, 0, -5):
                alpha = int(100 * (1 - r / radius))
                color = (255, 255, 255, alpha)
                draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                           fill=color)
            
            # Combinar con imagen original
            image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo efecto de reflector: {e}")
            return image
    
    def _add_rating_badge(self, image: Image.Image, rating: str) -> Image.Image:
        """Añade badge de calificación"""
        try:
            width, height = image.size
            draw = ImageDraw.Draw(image)
            
            # Posición del badge (esquina superior derecha)
            badge_x = width - 120
            badge_y = 20
            
            # Dibujar fondo del badge
            draw.rectangle([badge_x, badge_y, badge_x + 100, badge_y + 40], 
                         fill=self._hex_to_rgb(self.branding["colors"]["primary"]))
            
            # Dibujar texto del rating
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            text_bbox = draw.textbbox((0, 0), rating, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = badge_x + (100 - text_width) // 2
            text_y = badge_y + 8
            
            draw.text((text_x, text_y), rating, fill=(255, 255, 255), font=font)
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo badge de rating: {e}")
            return image
    
    def _add_explosion_effect(self, image: Image.Image) -> Image.Image:
        """Añade efecto de explosión"""
        try:
            width, height = image.size
            draw = ImageDraw.Draw(image)
            
            # Dibujar líneas de explosión
            center_x, center_y = width // 2, height // 2
            
            for angle in range(0, 360, 30):
                import math
                rad = math.radians(angle)
                end_x = center_x + int(50 * math.cos(rad))
                end_y = center_y + int(50 * math.sin(rad))
                
                draw.line([(center_x, center_y), (end_x, end_y)], 
                         fill=self._hex_to_rgb("#FF4500"), width=3)
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo efecto de explosión: {e}")
            return image
    
    def _add_dark_aura(self, image: Image.Image) -> Image.Image:
        """Añade aura oscura"""
        try:
            width, height = image.size
            
            # Crear overlay oscuro
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 50))
            image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo aura oscura: {e}")
            return image
    
    def _add_futuristic_elements(self, image: Image.Image) -> Image.Image:
        """Añade elementos futuristas"""
        try:
            width, height = image.size
            draw = ImageDraw.Draw(image)
            
            # Dibujar líneas futuristas
            for i in range(0, width, 40):
                draw.line([(i, 0), (i + 20, height)], 
                         fill=self._hex_to_rgb("#00FFFF"), width=2)
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo elementos futuristas: {e}")
            return image
    
    def _apply_text_elements(self, image: Image.Image, design: ThumbnailDesign, 
                           format_specs: Dict) -> Image.Image:
        """Aplica elementos de texto a la miniatura"""
        try:
            draw = ImageDraw.Draw(image)
            width, height = image.size
            
            # Calcular posiciones de texto
            text_positions = self._calculate_text_positions(width, height, format_specs)
            
            # Título principal
            title_font = self._get_scaled_font(self.title_font, format_specs["width"])
            draw.text(text_positions["title"], design.title, 
                     fill=self._hex_to_rgb(design.text_color), font=title_font)
            
            # Subtítulo
            subtitle_font = self._get_scaled_font(self.subtitle_font, format_specs["width"])
            draw.text(text_positions["subtitle"], design.subtitle, 
                     fill=self._hex_to_rgb(design.text_color), font=subtitle_font)
            
            # Añadir sombra al texto
            image = self._add_text_shadow(image, design, text_positions)
            
            return image
            
        except Exception as e:
            logger.error(f"Error aplicando texto: {e}")
            return image
    
    def _calculate_text_positions(self, width: int, height: int, format_specs: Dict) -> Dict:
        """Calcula posiciones óptimas para el texto"""
        try:
            positions = {}
            
            # Posición del título (centro superior)
            positions["title"] = (width // 2, height // 2 - 50)
            
            # Posición del subtítulo (centro inferior)
            positions["subtitle"] = (width // 2, height // 2 + 50)
            
            # Ajustar según formato
            if format_specs["ratio"] == "9:16":  # Vertical
                positions["title"] = (width // 2, height // 2 - 30)
                positions["subtitle"] = (width // 2, height // 2 + 30)
            elif format_specs["ratio"] == "1:1":  # Cuadrado
                positions["title"] = (width // 2, height // 2 - 40)
                positions["subtitle"] = (width // 2, height // 2 + 40)
            
            return positions
            
        except Exception as e:
            logger.error(f"Error calculando posiciones: {e}")
            return {
                "title": (width // 2, height // 2 - 50),
                "subtitle": (width // 2, height // 2 + 50)
            }
    
    def _get_scaled_font(self, base_font: ImageFont, width: int) -> ImageFont:
        """Obtiene fuente escalada según el ancho"""
        try:
            # Escalar fuente basado en el ancho
            scale_factor = width / 1920  # Ancho de referencia
            new_size = int(72 * scale_factor)
            
            return ImageFont.truetype("arial.ttf", new_size)
            
        except Exception as e:
            logger.error(f"Error escalando fuente: {e}")
            return base_font
    
    def _add_text_shadow(self, image: Image.Image, design: ThumbnailDesign, 
                        positions: Dict) -> Image.Image:
        """Añade sombra al texto"""
        try:
            draw = ImageDraw.Draw(image)
            
            # Sombra del título
            title_font = self._get_scaled_font(self.title_font, image.width)
            shadow_pos = (positions["title"][0] + 2, positions["title"][1] + 2)
            draw.text(shadow_pos, design.title, fill=(0, 0, 0), font=title_font)
            
            # Sombra del subtítulo
            subtitle_font = self._get_scaled_font(self.subtitle_font, image.width)
            shadow_pos = (positions["subtitle"][0] + 2, positions["subtitle"][1] + 2)
            draw.text(shadow_pos, design.subtitle, fill=(0, 0, 0), font=subtitle_font)
            
            return image
            
        except Exception as e:
            logger.error(f"Error añadiendo sombra: {e}")
            return image
    
    def _apply_branding(self, image: Image.Image, format_specs: Dict) -> Image.Image:
        """Aplica branding de Cine Norte"""
        try:
            draw = ImageDraw.Draw(image)
            width, height = image.size
            
            # Logo Cine Norte (esquina inferior izquierda)
            logo_text = "CINE NORTE"
            logo_font = self._get_scaled_font(self.accent_font, width)
            
            # Posición del logo
            logo_x = 20
            logo_y = height - 60
            
            # Sombra del logo
            draw.text((logo_x + 2, logo_y + 2), logo_text, fill=(0, 0, 0), font=logo_font)
            
            # Logo principal
            draw.text((logo_x, logo_y), logo_text, 
                     fill=self._hex_to_rgb(self.branding["colors"]["accent"]), font=logo_font)
            
            return image
            
        except Exception as e:
            logger.error(f"Error aplicando branding: {e}")
            return image
    
    def _save_thumbnail(self, image: Image.Image, script: GeneratedScript, 
                       format_type: str) -> str:
        """Guarda la miniatura generada"""
        try:
            # Crear directorio de salida
            output_dir = Path("output/thumbnails")
            output_dir.mkdir(exist_ok=True)
            
            # Generar nombre de archivo
            safe_title = self._sanitize_filename(script.content.title)
            filename = f"thumbnail_{safe_title}_{format_type}.png"
            output_path = output_dir / filename
            
            # Guardar imagen
            image.save(output_path, "PNG", optimize=True)
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error guardando miniatura: {e}")
            return ""
    
    def generate_seo_data(self, script: GeneratedScript) -> SEOData:
        """Genera datos SEO optimizados"""
        try:
            # Título optimizado
            title = self._optimize_title_for_seo(script.title)
            
            # Descripción optimizada
            description = self._optimize_description_for_seo(script.description)
            
            # Keywords
            keywords = self._extract_keywords(script)
            
            # Hashtags
            hashtags = script.hashtags
            
            # Tags adicionales
            tags = self._generate_tags(script)
            
            # Categoría
            category = self._determine_category(script.content)
            
            return SEOData(
                title=title,
                description=description,
                keywords=keywords,
                hashtags=hashtags,
                tags=tags,
                category=category,
                language="es"
            )
            
        except Exception as e:
            logger.error(f"Error generando datos SEO: {e}")
            return self._create_fallback_seo_data(script)
    
    def _optimize_title_for_seo(self, title: str) -> str:
        """Optimiza el título para SEO"""
        try:
            # Asegurar longitud óptima
            if len(title) < 50:
                title += " - Análisis Cinematográfico"
            elif len(title) > 60:
                title = title[:57] + "..."
            
            # Añadir palabras clave si no están
            if "análisis" not in title.lower():
                title = f"Análisis: {title}"
            
            return title
            
        except Exception as e:
            logger.error(f"Error optimizando título SEO: {e}")
            return title
    
    def _optimize_description_for_seo(self, description: str) -> str:
        """Optimiza la descripción para SEO"""
        try:
            # Asegurar longitud óptima
            if len(description) < 150:
                description += " ¡Suscríbete para más análisis cinematográficos!"
            elif len(description) > 160:
                description = description[:157] + "..."
            
            # Añadir call-to-action
            if "suscríbete" not in description.lower():
                description += " ¡No olvides suscribirte y dar like!"
            
            return description
            
        except Exception as e:
            logger.error(f"Error optimizando descripción SEO: {e}")
            return description
    
    def _extract_keywords(self, script: GeneratedScript) -> List[str]:
        """Extrae keywords del contenido"""
        try:
            keywords = []
            
            # Keywords del contenido
            content = script.content
            keywords.extend(content.genres)
            keywords.append(content.content_type)
            
            # Keywords del título
            title_words = script.title.lower().split()
            keywords.extend([word for word in title_words if len(word) > 3])
            
            # Keywords trending
            trending_keywords = ["streaming", "netflix", "disney", "hbo", "análisis", "reseña"]
            keywords.extend(trending_keywords)
            
            # Remover duplicados y limitar
            keywords = list(set(keywords))[:20]
            
            return keywords
            
        except Exception as e:
            logger.error(f"Error extrayendo keywords: {e}")
            return ["cine", "película", "análisis"]
    
    def _generate_tags(self, script: GeneratedScript) -> List[str]:
        """Genera tags adicionales"""
        try:
            tags = []
            
            # Tags por género
            for genre in script.content.genres:
                tags.append(f"#{genre.replace(' ', '')}")
            
            # Tags por plataforma
            for platform in script.content.platforms:
                tags.append(f"#{platform.replace(' ', '').replace('+', 'Plus')}")
            
            # Tags generales
            general_tags = ["#CineNorte", "#AnálisisCinematográfico", "#Entretenimiento"]
            tags.extend(general_tags)
            
            return tags[:15]  # Máximo 15 tags
            
        except Exception as e:
            logger.error(f"Error generando tags: {e}")
            return ["#CineNorte", "#Análisis"]
    
    def _determine_category(self, content: ContentItem) -> str:
        """Determina la categoría del contenido"""
        try:
            if content.content_type == "movie":
                return "Películas"
            else:
                return "Series"
                
        except Exception as e:
            logger.error(f"Error determinando categoría: {e}")
            return "Entretenimiento"
    
    def _create_fallback_design(self, script: GeneratedScript) -> ThumbnailDesign:
        """Crea diseño de respaldo"""
        return ThumbnailDesign(
            title=script.title[:40],
            subtitle="Análisis Cinematográfico",
            background_image="",
            overlay_color=self.branding["colors"]["secondary"],
            text_color=self.branding["colors"]["accent"],
            accent_color=self.branding["colors"]["primary"],
            style="cinematic",
            elements=[]
        )
    
    def _create_fallback_thumbnail(self, script: GeneratedScript, format_type: str) -> str:
        """Crea miniatura de respaldo"""
        try:
            format_specs = self._get_format_specs(format_type)
            design = self._create_fallback_design(script)
            
            image = self._create_solid_background(
                format_specs["width"], 
                format_specs["height"], 
                design.overlay_color
            )
            
            return self._save_thumbnail(image, script, format_type)
            
        except Exception as e:
            logger.error(f"Error creando miniatura de respaldo: {e}")
            return ""
    
    def _create_fallback_seo_data(self, script: GeneratedScript) -> SEOData:
        """Crea datos SEO de respaldo"""
        return SEOData(
            title=script.title,
            description=script.description,
            keywords=["cine", "película", "análisis"],
            hashtags=script.hashtags,
            tags=["#CineNorte"],
            category="Entretenimiento",
            language="es"
        )
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convierte color hex a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _hex_to_rgba(self, hex_color: str, alpha: float) -> Tuple[int, int, int, int]:
        """Convierte color hex a RGBA"""
        rgb = self._hex_to_rgb(hex_color)
        return (*rgb, int(255 * alpha))
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza nombre de archivo"""
        import re
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        return filename[:50]
    
    def _create_fallback_background(self, format_specs: Dict) -> Image.Image:
        """Crea fondo de respaldo"""
        return Image.new('RGB', (format_specs["width"], format_specs["height"]), (47, 47, 47))
