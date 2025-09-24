/**
 * Generador de Formatos Múltiples para Cine Norte
 * Crea videos optimizados para diferentes plataformas
 */

class FormatGenerator {
    constructor() {
        this.formats = {
            youtube: {
                name: 'YouTube',
                width: 1920,
                height: 1080,
                aspectRatio: '16:9',
                platform: 'youtube',
                maxDuration: 180,
                recommendedFps: 24,
                bitrate: '5000k',
                description: 'Formato estándar para YouTube, optimizado para desktop y TV'
            },
            tiktok: {
                name: 'TikTok',
                width: 1080,
                height: 1920,
                aspectRatio: '9:16',
                platform: 'tiktok',
                maxDuration: 60,
                recommendedFps: 30,
                bitrate: '3000k',
                description: 'Formato vertical para TikTok, optimizado para móviles'
            },
            instagram_reels: {
                name: 'Instagram Reels',
                width: 1080,
                height: 1920,
                aspectRatio: '9:16',
                platform: 'instagram',
                maxDuration: 90,
                recommendedFps: 30,
                bitrate: '3000k',
                description: 'Formato vertical para Instagram Reels'
            },
            instagram_square: {
                name: 'Instagram Square',
                width: 1080,
                height: 1080,
                aspectRatio: '1:1',
                platform: 'instagram',
                maxDuration: 60,
                recommendedFps: 30,
                bitrate: '2500k',
                description: 'Formato cuadrado para Instagram posts'
            },
            facebook: {
                name: 'Facebook',
                width: 1920,
                height: 1080,
                aspectRatio: '16:9',
                platform: 'facebook',
                maxDuration: 240,
                recommendedFps: 24,
                bitrate: '4000k',
                description: 'Formato para Facebook videos'
            },
            twitter: {
                name: 'Twitter',
                width: 1280,
                height: 720,
                aspectRatio: '16:9',
                platform: 'twitter',
                maxDuration: 140,
                recommendedFps: 30,
                bitrate: '2000k',
                description: 'Formato para Twitter videos'
            }
        };
    }
    
    /**
     * Genera todos los formatos disponibles para un video
     * @param {Blob} sourceVideo - Video fuente
     * @param {string} scriptTitle - Título del guion
     * @param {Object} contentInfo - Información del contenido
     * @returns {Promise<Array>} Formatos generados
     */
    async generateAllFormats(sourceVideo, scriptTitle, contentInfo) {
        const generatedFormats = [];
        
        for (const [formatType, spec] of Object.entries(this.formats)) {
            try {
                const generatedFormat = await this._generateSingleFormat(
                    sourceVideo,
                    formatType,
                    spec,
                    scriptTitle,
                    contentInfo
                );
                
                if (generatedFormat) {
                    generatedFormats.push(generatedFormat);
                }
                
            } catch (error) {
                console.error(`Error generando formato ${formatType}:`, error);
            }
        }
        
        return generatedFormats;
    }
    
    /**
     * Genera un formato específico
     * @param {Blob} sourceVideo - Video fuente
     * @param {string} formatType - Tipo de formato
     * @param {Object} spec - Especificación del formato
     * @param {string} scriptTitle - Título del guion
     * @param {Object} contentInfo - Información del contenido
     * @returns {Promise<Object>} Formato generado
     */
    async _generateSingleFormat(sourceVideo, formatType, spec, scriptTitle, contentInfo) {
        try {
            // Crear canvas para el formato específico
            const canvas = document.createElement('canvas');
            canvas.width = spec.width;
            canvas.height = spec.height;
            const ctx = canvas.getContext('2d');
            
            // Aplicar transformaciones específicas del formato
            await this._applyFormatTransformations(canvas, ctx, sourceVideo, formatType, spec);
            
            // Optimizar para la plataforma
            this._optimizeForPlatform(canvas, ctx, formatType, spec);
            
            // Generar video
            const videoBlob = await this._exportFormatVideo(canvas, formatType, scriptTitle);
            
            // Generar miniatura
            const thumbnailBlob = await this._generateThumbnail(canvas, formatType, scriptTitle, contentInfo);
            
            // Calcular score de optimización
            const optimizationScore = this._calculateOptimizationScore(canvas, formatType, spec);
            
            // Crear metadatos
            const metadata = this._createFormatMetadata(formatType, spec, contentInfo, optimizationScore);
            
            return {
                format_type: formatType,
                video_blob: videoBlob,
                thumbnail_blob: thumbnailBlob,
                metadata: metadata,
                optimization_score: optimizationScore
            };
            
        } catch (error) {
            console.error(`Error generando formato ${formatType}:`, error);
            return null;
        }
    }
    
