"""
Configuración principal del sistema Cine Norte
"""

import os
from pathlib import Path

# Directorios del proyecto
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"

# Crear directorios si no existen
for directory in [DATA_DIR, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuración de branding Cine Norte
BRANDING = {
    "name": "Cine Norte",
    "colors": {
        "primary": "#E50914",      # Rojo Netflix
        "secondary": "#0A0A0A",    # Negro profundo
        "accent": "#C0C0C0"        # Plateado metálico
    },
    "fonts": {
        "primary": "Arial Black",
        "secondary": "Helvetica Neue"
    }
}

# Configuración de video
VIDEO_CONFIG = {
    "formats": {
        "youtube": {"width": 1920, "height": 1080, "ratio": "16:9"},
        "tiktok": {"width": 1080, "height": 1920, "ratio": "9:16"},
        "instagram": {"width": 1080, "height": 1080, "ratio": "1:1"}
    },
    "max_duration": 180,  # 3 minutos en segundos
    "fps": 30,
    "bitrate": "5000k"
}

# Configuración de audio
AUDIO_CONFIG = {
    "sample_rate": 44100,
    "channels": 2,
    "bitrate": "192k",
    "voice_settings": {
        "language": "es",
        "speed": 1.0,
        "pitch": 0
    }
}

# APIs y servicios externos
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "tmdb": os.getenv("TMDB_API_KEY", ""),
    "youtube": os.getenv("YOUTUBE_API_KEY", ""),
    "elevenlabs": os.getenv("ELEVENLABS_API_KEY", "")
}

# Configuración de plataformas de streaming
STREAMING_PLATFORMS = [
    "Netflix", "Amazon Prime", "Disney+", "HBO Max", 
    "Paramount+", "Apple TV+", "MagisTV", "Star+", 
    "Crunchyroll", "Hulu", "Peacock"
]

# Configuración de generación de contenido
CONTENT_CONFIG = {
    "max_script_length": 500,  # palabras
    "min_script_length": 100,
    "thumbnail_style": "cinematic",
    "auto_subtitles": True,
    "background_music": True,
    "intro_duration": 3,  # segundos
    "outro_duration": 3
}

# Configuración de SEO
SEO_CONFIG = {
    "max_hashtags": 10,
    "title_max_length": 60,
    "description_max_length": 160,
    "keywords": [
        "cine", "películas", "series", "netflix", "streaming",
        "resumen", "análisis", "cine norte", "entretenimiento"
    ]
}
