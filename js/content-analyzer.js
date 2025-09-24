/**
 * Analizador de Contenido para Cine Norte
 * Conecta con APIs de streaming y analiza películas/series populares
 */

class ContentAnalyzer {
    constructor() {
        this.tmdbBaseUrl = 'https://api.themoviedb.org/3';
        this.omdbBaseUrl = 'https://www.omdbapi.com';
        this.cache = new Map();
        this.cacheExpiry = 30 * 60 * 1000; // 30 minutos
    }
    
    /**
     * Busca contenido en TMDB
     * @param {string} query - Término de búsqueda
     * @param {string} type - Tipo de contenido (movie, tv, all)
     * @returns {Promise<Array>} Lista de contenidos encontrados
     */
    async searchContent(query, type = 'all') {
        try {
            const apiKey = config.get('apis.tmdb.key');
            if (!apiKey) {
                throw new Error('TMDB API key no configurada');
            }
            
            const results = [];
            
            if (type === 'all' || type === 'movie') {
                const movies = await this._searchMovies(query, apiKey);
                results.push(...movies);
            }
            
            if (type === 'all' || type === 'tv') {
                const tvShows = await this._searchTVShows(query, apiKey);
                results.push(...tvShows);
            }
            
            // Ordenar por popularidad
            results.sort((a, b) => b.popularity - a.popularity);
            
            return results.slice(0, 20); // Máximo 20 resultados
            
        } catch (error) {
            console.error('Error buscando contenido:', error);
            throw error;
        }
    }
    