    /**
     * Aplica transformaciones específicas del formato
     * @param {HTMLCanvasElement} canvas - Canvas de destino
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {Blob} sourceVideo - Video fuente
     * @param {string} formatType - Tipo de formato
     * @param {Object} spec - Especificación del formato
     */
    async _applyFormatTransformations(canvas, ctx, sourceVideo, formatType, spec) {
        // Crear video element temporal
        const video = document.createElement('video');
        video.src = URL.createObjectURL(sourceVideo);
        
        return new Promise((resolve) => {
            video.onloadeddata = () => {
                const sourceWidth = video.videoWidth || 1920;
                const sourceHeight = video.videoHeight || 1080;
                const targetWidth = spec.width;
                const targetHeight = spec.height;
                
                // Calcular factor de escala
                const scaleFactor = Math.min(targetWidth / sourceWidth, targetHeight / sourceHeight);
                
                // Aplicar transformaciones específicas por formato
                if (formatType === 'tiktok' || formatType === 'instagram_reels') {
                    // Formato vertical - centrar y recortar
                    this._createVerticalFormat(ctx, video, sourceWidth, sourceHeight, targetWidth, targetHeight, scaleFactor);
                } else if (formatType === 'instagram_square') {
                    // Formato cuadrado - centrar y recortar
                    this._createSquareFormat(ctx, video, sourceWidth, sourceHeight, targetWidth, targetHeight, scaleFactor);
                } else {
                    // Formato horizontal - centrar y rellenar si es necesario
                    this._createHorizontalFormat(ctx, video, sourceWidth, sourceHeight, targetWidth, targetHeight, scaleFactor);
                }
                
                URL.revokeObjectURL(video.src);
                resolve();
            };
        });
    }
    
    /**
     * Crea formato vertical (9:16)
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {HTMLVideoElement} video - Video fuente
     * @param {number} sourceWidth - Ancho fuente
     * @param {number} sourceHeight - Alto fuente
     * @param {number} targetWidth - Ancho objetivo
     * @param {number} targetHeight - Alto objetivo
     * @param {number} scaleFactor - Factor de escala
     */
    _createVerticalFormat(ctx, video, sourceWidth, sourceHeight, targetWidth, targetHeight, scaleFactor) {
        // Escalar video
        const scaledWidth = sourceWidth * scaleFactor;
        const scaledHeight = sourceHeight * scaleFactor;
        
        // Centrar horizontalmente
        const x = (targetWidth - scaledWidth) / 2;
        const y = (targetHeight - scaledHeight) / 2;
        
        // Dibujar video escalado
        ctx.drawImage(video, x, y, scaledWidth, scaledHeight);
        
        // Rellenar áreas vacías con color de fondo
        if (x > 0) {
            ctx.fillStyle = '#0A0A0A';
            ctx.fillRect(0, 0, x, targetHeight);
            ctx.fillRect(targetWidth - x, 0, x, targetHeight);
        }
    }
    
    /**
     * Crea formato cuadrado (1:1)
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {HTMLVideoElement} video - Video fuente
     * @param {number} sourceWidth - Ancho fuente
     * @param {number} sourceHeight - Alto fuente
     * @param {number} targetWidth - Ancho objetivo
     * @param {number} targetHeight - Alto objetivo
     * @param {number} scaleFactor - Factor de escala
     */
    _createSquareFormat(ctx, video, sourceWidth, sourceHeight, targetWidth, targetHeight, scaleFactor) {
        // Usar la dimensión más pequeña
        const minDimension = Math.min(sourceWidth, sourceHeight);
        const scaledSize = minDimension * scaleFactor;
        
        // Centrar en el canvas
        const x = (targetWidth - scaledSize) / 2;
        const y = (targetHeight - scaledSize) / 2;
        
        // Dibujar video cuadrado
        ctx.drawImage(video, x, y, scaledSize, scaledSize);
        
        // Rellenar áreas vacías
        if (x > 0 || y > 0) {
            ctx.fillStyle = '#0A0A0A';
            ctx.fillRect(0, 0, targetWidth, targetHeight);
            ctx.drawImage(video, x, y, scaledSize, scaledSize);
        }
    }
    
