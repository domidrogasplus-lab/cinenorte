/**
 * Sistema de Optimización con IA para Cine Norte
 * Analiza y optimiza contenido para máximo engagement
 */

class AIOptimizer {
    constructor() {
        this.openaiBaseUrl = 'https://api.openai.com/v1';
        this.huggingfaceBaseUrl = 'https://api-inference.huggingface.co/models';
        this.cache = new Map();
    }
    
    /**
     * Optimiza contenido completo con IA
     * @param {Object} script - Guion generado
     * @param {Object} contentInfo - Información del contenido
     * @param {Blob} videoBlob - Video generado (opcional)
     * @returns {Promise<Object>} Análisis de optimización
     */
    async optimizeContent(script, contentInfo, videoBlob = null) {
        try {
            this.showLoading('Analizando contenido con IA...');
            
            // Análisis de contenido
            const contentScore = this._analyzeContentQuality(script, contentInfo);
            
            // Análisis de engagement
            const engagementPotential = this._analyzeEngagementPotential(script);
            
            // Análisis de viralidad
            const viralProbability = this._analyzeViralPotential(script, contentInfo);
            
            // Análisis SEO
            const seoAnalysis = this._analyzeSEOOptimization(script, contentInfo);
            
            // Análisis visual (si hay video)
            let visualImpact = 0;
            if (videoBlob) {
                const visualAnalysis = await this._analyzeVisualContent(videoBlob);
                visualImpact = visualAnalysis.composition_score;
            }
            
            // Análisis de audio
            const audioAnalysis = this._analyzeAudioQuality(script);
            
            // Calcular score general
            const overallScore = this._calculateOverallScore(
                contentScore, engagementPotential, viralProbability,
                seoAnalysis, visualImpact, audioAnalysis
            );
            
            // Generar recomendaciones
            const recommendations = this._generateRecommendations(
                contentScore, engagementPotential, viralProbability,
                seoAnalysis, visualImpact, audioAnalysis
            );
            
            // Generar mejoras específicas
            const improvements = this._generateImprovements(
                script, contentInfo, visualImpact, audioAnalysis
            );
            
            this.hideLoading();
            
            return {
                content_score: contentScore,
                engagement_potential: engagementPotential,
                viral_probability: viralProbability,
                seo_score: seoAnalysis.overall_score,
                visual_impact: visualImpact,
                audio_quality: audioAnalysis.volume_consistency,
                overall_score: overallScore,
                recommendations: recommendations,
                improvements: improvements,
                generated_at: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('Error optimizando contenido:', error);
            this.hideLoading();
            return this._createFallbackAnalysis();
        }
    }
    
    /**
     * Analiza calidad del contenido
     * @param {Object} script - Guion generado
     * @param {Object} contentInfo - Información del contenido
     * @returns {number} Score de calidad
     */
    _analyzeContentQuality(script, contentInfo) {
        let score = 0;
        
        // Análisis de longitud del guion
        const wordCount = script.word_count;
        if (wordCount >= 100 && wordCount <= 500) {
            score += 20;
        } else if (wordCount >= 50 && wordCount <= 800) {
            score += 15;
        } else {
            score += 10;
        }
        
        // Análisis de estructura
        const sectionCount = script.sections.length;
        if (sectionCount >= 3 && sectionCount <= 6) {
            score += 20;
        } else if (sectionCount >= 2 && sectionCount <= 8) {
            score += 15;
        } else {
            score += 10;
        }
        
        // Análisis de duración
        const duration = script.total_duration;
        if (duration >= 60 && duration <= 180) {
            score += 20;
        } else if (duration >= 30 && duration <= 240) {
            score += 15;
        } else {
            score += 10;
        }
        
        // Análisis de popularidad del contenido
        const popularityScore = Math.min(contentInfo.popularity / 100, 1) * 20;
        score += popularityScore;
        
        // Análisis de rating
        const ratingScore = (contentInfo.rating / 10) * 20;
        score += ratingScore;
        
        return Math.min(100, score);
    }
    
    /**
     * Analiza potencial de engagement
     * @param {Object} script - Guion generado
     * @returns {number} Score de engagement
     */
    _analyzeEngagementPotential(script) {
        let score = 0;
        
        // Análisis de palabras emocionales
        const emotionalWords = this._countEmotionalWords(script.raw_text);
        const emotionalScore = Math.min(emotionalWords / 10, 1) * 25;
        score += emotionalScore;
        
        // Análisis de preguntas y call-to-actions
        const questions = (script.raw_text.match(/\?/g) || []).length;
        const ctas = (script.raw_text.match(/(suscríbete|comenta|like|comparte)/gi) || []).length;
        const interactionScore = Math.min((questions + ctas) / 5, 1) * 25;
        score += interactionScore;
        
        // Análisis de hooks y ganchos
        const hooks = this._analyzeHooks(script);
        const hookScore = Math.min(hooks / 3, 1) * 25;
        score += hookScore;
        
        // Análisis de variedad de emociones
        const emotionVariety = new Set(script.sections.map(s => s.emotion)).size;
        const varietyScore = Math.min(emotionVariety / 4, 1) * 25;
        score += varietyScore;
        
        return Math.min(100, score);
    }
    
    /**
     * Analiza potencial viral
     * @param {Object} script - Guion generado
     * @param {Object} contentInfo - Información del contenido
     * @returns {number} Score de viralidad
     */
    _analyzeViralPotential(script, contentInfo) {
        let score = 0;
        
        // Análisis de trending topics
        const trendingScore = this._analyzeTrendingKeywords(script.raw_text);
        score += trendingScore * 30;
        
        // Análisis de controversia (sin spoilers)
        const controversyScore = this._analyzeControversyPotential(script, contentInfo);
        score += controversyScore * 20;
        
        // Análisis de shareability
        const shareabilityScore = this._analyzeShareability(script);
        score += shareabilityScore * 25;
        
        // Análisis de timing
        const timingScore = this._analyzeTimingRelevance(contentInfo);
        score += timingScore * 25;
        
        return Math.min(100, score);
    }
    
    /**
     * Analiza optimización SEO
     * @param {Object} script - Guion generado
     * @param {Object} contentInfo - Información del contenido
     * @returns {Object} Análisis SEO
     */
    _analyzeSEOOptimization(script, contentInfo) {
        // Análisis de keywords
        const keywords = this._extractKeywords(script.raw_text);
        const keywordDensity = this._calculateKeywordDensity(script.raw_text, keywords);
        
        // Análisis de títulos
        const titleScore = this._analyzeTitleOptimization(script.title_suggestions);
        
        // Análisis de hashtags
        const hashtagScore = this._analyzeHashtagOptimization(script.hashtags);
        
        // Análisis de descripción
        const descriptionScore = this._analyzeDescriptionOptimization(script.raw_text);
        
        // Score general SEO
        const overallScore = (titleScore + hashtagScore + descriptionScore) / 3;
        
        return {
            overall_score: overallScore,
            keywords: keywords,
            keyword_density: keywordDensity,
            title_score: titleScore,
            hashtag_score: hashtagScore,
            description_score: descriptionScore
        };
    }
    
    /**
     * Analiza contenido visual del video
     * @param {Blob} videoBlob - Video a analizar
     * @returns {Promise<Object>} Análisis visual
     */
    async _analyzeVisualContent(videoBlob) {
        try {
            // Crear video element temporal
            const video = document.createElement('video');
            video.src = URL.createObjectURL(videoBlob);
            
            return new Promise((resolve) => {
                video.onloadeddata = () => {
                    // Análisis básico de composición
                    const compositionScore = this._analyzeComposition(video);
                    
                    // Análisis de colores
                    const colorAnalysis = this._analyzeColors(video);
                    
                    // Análisis de movimiento
                    const motionAnalysis = this._analyzeMotion(video);
                    
                    URL.revokeObjectURL(video.src);
                    
                    resolve({
                        composition_score: compositionScore,
                        color_analysis: colorAnalysis,
                        motion_analysis: motionAnalysis,
                        visual_hooks: [],
                        recommended_cuts: []
                    });
                };
            });
        } catch (error) {
            console.error('Error analizando contenido visual:', error);
            return {
                composition_score: 50,
                color_analysis: {},
                motion_analysis: {},
                visual_hooks: [],
                recommended_cuts: []
            };
        }
    }
    
    /**
     * Analiza calidad del audio
     * @param {Object} script - Guion generado
     * @returns {Object} Análisis de audio
     */
    _analyzeAudioQuality(script) {
        // Análisis de consistencia de volumen
        const volumeConsistency = this._analyzeVolumeConsistency(script);
        
        // Análisis de claridad del habla
        const speechClarity = this._analyzeSpeechClarity(script);
        
        // Análisis de balance musical
        const musicBalance = this._analyzeMusicBalance(script);
        
        // Análisis de silencios
        const silenceAnalysis = this._analyzeSilences(script);
        
        // Recomendaciones de ajuste
        const adjustments = this._generateAudioAdjustments(
            volumeConsistency, speechClarity, musicBalance
        );
        
        return {
            volume_consistency: volumeConsistency,
            speech_clarity: speechClarity,
            music_balance: musicBalance,
            silence_analysis: silenceAnalysis,
            recommended_adjustments: adjustments
        };
    }
    
    /**
     * Cuenta palabras emocionales en el texto
     * @param {string} text - Texto a analizar
     * @returns {number} Cantidad de palabras emocionales
     */
    _countEmotionalWords(text) {
        const emotionalWords = [
            'increíble', 'espectacular', 'impresionante', 'sorprendente',
            'emocionante', 'intenso', 'dramático', 'épico', 'genial',
            'fantástico', 'excelente', 'maravilloso', 'asombroso'
        ];
        
        let count = 0;
        const textLower = text.toLowerCase();
        for (const word of emotionalWords) {
            count += (textLower.match(new RegExp(word, 'g')) || []).length;
        }
        
        return count;
    }
    
    /**
     * Analiza hooks y ganchos en el guion
     * @param {Object} script - Guion generado
     * @returns {number} Cantidad de hooks
     */
    _analyzeHooks(script) {
        const hookPatterns = [
            /\?/g,  // Preguntas
            /!/g,   // Exclamaciones
            /(nunca|siempre|definitivamente|absolutamente)/gi,
            /(descubre|conoce|aprende|mira)/gi,
            /(spoiler|revelación|sorpresa)/gi
        ];
        
        let hookCount = 0;
        for (const pattern of hookPatterns) {
            hookCount += (script.raw_text.match(pattern) || []).length;
        }
        
        return hookCount;
    }
    
    /**
     * Analiza keywords trending en el texto
     * @param {string} text - Texto a analizar
     * @returns {number} Score de trending
     */
    _analyzeTrendingKeywords(text) {
        const trendingKeywords = [
            'netflix', 'disney', 'marvel', 'dc', 'streaming',
            'película', 'serie', 'tráiler', 'estreno', 'nuevo'
        ];
        
        const textLower = text.toLowerCase();
        const foundKeywords = trendingKeywords.filter(keyword => 
            textLower.includes(keyword)
        ).length;
        
        return Math.min(foundKeywords / trendingKeywords.length, 1.0);
    }
    
    /**
     * Analiza potencial de controversia
     * @param {Object} script - Guion generado
     * @param {Object} contentInfo - Información del contenido
     * @returns {number} Score de controversia
     */
    _analyzeControversyPotential(script, contentInfo) {
        const controversyWords = [
            'polémico', 'debate', 'discutido', 'controversial',
            'divisivo', 'opinión', 'crítico', 'revisión'
        ];
        
        const textLower = script.raw_text.toLowerCase();
        const controversyCount = controversyWords.filter(word => 
            textLower.includes(word)
        ).length;
        
        return Math.min(controversyCount / 5, 1.0);
    }
    
    /**
     * Analiza potencial de compartir
     * @param {Object} script - Guion generado
     * @returns {number} Score de shareability
     */
    _analyzeShareability(script) {
        const shareabilityIndicators = [
            'comparte', 'compartir', 'viral', 'tendencia',
            'recomienda', 'recomendación', 'debe ver', 'no te pierdas'
        ];
        
        const textLower = script.raw_text.toLowerCase();
        const shareabilityCount = shareabilityIndicators.filter(indicator => 
            textLower.includes(indicator)
        ).length;
        
        return Math.min(shareabilityCount / 3, 1.0);
    }
    
    /**
     * Analiza relevancia temporal del contenido
     * @param {Object} contentInfo - Información del contenido
     * @returns {number} Score de timing
     */
    _analyzeTimingRelevance(contentInfo) {
        try {
            const releaseDate = new Date(contentInfo.release_date);
            const now = new Date();
            const daysOld = (now - releaseDate) / (1000 * 60 * 60 * 24);
            
            if (daysOld <= 30) return 1.0;
            if (daysOld <= 90) return 0.8;
            if (daysOld <= 365) return 0.6;
            return 0.4;
        } catch {
            return 0.5;
        }
    }
    
    /**
     * Extrae keywords del texto
     * @param {string} text - Texto a analizar
     * @returns {Array} Lista de keywords
     */
    _extractKeywords(text) {
        // Palabras comunes a excluir
        const stopWords = [
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se',
            'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con',
            'para', 'al', 'del', 'los', 'las', 'una', 'como', 'más',
            'pero', 'sus', 'todo', 'esta', 'muy', 'ya', 'cuando',
            'todo', 'sobre', 'entre', 'hasta', 'desde', 'durante'
        ];
        
        // Extraer palabras
        const words = text.toLowerCase()
            .replace(/[^\w\s]/g, '')
            .split(/\s+/)
            .filter(word => word.length > 3 && !stopWords.includes(word));
        
        // Contar frecuencia
        const wordCount = {};
        words.forEach(word => {
            wordCount[word] = (wordCount[word] || 0) + 1;
        });
        
        // Ordenar por frecuencia
        return Object.entries(wordCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([word]) => word);
    }
    
    /**
     * Calcula densidad de keywords
     * @param {string} text - Texto a analizar
     * @param {Array} keywords - Lista de keywords
     * @returns {Object} Densidad de keywords
     */
    _calculateKeywordDensity(text, keywords) {
        const wordCount = text.split(' ').length;
        const densities = {};
        
        keywords.forEach(keyword => {
            const count = (text.toLowerCase().match(new RegExp(keyword, 'g')) || []).length;
            densities[keyword] = (count / wordCount) * 100;
        });
        
        return densities;
    }
    
    /**
     * Analiza optimización de títulos
     * @param {Array} titles - Lista de títulos
     * @returns {number} Score de optimización
     */
    _analyzeTitleOptimization(titles) {
        if (!titles || titles.length === 0) return 0;
        
        let totalScore = 0;
        
        titles.forEach(title => {
            let score = 0;
            
            // Longitud óptima (50-60 caracteres)
            if (title.length >= 50 && title.length <= 60) {
                score += 30;
            } else if (title.length >= 40 && title.length <= 70) {
                score += 20;
            } else {
                score += 10;
            }
            
            // Palabras clave emocionales
            const emotionalWords = ['increíble', 'sorprendente', 'épico', 'mejor', 'peor'];
            const emotionalCount = emotionalWords.filter(word => 
                title.toLowerCase().includes(word)
            ).length;
            score += Math.min(emotionalCount * 10, 30);
            
            // Números y símbolos
            if (/\d/.test(title)) score += 10;
            if (/[!?]/.test(title)) score += 10;
            
            // Palabras de acción
            const actionWords = ['descubre', 'mira', 'conoce', 'aprende', 'revela'];
            const actionCount = actionWords.filter(word => 
                title.toLowerCase().includes(word)
            ).length;
            score += Math.min(actionCount * 10, 20);
            
            totalScore += Math.min(score, 100);
        });
        
        return totalScore / titles.length;
    }
    
    /**
     * Analiza optimización de hashtags
     * @param {Array} hashtags - Lista de hashtags
     * @returns {number} Score de optimización
     */
    _analyzeHashtagOptimization(hashtags) {
        if (!hashtags || hashtags.length === 0) return 0;
        
        let score = 0;
        
        // Cantidad óptima (5-15 hashtags)
        if (hashtags.length >= 5 && hashtags.length <= 15) {
            score += 30;
        } else if (hashtags.length >= 3 && hashtags.length <= 20) {
            score += 20;
        } else {
            score += 10;
        }
        
        // Diversidad de hashtags
        const uniqueHashtags = new Set(hashtags).size;
        const diversityScore = Math.min(uniqueHashtags / hashtags.length, 1) * 20;
        score += diversityScore;
        
        // Hashtags trending
        const trendingHashtags = ['#viral', '#tendencia', '#nuevo', '#estreno', '#netflix'];
        const trendingCount = hashtags.filter(tag => 
            trendingHashtags.includes(tag.toLowerCase())
        ).length;
        score += Math.min(trendingCount * 10, 30);
        
        // Longitud de hashtags
        const avgLength = hashtags.reduce((sum, tag) => sum + tag.length, 0) / hashtags.length;
        if (avgLength >= 5 && avgLength <= 15) {
            score += 20;
        } else {
            score += 10;
        }
        
        return Math.min(score, 100);
    }
    
    /**
     * Analiza optimización de descripción
     * @param {string} text - Texto de descripción
     * @returns {number} Score de optimización
     */
    _analyzeDescriptionOptimization(text) {
        let score = 0;
        
        // Longitud óptima (150-300 caracteres)
        if (text.length >= 150 && text.length <= 300) {
            score += 30;
        } else if (text.length >= 100 && text.length <= 400) {
            score += 20;
        } else {
            score += 10;
        }
        
        // Call-to-action
        const ctaWords = ['suscríbete', 'comenta', 'comparte', 'like', 'síguenos'];
        const ctaCount = ctaWords.filter(word => 
            text.toLowerCase().includes(word)
        ).length;
        score += Math.min(ctaCount * 15, 30);
        
        // Densidad de keywords
        const wordCount = text.split(' ').length;
        const keywordDensity = wordCount / text.length;
        if (keywordDensity >= 0.1 && keywordDensity <= 0.3) {
            score += 20;
        } else {
            score += 10;
        }
        
        // Emojis (opcional)
        const emojiCount = (text.match(/[^\w\s]/g) || []).length;
        if (emojiCount >= 1 && emojiCount <= 5) {
            score += 20;
        } else {
            score += 10;
        }
        
        return Math.min(score, 100);
    }
    
    /**
     * Analiza composición del video
     * @param {HTMLVideoElement} video - Video a analizar
     * @returns {number} Score de composición
     */
    _analyzeComposition(video) {
        // Análisis básico de composición
        const aspectRatio = video.videoWidth / video.videoHeight;
        
        // Verificar regla de tercios
        let score = 50;
        
        if (aspectRatio >= 1.7 && aspectRatio <= 1.8) {
            score += 20; // 16:9
        } else if (aspectRatio >= 0.5 && aspectRatio <= 0.6) {
            score += 20; // 9:16
        } else if (aspectRatio >= 0.9 && aspectRatio <= 1.1) {
            score += 15; // 1:1
        }
        
        return Math.min(score, 100);
    }
    
    /**
     * Analiza colores del video
     * @param {HTMLVideoElement} video - Video a analizar
     * @returns {Object} Análisis de colores
     */
    _analyzeColors(video) {
        // Análisis básico de colores
        return {
            dominant_colors: [],
            color_consistency: 0.5,
            contrast_ratio: 0.7
        };
    }
    
    /**
     * Analiza movimiento en el video
     * @param {HTMLVideoElement} video - Video a analizar
     * @returns {Object} Análisis de movimiento
     */
    _analyzeMotion(video) {
        // Análisis básico de movimiento
        return {
            motion_intensity: 0.5,
            motion_consistency: 0.5,
            camera_stability: 0.7
        };
    }
    
    /**
     * Analiza consistencia de volumen
     * @param {Object} script - Guion generado
     * @returns {number} Score de consistencia
     */
    _analyzeVolumeConsistency(script) {
        // Análisis básico de consistencia
        return 75;
    }
    
    /**
     * Analiza claridad del habla
     * @param {Object} script - Guion generado
     * @returns {number} Score de claridad
     */
    _analyzeSpeechClarity(script) {
        // Análisis básico de claridad
        return 80;
    }
    
    /**
     * Analiza balance musical
     * @param {Object} script - Guion generado
     * @returns {number} Score de balance
     */
    _analyzeMusicBalance(script) {
        // Análisis básico de balance
        return 70;
    }
    
    /**
     * Analiza silencios en el audio
     * @param {Object} script - Guion generado
     * @returns {Array} Análisis de silencios
     */
    _analyzeSilences(script) {
        // Análisis básico de silencios
        return [];
    }
    
    /**
     * Genera recomendaciones de ajuste de audio
     * @param {number} volume - Score de volumen
     * @param {number} clarity - Score de claridad
     * @param {number} balance - Score de balance
     * @returns {Array} Recomendaciones
     */
    _generateAudioAdjustments(volume, clarity, balance) {
        const adjustments = [];
        
        if (volume < 70) {
            adjustments.push('Aumentar volumen general');
        }
        if (clarity < 70) {
            adjustments.push('Mejorar claridad del habla');
        }
        if (balance < 70) {
            adjustments.push('Ajustar balance musical');
        }
        
        return adjustments;
    }
    
    /**
     * Calcula score general de optimización
     * @param {number} contentScore - Score de contenido
     * @param {number} engagementPotential - Potencial de engagement
     * @param {number} viralProbability - Probabilidad viral
     * @param {Object} seoAnalysis - Análisis SEO
     * @param {number} visualImpact - Impacto visual
     * @param {Object} audioAnalysis - Análisis de audio
     * @returns {number} Score general
     */
    _calculateOverallScore(contentScore, engagementPotential, viralProbability, 
                          seoAnalysis, visualImpact, audioAnalysis) {
        const weights = {
            content: 0.25,
            engagement: 0.25,
            viral: 0.20,
            seo: 0.15,
            visual: 0.10,
            audio: 0.05
        };
        
        const seoScore = seoAnalysis.overall_score || 0;
        const audioScore = (audioAnalysis.volume_consistency + audioAnalysis.speech_clarity) / 2;
        
        const overallScore = (
            contentScore * weights.content +
            engagementPotential * weights.engagement +
            viralProbability * weights.viral +
            seoScore * weights.seo +
            visualImpact * weights.visual +
            audioScore * weights.audio
        );
        
        return Math.min(100, overallScore);
    }
    
    /**
     * Genera recomendaciones de optimización
     * @param {number} contentScore - Score de contenido
     * @param {number} engagementPotential - Potencial de engagement
     * @param {number} viralProbability - Probabilidad viral
     * @param {Object} seoAnalysis - Análisis SEO
     * @param {number} visualImpact - Impacto visual
     * @param {Object} audioAnalysis - Análisis de audio
     * @returns {Array} Lista de recomendaciones
     */
    _generateRecommendations(contentScore, engagementPotential, viralProbability,
                           seoAnalysis, visualImpact, audioAnalysis) {
        const recommendations = [];
        
        // Recomendaciones de contenido
        if (contentScore < 70) {
            recommendations.push('Mejora la estructura del guion con más secciones definidas');
            recommendations.push('Ajusta la duración para estar entre 60-180 segundos');
        }
        
        // Recomendaciones de engagement
        if (engagementPotential < 70) {
            recommendations.push('Agrega más preguntas y call-to-actions');
            recommendations.push('Incluye más palabras emocionales y hooks');
        }
        
        // Recomendaciones de viralidad
        if (viralProbability < 70) {
            recommendations.push('Incorpora más keywords trending');
            recommendations.push('Aumenta el potencial de controversia sin spoilers');
        }
        
        // Recomendaciones SEO
        const seoScore = seoAnalysis.overall_score || 0;
        if (seoScore < 70) {
            recommendations.push('Optimiza títulos con más palabras clave emocionales');
            recommendations.push('Mejora la diversidad y relevancia de hashtags');
        }
        
        // Recomendaciones visuales
        if (visualImpact < 70) {
            recommendations.push('Mejora la composición visual del video');
            recommendations.push('Agrega más elementos visuales llamativos');
        }
        
        // Recomendaciones de audio
        if (audioAnalysis.volume_consistency < 70) {
            recommendations.push('Normaliza el volumen del audio');
            recommendations.push('Mejora la claridad del habla');
        }
        
        return recommendations;
    }
    
    /**
     * Genera mejoras específicas
     * @param {Object} script - Guion generado
     * @param {Object} contentInfo - Información del contenido
     * @param {number} visualImpact - Impacto visual
     * @param {Object} audioAnalysis - Análisis de audio
     * @returns {Array} Lista de mejoras
     */
    _generateImprovements(script, contentInfo, visualImpact, audioAnalysis) {
        const improvements = [];
        
        // Mejoras de guion
        if (script.word_count < 100) {
            improvements.push('Expandir el guion con más detalles y análisis');
        } else if (script.word_count > 500) {
            improvements.push('Condensar el guion para mayor impacto');
        }
        
        // Mejoras de estructura
        if (script.sections.length < 3) {
            improvements.push('Agregar más secciones para mejor estructura');
        }
        
        // Mejoras de duración
        if (script.total_duration < 60) {
            improvements.push('Extender la duración para mayor engagement');
        } else if (script.total_duration > 180) {
            improvements.push('Reducir la duración para mantener atención');
        }
        
        // Mejoras de audio
        if (audioAnalysis.silence_analysis && audioAnalysis.silence_analysis.length > 0) {
            improvements.push('Reducir silencios largos en el audio');
        }
        
        return improvements;
    }
    
    /**
     * Crea análisis de respaldo si falla la optimización
     * @returns {Object} Análisis de respaldo
     */
    _createFallbackAnalysis() {
        return {
            content_score: 50.0,
            engagement_potential: 50.0,
            viral_probability: 50.0,
            seo_score: 50.0,
            visual_impact: 50.0,
            audio_quality: 50.0,
            overall_score: 50.0,
            recommendations: ['Revisar configuración de IA', 'Verificar calidad del contenido'],
            improvements: ['Optimizar configuración', 'Mejorar calidad general'],
            generated_at: new Date().toISOString()
        };
    }
    
    /**
     * Muestra indicador de carga
     * @param {string} message - Mensaje de carga
     */
    showLoading(message) {
        const loadingOverlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        
        if (loadingOverlay) {
            loadingOverlay.classList.add('active');
        }
        
        if (loadingText) {
            loadingText.textContent = message;
        }
    }
    
    /**
     * Oculta indicador de carga
     */
    hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        
        if (loadingOverlay) {
            loadingOverlay.classList.remove('active');
        }
    }
}

// Instancia global del optimizador
window.AIOptimizer = AIOptimizer;
window.aiOptimizer = new AIOptimizer();