    /**
     * Busca películas específicas
     * @param {string} query - Término de búsqueda
     * @param {string} apiKey - Clave de API
     * @returns {Promise<Array>} Lista de películas
     */
    async _searchMovies(query, apiKey) {
        const url = `${this.tmdbBaseUrl}/search/movie`;
        const params = new URLSearchParams({
            api_key: apiKey,
            query: query,
            language: 'es-ES',
            region: 'MX'
        });
        
        const response = await fetch(`${url}?${params}`);
        if (!response.ok) {
            throw new Error(`Error TMDB: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results.map(item => this._parseContent(item, 'movie'));
    }
    
    /**
     * Busca series de TV específicas
     * @param {string} query - Término de búsqueda
     * @param {string} apiKey - Clave de API
     * @returns {Promise<Array>} Lista de series
     */
    async _searchTVShows(query, apiKey) {
        const url = `${this.tmdbBaseUrl}/search/tv`;
        const params = new URLSearchParams({
            api_key: apiKey,
            query: query,
            language: 'es-ES',
            region: 'MX'
        });
        
        const response = await fetch(`${url}?${params}`);
        if (!response.ok) {
            throw new Error(`Error TMDB: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results.map(item => this._parseContent(item, 'tv'));
    }
    
    /**
     * Obtiene contenido trending
     * @param {string} timeWindow - Ventana de tiempo (day, week)
     * @param {string} type - Tipo de contenido (movie, tv, all)
     * @returns {Promise<Array>} Lista de contenido trending
     */
    async getTrendingContent(timeWindow = 'week', type = 'all') {
        try {
            const apiKey = config.get('apis.tmdb.key');
            if (!apiKey) {
                throw new Error('TMDB API key no configurada');
            }
            
            const results = [];
            
            if (type === 'all' || type === 'movie') {
                const movies = await this._getTrendingMovies(timeWindow, apiKey);
                results.push(...movies);
            }
            
            if (type === 'all' || type === 'tv') {
                const tvShows = await this._getTrendingTVShows(timeWindow, apiKey);
                results.push(...tvShows);
            }
            
            // Ordenar por popularidad
            results.sort((a, b) => b.popularity - a.popularity);
            
            return results.slice(0, 20);
            
        } catch (error) {
            console.error('Error obteniendo contenido trending:', error);
            throw error;
        }
    }
    
    /**
     * Obtiene películas trending
     * @param {string} timeWindow - Ventana de tiempo
     * @param {string} apiKey - Clave de API
     * @returns {Promise<Array>} Lista de películas trending
     */
    async _getTrendingMovies(timeWindow, apiKey) {
        const url = `${this.tmdbBaseUrl}/trending/movie/${timeWindow}`;
        const params = new URLSearchParams({
            api_key: apiKey,
            language: 'es-ES',
            region: 'MX'
        });
        
        const response = await fetch(`${url}?${params}`);
        if (!response.ok) {
            throw new Error(`Error TMDB: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results.map(item => this._parseContent(item, 'movie'));
    }
    
    /**
     * Obtiene series trending
     * @param {string} timeWindow - Ventana de tiempo
     * @param {string} apiKey - Clave de API
     * @returns {Promise<Array>} Lista de series trending
     */
    async _getTrendingTVShows(timeWindow, apiKey) {
        const url = `${this.tmdbBaseUrl}/trending/tv/${timeWindow}`;
        const params = new URLSearchParams({
            api_key: apiKey,
            language: 'es-ES',
            region: 'MX'
        });
        
        const response = await fetch(`${url}?${params}`);
        if (!response.ok) {
            throw new Error(`Error TMDB: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results.map(item => this._parseContent(item, 'tv'));
    }
    
    /**
     * Obtiene detalles adicionales del contenido
     * @param {number} contentId - ID del contenido
     * @param {string} type - Tipo de contenido (movie, tv)
     * @returns {Promise<Object>} Detalles del contenido
     */
    async getContentDetails(contentId, type) {
        try {
            const apiKey = config.get('apis.tmdb.key');
            if (!apiKey) {
                throw new Error('TMDB API key no configurada');
            }
            
            const cacheKey = `details_${type}_${contentId}`;
            const cached = this._getFromCache(cacheKey);
            if (cached) {
                return cached;
            }
            
            const url = `${this.tmdbBaseUrl}/${type}/${contentId}`;
            const params = new URLSearchParams({
                api_key: apiKey,
                language: 'es-ES',
                append_to_response: 'credits,keywords,videos'
            });
            
            const response = await fetch(`${url}?${params}`);
            if (!response.ok) {
                throw new Error(`Error TMDB: ${response.status}`);
            }
            
            const data = await response.json();
            const details = this._parseContentDetails(data, type);
            
            this._setCache(cacheKey, details);
            return details;
            
        } catch (error) {
            console.error('Error obteniendo detalles:', error);
            throw error;
        }
    }
    
    /**
     * Parsea contenido de TMDB
     * @param {Object} item - Item de TMDB
     * @param {string} type - Tipo de contenido
     * @returns {Object} Contenido parseado
     */
    _parseContent(item, type) {
        return {
            id: item.id,
            title: item.title || item.name,
            original_title: item.original_title || item.original_name,
            overview: item.overview || '',
            release_date: item.release_date || item.first_air_date || '',
            genre: this._getGenreNames(item.genre_ids || []),
            rating: item.vote_average || 0,
            popularity: item.popularity || 0,
            poster_url: item.poster_path ? 
                `https://image.tmdb.org/t/p/w500${item.poster_path}` : '',
            backdrop_url: item.backdrop_path ? 
                `https://image.tmdb.org/t/p/w1280${item.backdrop_path}` : '',
            content_type: type,
            platform: this._detectPlatform(item),
            language: item.original_language || 'es',
            adult: item.adult || false
        };
    }
    
    /**
     * Parsea detalles del contenido
     * @param {Object} data - Datos de TMDB
     * @param {string} type - Tipo de contenido
     * @returns {Object} Detalles parseados
     */
    _parseContentDetails(data, type) {
        const details = {
            runtime: data.runtime || null,
            cast: [],
            director: [],
            keywords: [],
            production_countries: [],
            trailer_url: null
        };
        
        // Procesar cast
        if (data.credits && data.credits.cast) {
            details.cast = data.credits.cast.slice(0, 10).map(actor => actor.name);
        }
        
        // Procesar director
        if (data.credits && data.credits.crew) {
            details.director = data.credits.crew
                .filter(crew => crew.job === 'Director')
                .map(crew => crew.name);
        }
        
        // Procesar keywords
        if (data.keywords && data.keywords.keywords) {
            details.keywords = data.keywords.keywords.slice(0, 10).map(kw => kw.name);
        }
        
        // Procesar países de producción
        if (data.production_countries) {
            details.production_countries = data.production_countries.map(country => country.name);
        }
        
        // Buscar tráiler
        if (data.videos && data.videos.results) {
            const trailer = data.videos.results.find(video => 
                video.type === 'Trailer' && video.site === 'YouTube'
            );
            if (trailer) {
                details.trailer_url = `https://www.youtube.com/watch?v=${trailer.key}`;
            }
        }
        
        return details;
    }
    
    /**
     * Convierte IDs de género a nombres
     * @param {Array} genreIds - IDs de género
     * @returns {Array} Nombres de género
     */
    _getGenreNames(genreIds) {
        const genreMap = {
            28: 'Acción', 12: 'Aventura', 16: 'Animación', 35: 'Comedia',
            80: 'Crimen', 99: 'Documental', 18: 'Drama', 10751: 'Familia',
            14: 'Fantasía', 36: 'Historia', 27: 'Terror', 10402: 'Música',
            9648: 'Misterio', 10749: 'Romance', 878: 'Ciencia Ficción',
            10770: 'Película de TV', 53: 'Suspenso', 10752: 'Guerra', 37: 'Western'
        };
        
        return genreIds.map(id => genreMap[id] || 'Desconocido');
    }
    
    /**
     * Detecta la plataforma de streaming
     * @param {Object} item - Item de contenido
     * @returns {string} Plataforma detectada
     */
    _detectPlatform(item) {
        const title = (item.title || item.name || '').toLowerCase();
        
        // Detección básica por palabras clave
        if (title.includes('stranger things') || title.includes('the crown') || 
            title.includes('netflix')) {
            return 'Netflix';
        }
        
        if (title.includes('the boys') || title.includes('amazon') || 
            title.includes('prime')) {
            return 'Amazon Prime';
        }
        
        if (title.includes('marvel') || title.includes('star wars') || 
            title.includes('disney')) {
            return 'Disney+';
        }
        
        if (title.includes('game of thrones') || title.includes('hbo') || 
            title.includes('max')) {
            return 'HBO Max';
        }
        
        return 'Múltiples plataformas';
    }
    
    /**
     * Analiza la viabilidad del contenido para crear videos
     * @param {Object} content - Información del contenido
     * @returns {Object} Análisis de viabilidad
     */
    analyzeContentViability(content) {
        let score = 0;
        const factors = {};
        
        // Factor de popularidad (0-30 puntos)
        const popularityScore = Math.min(content.popularity / 100, 1) * 30;
        score += popularityScore;
        factors.popularity = popularityScore;
        
        // Factor de rating (0-25 puntos)
        const ratingScore = (content.rating / 10) * 25;
        score += ratingScore;
        factors.rating = ratingScore;
        
        // Factor de disponibilidad de tráiler (0-20 puntos)
        const trailerScore = content.trailer_url ? 20 : 0;
        score += trailerScore;
        factors.trailer_available = trailerScore;
        
        // Factor de calidad de descripción (0-15 puntos)
        const overviewScore = Math.min(content.overview.length / 200, 1) * 15;
        score += overviewScore;
        factors.overview_quality = overviewScore;
        
        // Factor de género (0-10 puntos)
        const highImpactGenres = ['Acción', 'Ciencia Ficción', 'Terror', 'Suspenso', 'Aventura'];
        const genreScore = content.genre.some(genre => 
            highImpactGenres.includes(genre)) ? 10 : 5;
        score += genreScore;
        factors.genre_impact = genreScore;
        
        // Clasificación final
        let viability;
        if (score >= 80) {
            viability = 'Excelente';
        } else if (score >= 60) {
            viability = 'Buena';
        } else if (score >= 40) {
            viability = 'Regular';
        } else {
            viability = 'Baja';
        }
        
        return {
            total_score: Math.round(score * 100) / 100,
            viability,
            factors,
            recommendations: this._getRecommendations(score, content)
        };
    }
    
    /**
     * Genera recomendaciones basadas en el análisis
     * @param {number} score - Score del análisis
     * @param {Object} content - Información del contenido
     * @returns {Array} Lista de recomendaciones
     */
    _getRecommendations(score, content) {
        const recommendations = [];
        
        if (score < 40) {
            recommendations.push('Considera buscar contenido más popular o reciente');
        }
        
        if (!content.trailer_url) {
            recommendations.push('Busca tráileres alternativos o clips oficiales');
        }
        
        if (content.overview.length < 100) {
            recommendations.push('Investiga más detalles de la trama');
        }
        
        const highImpactGenres = ['Acción', 'Ciencia Ficción', 'Terror', 'Suspenso'];
        if (!content.genre.some(genre => highImpactGenres.includes(genre))) {
            recommendations.push('Enfócate en aspectos emocionales o dramáticos');
        }
        
        return recommendations;
    }
    
    /**
     * Obtiene contenido del cache
     * @param {string} key - Clave del cache
     * @returns {any} Contenido del cache o null
     */
    _getFromCache(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
            return cached.data;
        }
        return null;
    }
    
    /**
     * Establece contenido en el cache
     * @param {string} key - Clave del cache
     * @param {any} data - Datos a cachear
     */
    _setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }
    
    /**
     * Limpia el cache expirado
     */
    cleanCache() {
        const now = Date.now();
        for (const [key, value] of this.cache.entries()) {
            if (now - value.timestamp >= this.cacheExpiry) {
                this.cache.delete(key);
            }
        }
    }
}

// Instancia global del analizador
window.ContentAnalyzer = ContentAnalyzer;
window.contentAnalyzer = new ContentAnalyzer();