    /**
     * Crea formato horizontal (16:9)
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {HTMLVideoElement} video - Video fuente
     * @param {number} sourceWidth - Ancho fuente
     * @param {number} sourceHeight - Alto fuente
     * @param {number} targetWidth - Ancho objetivo
     * @param {number} targetHeight - Alto objetivo
     * @param {number} scaleFactor - Factor de escala
     */
    _createHorizontalFormat(ctx, video, sourceWidth, sourceHeight, targetWidth, targetHeight, scaleFactor) {
        // Escalar video
        const scaledWidth = sourceWidth * scaleFactor;
        const scaledHeight = sourceHeight * scaleFactor;
        
        // Centrar en el canvas
        const x = (targetWidth - scaledWidth) / 2;
        const y = (targetHeight - scaledHeight) / 2;
        
        // Dibujar video escalado
        ctx.drawImage(video, x, y, scaledWidth, scaledHeight);
        
        // Rellenar áreas vacías si es necesario
        if (x > 0 || y > 0) {
            ctx.fillStyle = '#0A0A0A';
            ctx.fillRect(0, 0, targetWidth, targetHeight);
            ctx.drawImage(video, x, y, scaledWidth, scaledHeight);
        }
    }
    
    /**
     * Optimiza video para plataforma específica
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {string} formatType - Tipo de formato
     * @param {Object} spec - Especificación del formato
     */
    _optimizeForPlatform(canvas, ctx, formatType, spec) {
        // Aplicar optimizaciones específicas por plataforma
        if (formatType === 'tiktok') {
            this._optimizeForTikTok(canvas, ctx);
        } else if (formatType === 'instagram_reels') {
            this._optimizeForInstagramReels(canvas, ctx);
        } else if (formatType === 'youtube') {
            this._optimizeForYouTube(canvas, ctx);
        }
    }
    
    /**
     * Optimizaciones específicas para TikTok
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     */
    _optimizeForTikTok(canvas, ctx) {
        // Aumentar contraste y saturación para móviles
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            // Aumentar contraste
            data[i] = Math.min(255, data[i] * 1.1);     // R
            data[i + 1] = Math.min(255, data[i + 1] * 1.1); // G
            data[i + 2] = Math.min(255, data[i + 2] * 1.1); // B
        }
        
