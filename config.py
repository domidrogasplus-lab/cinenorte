"""
Configuración principal del sistema Cine Norte
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class CineNorteConfig:
    """Configuración de marca Cine Norte"""
    
    # Colores de marca
    PRIMARY_RED = "#E50914"
    DEEP_BLACK = "#0A0A0A"
    METALLIC_SILVER = "#C0C0C0"
    
    # Configuración de video
    VIDEO_DURATION_MAX = 180  # 3 minutos en segundos
    VIDEO_QUALITY = "1080p"
    
    # Formatos de salida
    FORMATS = {
        "youtube": (1920, 1080),  # 16:9
        "tiktok": (1080, 1920),   # 9:16
        "instagram": (1080, 1080) # 1:1
    }
    
    # Configuración de audio
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_BITRATE = "192k"
    
    # Configuración de IA
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # APIs de streaming
    TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
    
    # Configuración de redes sociales
    HASHTAGS_BASE = [
        "#CineNorte", "#Películas", "#Series", "#Netflix", "#AmazonPrime", 
        "#DisneyPlus", "#HBOMax", "#Paramount", "#AppleTV", "#MagisTV"
    ]
    
    # Configuración de guiones
    SCRIPT_TEMPLATES = {
        "intro": "¡Hola cinéfilos! Bienvenidos a Cine Norte, donde exploramos las mejores historias del entretenimiento.",
        "outro": "¿Qué opinas de esta película? Déjanos tu comentario y no olvides suscribirte para más contenido como este.",
        "spoiler_warning": "⚠️ Contiene spoilers menores ⚠️"
    }
    
    # Configuración de fuentes
    FONTS = {
        "title": "Arial Black",
        "subtitle": "Arial",
        "body": "Arial"
    }
    
    # Configuración de música
    MUSIC_GENRES = {
        "action": "epic_action.mp3",
        "drama": "emotional_drama.mp3", 
        "comedy": "light_comedy.mp3",
        "horror": "tense_horror.mp3",
        "sci_fi": "futuristic_sci_fi.mp3"
    }

# Instancia global de configuración
config = CineNorteConfig()
