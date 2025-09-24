/**
 * Configuración de Cine Norte
 * Maneja la configuración global de la aplicación
 */

class CineNorteConfig {
    constructor() {
        this.config = {
            // Colores de marca
            colors: {
                primaryRed: '#E50914',
                deepBlack: '#0A0A0A',
                metallicSilver: '#C0C0C0',
                darkGray: '#1A1A1A',
                lightGray: '#2A2A2A',
                white: '#FFFFFF',
                gold: '#FFD700'
            },
            
            // APIs
            apis: {
                openai: {
                    baseUrl: 'https://api.openai.com/v1',
                    key: localStorage.getItem('openai_key') || '',
                    model: 'gpt-4'
                },
                tmdb: {
                    baseUrl: 'https://api.themoviedb.org/3',
                    key: localStorage.getItem('tmdb_key') || '',
                    imageBaseUrl: 'https://image.tmdb.org/t/p'
                },
                huggingface: {
                    baseUrl: 'https://api-inference.huggingface.co/models',
                    key: localStorage.getItem('huggingface_key') || ''
                }
            },
            
            // Configuración de video
            video: {
                maxDuration: 180, // segundos
                quality: '1080p',
                formats: {
                    youtube: { width: 1920, height: 1080, aspectRatio: '16:9' },
                    tiktok: { width: 1080, height: 1920, aspectRatio: '9:16' },
                    instagram: { width: 1080, height: 1080, aspectRatio: '1:1' },
                    facebook: { width: 1920, height: 1080, aspectRatio: '16:9' },
                    twitter: { width: 1280, height: 720, aspectRatio: '16:9' }
                }
            },
            
            // Configuración de audio
            audio: {
                sampleRate: 44100,
                bitrate: '192k',
                voices: {
                    male: { name: 'Masculino', lang: 'es-ES', pitch: 0.8, rate: 0.9 },
                    female: { name: 'Femenino', lang: 'es-ES', pitch: 1.1, rate: 0.95 },
                    dramatic: { name: 'Dramático', lang: 'es-ES', pitch: 0.7, rate: 0.8 },
                    energetic: { name: 'Energético', lang: 'es-ES', pitch: 1.2, rate: 1.1 }
                }
            },
            
            // Configuración de guiones
            script: {
                maxWords: 500,
                minWords: 100,
                sections: ['intro', 'hook', 'plot', 'analysis', 'outro'],
                templates: {
                    intro: '¡Hola cinéfilos! Bienvenidos a Cine Norte, donde exploramos las mejores historias del entretenimiento.',
                    outro: '¿Qué opinas de esta película? Déjanos tu comentario y no olvides suscribirte para más contenido como este.',
                    spoilerWarning: '⚠️ Contiene spoilers menores ⚠️'
                }
            },
            
            // Hashtags base
            hashtags: [
                '#CineNorte', '#Películas', '#Series', '#Netflix', '#AmazonPrime',
                '#DisneyPlus', '#HBOMax', '#Paramount', '#AppleTV', '#MagisTV',
                '#Streaming', '#Entretenimiento', '#Cine', '#Análisis'
            ],
            
            // Configuración de UI
            ui: {
                animations: true,
                notifications: true,
                autoSave: true,
                theme: 'dark'
            }
        };
        
        this.loadSettings();
    }
    
    /**
     * Carga la configuración desde localStorage
     */
    loadSettings() {
        const savedConfig = localStorage.getItem('cine_norte_config');
        if (savedConfig) {
            try {
                const parsed = JSON.parse(savedConfig);
                this.config = { ...this.config, ...parsed };
            } catch (error) {
                console.warn('Error cargando configuración:', error);
            }
        }
    }
    
    /**
     * Guarda la configuración en localStorage
     */
    saveSettings() {
        try {
            localStorage.setItem('cine_norte_config', JSON.stringify(this.config));
            return true;
        } catch (error) {
            console.error('Error guardando configuración:', error);
            return false;
        }
    }
    
    /**
     * Obtiene un valor de configuración
     * @param {string} path - Ruta del valor (ej: 'apis.openai.key')
     * @returns {any} Valor de configuración
     */
    get(path) {
        return path.split('.').reduce((obj, key) => obj?.[key], this.config);
    }
    
    /**
     * Establece un valor de configuración
     * @param {string} path - Ruta del valor
     * @param {any} value - Nuevo valor
     */
    set(path, value) {
        const keys = path.split('.');
        const lastKey = keys.pop();
        const target = keys.reduce((obj, key) => {
            if (!obj[key]) obj[key] = {};
            return obj[key];
        }, this.config);
        target[lastKey] = value;
    }
    