        ctx.putImageData(imageData, 0, 0);
    }
    
    /**
     * Optimizaciones específicas para Instagram Reels
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     */
    _optimizeForInstagramReels(canvas, ctx) {
        // Optimizar para feed de Instagram
        // Aplicar filtros sutiles
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            // Ajuste sutil de brillo
            data[i] = Math.min(255, data[i] * 1.05);     // R
            data[i + 1] = Math.min(255, data[i + 1] * 1.05); // G
            data[i + 2] = Math.min(255, data[i + 2] * 1.05); // B
        }
        
        ctx.putImageData(imageData, 0, 0);
    }
    
    /**
     * Optimizaciones específicas para YouTube
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     */
    _optimizeForYouTube(canvas, ctx) {
        // Optimizar para reproducción en diferentes dispositivos
        // Mantener calidad original
    }
    
    /**
     * Exporta video en formato específico
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {string} formatType - Tipo de formato
     * @param {string} scriptTitle - Título del guion
     * @returns {Promise<Blob>} Video exportado
     */
    async _exportFormatVideo(canvas, formatType, scriptTitle) {
        return new Promise((resolve) => {
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'video/webm', 0.8);
        });
    }
    
    /**
     * Genera miniatura para el formato
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {string} formatType - Tipo de formato
     * @param {string} scriptTitle - Título del guion
     * @param {Object} contentInfo - Información del contenido
     * @returns {Promise<Blob>} Miniatura generada
     */
    async _generateThumbnail(canvas, formatType, scriptTitle, contentInfo) {
        // Crear canvas para miniatura
        const thumbnailCanvas = document.createElement('canvas');
        thumbnailCanvas.width = canvas.width;
        thumbnailCanvas.height = canvas.height;
        const thumbnailCtx = thumbnailCanvas.getContext('2d');
        
        // Copiar contenido del video
        thumbnailCtx.drawImage(canvas, 0, 0);
        
        // Agregar overlay de Cine Norte
        this._addCineNorteOverlay(thumbnailCtx, scriptTitle, canvas.width, canvas.height);
        
        return new Promise((resolve) => {
            thumbnailCanvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/jpeg', 0.95);
        });
    }
    
    /**
     * Agrega overlay de Cine Norte a la miniatura
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {string} title - Título del contenido
     * @param {number} width - Ancho del canvas
     * @param {number} height - Alto del canvas
     */
    _addCineNorteOverlay(ctx, title, width, height) {
        // Dibujar fondo semi-transparente
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, height - 100, width, 100);
        
        // Dibujar texto de marca
        ctx.fillStyle = '#E50914';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('CINE NORTE', width / 2, height - 50);
        
        // Dibujar título del contenido
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '18px Arial';
        ctx.fillText(title, width / 2, height - 25);
    }
    
    /**
     * Calcula score de optimización para el formato
     * @param {HTMLCanvasElement} canvas - Canvas del video
     * @param {string} formatType - Tipo de formato
     * @param {Object} spec - Especificación del formato
     * @returns {number} Score de optimización
     */
    _calculateOptimizationScore(canvas, formatType, spec) {
        let score = 0;
        
        // Score por resolución (0-40 puntos)
        const resolutionScore = Math.min(40, (canvas.width * canvas.height) / (spec.width * spec.height) * 40);
        score += resolutionScore;
        
        // Score por aspecto (0-30 puntos)
        const aspectRatio = canvas.width / canvas.height;
        const targetAspect = spec.width / spec.height;
        const aspectScore = 30 - Math.abs(aspectRatio - targetAspect) * 30;
        score += Math.max(0, aspectScore);
        
        // Score por calidad (0-30 puntos)
        const qualityScore = 30; // Asumir calidad alta
        score += qualityScore;
        
        return Math.min(100, score);
    }
    
    /**
     * Crea metadatos para el formato
     * @param {string} formatType - Tipo de formato
     * @param {Object} spec - Especificación del formato
     * @param {Object} contentInfo - Información del contenido
     * @param {number} optimizationScore - Score de optimización
     * @returns {Object} Metadatos del formato
     */
    _createFormatMetadata(formatType, spec, contentInfo, optimizationScore) {
        return {
            format_type: formatType,
            platform: spec.platform,
            dimensions: `${spec.width}x${spec.height}`,
            aspect_ratio: spec.aspectRatio,
            max_duration: spec.maxDuration,
            recommended_fps: spec.recommendedFps,
            bitrate: spec.bitrate,
            optimization_score: optimizationScore,
            description: spec.description,
            content_title: contentInfo.title || '',
            content_platform: contentInfo.platform || '',
            generated_at: new Date().toISOString()
        };
    }
    
    /**
     * Obtiene especificaciones de todos los formatos
     * @returns {Object} Especificaciones de formatos
     */
    getFormatSpecs() {
        return { ...this.formats };
    }
    
    /**
     * Obtiene especificación de un formato específico
     * @param {string} formatType - Tipo de formato
     * @returns {Object} Especificación del formato
     */
    getFormatSpec(formatType) {
        return this.formats[formatType] || null;
    }
    
    /**
     * Valida si un formato es compatible con la duración
     * @param {string} formatType - Tipo de formato
     * @param {number} duration - Duración en segundos
     * @returns {boolean} True si es compatible
     */
    isDurationCompatible(formatType, duration) {
        const spec = this.formats[formatType];
        return spec ? duration <= spec.maxDuration : false;
    }
    
    /**
     * Obtiene el formato recomendado para una duración
     * @param {number} duration - Duración en segundos
     * @returns {string} Formato recomendado
     */
    getRecommendedFormat(duration) {
        const compatibleFormats = Object.entries(this.formats)
            .filter(([_, spec]) => duration <= spec.maxDuration)
            .sort((a, b) => b[1].maxDuration - a[1].maxDuration);
        
        return compatibleFormats.length > 0 ? compatibleFormats[0][0] : 'youtube';
    }
}

// Instancia global del generador
window.FormatGenerator = FormatGenerator;
window.formatGenerator = new FormatGenerator();
