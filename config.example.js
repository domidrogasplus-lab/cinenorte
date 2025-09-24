/**
 * Archivo de Configuración de Ejemplo para Cine Norte
 * Copia este archivo como config.local.js y personaliza los valores
 */

// Configuración de APIs
const API_CONFIG = {
    // OpenAI API - Requerida para generación de guiones
    OPENAI_API_KEY: 'tu_clave_openai_aqui',
    
    // TMDB API - Recomendada para análisis de contenido
    TMDB_API_KEY: 'tu_clave_tmdb_aqui',
    
    // Hugging Face API - Opcional para análisis avanzado
    HUGGINGFACE_API_KEY: 'tu_clave_huggingface_aqui'
};

// Configuración de la aplicación
const APP_CONFIG = {
    // Configuración de video
    VIDEO: {
        MAX_DURATION: 180, // segundos
        DEFAULT_QUALITY: '1080p',
        DEFAULT_FPS: 24
    },
    
    // Configuración de audio
    AUDIO: {
        SAMPLE_RATE: 44100,
        DEFAULT_BITRATE: '192k',
        DEFAULT_VOICE: 'male'
    },
    
    // Configuración de guiones
    SCRIPT: {
        MAX_WORDS: 500,
        MIN_WORDS: 100,
        DEFAULT_DURATION: 120 // segundos
    },
    
    // Configuración de UI
    UI: {
        ANIMATIONS: true,
        NOTIFICATIONS: true,
        AUTO_SAVE: true,
        THEME: 'dark'
    }
};

// Configuración de branding Cine Norte
const BRANDING_CONFIG = {
    COLORS: {
        PRIMARY_RED: '#E50914',
        DEEP_BLACK: '#0A0A0A',
        METALLIC_SILVER: '#C0C0C0',
        WHITE: '#FFFFFF',
        GOLD: '#FFD700'
    },
    
    LOGO: {
        TEXT: 'CINE NORTE',
        FONT: 'Arial, sans-serif',
        SIZE: '48px'
    },
    
    TAGLINE: 'Generador Automatizado de Contenido Audiovisual'
};

// Configuración de formatos de salida
const FORMATS_CONFIG = {
    YOUTUBE: {
        WIDTH: 1920,
        HEIGHT: 1080,
        ASPECT_RATIO: '16:9',
        MAX_DURATION: 180
    },
    
    TIKTOK: {
        WIDTH: 1080,
        HEIGHT: 1920,
        ASPECT_RATIO: '9:16',
        MAX_DURATION: 60
    },
    
    INSTAGRAM: {
        WIDTH: 1080,
        HEIGHT: 1080,
        ASPECT_RATIO: '1:1',
        MAX_DURATION: 60
    }
};

// Configuración de optimización
const OPTIMIZATION_CONFIG = {
    WEIGHTS: {
        CONTENT: 0.25,
        ENGAGEMENT: 0.25,
        VIRAL: 0.20,
        SEO: 0.15,
        VISUAL: 0.10,
        AUDIO: 0.05
    },
    
    THRESHOLDS: {
        EXCELLENT: 80,
        GOOD: 60,
        FAIR: 40,
        POOR: 20
    }
};

// Exportar configuración
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        API_CONFIG,
        APP_CONFIG,
        BRANDING_CONFIG,
        FORMATS_CONFIG,
        OPTIMIZATION_CONFIG
    };
} else {
    window.CONFIG_EXAMPLE = {
        API_CONFIG,
        APP_CONFIG,
        BRANDING_CONFIG,
        FORMATS_CONFIG,
        OPTIMIZATION_CONFIG
    };
}