    /**
     * Actualiza la configuración de APIs
     * @param {Object} apiConfig - Configuración de APIs
     */
    updateAPIs(apiConfig) {
        Object.keys(apiConfig).forEach(api => {
            if (this.config.apis[api]) {
                this.config.apis[api] = { ...this.config.apis[api], ...apiConfig[api] };
            }
        });
        this.saveSettings();
    }
    
    /**
     * Verifica si las APIs están configuradas
     * @returns {Object} Estado de las APIs
     */
    checkAPIs() {
        return {
            openai: !!this.config.apis.openai.key,
            tmdb: !!this.config.apis.tmdb.key,
            huggingface: !!this.config.apis.huggingface.key
        };
    }
    
    /**
     * Obtiene la configuración de formato de video
     * @param {string} platform - Plataforma objetivo
     * @returns {Object} Configuración del formato
     */
    getVideoFormat(platform) {
        return this.config.video.formats[platform] || this.config.video.formats.youtube;
    }
    
    /**
     * Obtiene la configuración de voz
     * @param {string} voiceType - Tipo de voz
     * @returns {Object} Configuración de voz
     */
    getVoiceConfig(voiceType) {
        return this.config.audio.voices[voiceType] || this.config.audio.voices.male;
    }
    
    /**
     * Genera hashtags personalizados
     * @param {Object} content - Información del contenido
     * @param {string} platform - Plataforma objetivo
     * @returns {Array} Lista de hashtags
     */
    generateHashtags(content, platform) {
        let hashtags = [...this.config.hashtags];
        
        // Agregar hashtags específicos del contenido
        if (content.title) {
            hashtags.push(`#${content.title.replace(/\s+/g, '')}`);
        }
        if (content.platform) {
            hashtags.push(`#${content.platform.replace(/\s+/g, '')}`);
        }
        if (content.content_type) {
            hashtags.push(`#${content.content_type.toUpperCase()}`);
        }
        
        // Agregar hashtags por género
        if (content.genre && Array.isArray(content.genre)) {
            content.genre.slice(0, 3).forEach(genre => {
                hashtags.push(`#${genre.replace(/\s+/g, '')}`);
            });
        }
        
        // Hashtags específicos por plataforma
        const platformHashtags = {
            youtube: ['#YouTube', '#CineNorte', '#AnálisisCinematográfico'],
            tiktok: ['#TikTok', '#FYP', '#CineTok', '#Viral'],
            instagram: ['#Instagram', '#Reels', '#CineNorte', '#Stories'],
            facebook: ['#Facebook', '#Video', '#CineNorte'],
            twitter: ['#Twitter', '#Tweet', '#CineNorte']
        };
        
        if (platformHashtags[platform]) {
            hashtags.push(...platformHashtags[platform]);
        }
        
        return [...new Set(hashtags)].slice(0, 15); // Máximo 15 hashtags únicos
    }
    
    /**
     * Obtiene el template de guion según el tipo
     * @param {string} type - Tipo de sección
     * @returns {string} Template
     */
    getScriptTemplate(type) {
        return this.config.script.templates[type] || '';
    }
    
    /**
     * Valida la configuración
     * @returns {Object} Resultado de validación
     */
    validate() {
        const errors = [];
        const warnings = [];
        
        // Validar APIs requeridas
        if (!this.config.apis.openai.key) {
            errors.push('OpenAI API key es requerida para generar guiones');
        }
        
        if (!this.config.apis.tmdb.key) {
            warnings.push('TMDB API key es recomendada para análisis de contenido');
        }
        
        // Validar configuración de video
        if (this.config.video.maxDuration < 30 || this.config.video.maxDuration > 300) {
            warnings.push('Duración de video debe estar entre 30 y 300 segundos');
        }
        
        return {
            valid: errors.length === 0,
            errors,
            warnings
        };
    }
    
    /**
     * Resetea la configuración a valores por defecto
     */
    reset() {
        localStorage.removeItem('cine_norte_config');
        this.loadSettings();
    }
    
    /**
     * Exporta la configuración
     * @returns {string} Configuración en JSON
     */
    export() {
        return JSON.stringify(this.config, null, 2);
    }
    
    /**
     * Importa la configuración
     * @param {string} configJson - Configuración en JSON
     * @returns {boolean} Éxito de la importación
     */
    import(configJson) {
        try {
            const imported = JSON.parse(configJson);
            this.config = { ...this.config, ...imported };
            this.saveSettings();
            return true;
        } catch (error) {
            console.error('Error importando configuración:', error);
            return false;
        }
    }
}

// Instancia global de configuración
window.CineNorteConfig = CineNorteConfig;
window.config = new CineNorteConfig();
