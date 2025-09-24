/**
 * Generador de Miniaturas para Cine Norte
 * Crea miniaturas optimizadas para diferentes plataformas
 */

class ThumbnailGenerator {
    constructor() {
        this.thumbnailSpecs = {
            youtube: {
                platform: 'YouTube',
                width: 1280,
                height: 720,
                aspectRatio: '16:9',
                textSize: 48,
                overlayOpacity: 0.8,
                description: 'Miniatura estándar para YouTube'
            },
            tiktok: {
                platform: 'TikTok',
                width: 1080,
                height: 1920,
                aspectRatio: '9:16',
                textSize: 36,
                overlayOpacity: 0.7,
                description: 'Miniatura vertical para TikTok'
            },
            instagram: {
                platform: 'Instagram',
                width: 1080,
                height: 1080,
                aspectRatio: '1:1',
                textSize: 42,
                overlayOpacity: 0.75,
                description: 'Miniatura cuadrado para Instagram'
            },
            facebook: {
                platform: 'Facebook',
                width: 1200,
                height: 630,
                aspectRatio: '1.91:1',
                textSize: 44,
                overlayOpacity: 0.8,
                description: 'Miniatura para Facebook'
            },
            twitter: {
                platform: 'Twitter',
                width: 1200,
                height: 675,
                aspectRatio: '16:9',
                textSize: 40,
                overlayOpacity: 0.8,
                description: 'Miniatura para Twitter'
            }
        };
        
        this.colorSchemes = {
            cinematic: {
                primary: '#E50914',
                secondary: '#C0C0C0',
                background: '#0A0A0A',
                text: '#FFFFFF',
                accent: '#FFD700'
            },
            dramatic: {
                primary: '#8B0000',
                secondary: '#808080',
                background: '#1A1A1A',
                text: '#FFFFFF',
                accent: '#FF4500'
            },
            action: {
                primary: '#FF0000',
                secondary: '#FFA500',
                background: '#000000',
                text: '#FFFFFF',
                accent: '#00FFFF'
            },
            mystery: {
                primary: '#4B0082',
                secondary: '#9370DB',
                background: '#2F2F2F',
                text: '#FFFFFF',
                accent: '#FFD700'
            }
        };
    }
    
    /**
     * Genera miniaturas para todas las plataformas
     * @param {Blob} videoBlob - Video fuente
     * @param {Object} contentInfo - Información del contenido
     * @param {string} title - Título del contenido
     * @param {string} style - Estilo visual
     * @returns {Promise<Array>} Miniaturas generadas
     */
    async generateThumbnails(videoBlob, contentInfo, title, style = 'cinematic') {
        const generatedThumbnails = [];
        
        for (const [platform, spec] of Object.entries(this.thumbnailSpecs)) {
            try {
                const thumbnail = await this._generateSingleThumbnail(
                    videoBlob, contentInfo, title, platform, spec, style
                );
                
                if (thumbnail) {
                    generatedThumbnails.push(thumbnail);
                }
                
            } catch (error) {
                console.error(`Error generando miniatura para ${platform}:`, error);
            }
        }
        
        return generatedThumbnails;
    }
    
    /**
     * Genera una miniatura específica
     * @param {Blob} videoBlob - Video fuente
     * @param {Object} contentInfo - Información del contenido
     * @param {string} title - Título del contenido
     * @param {string} platform - Plataforma objetivo
     * @param {Object} spec - Especificación de la miniatura
     * @param {string} style - Estilo visual
     * @returns {Promise<Object>} Miniatura generada
     */
    async _generateSingleThumbnail(videoBlob, contentInfo, title, platform, spec, style) {
        try {
            // Obtener esquema de color
            const colorScheme = this.colorSchemes[style] || this.colorSchemes.cinematic;
            
            // Extraer frame del video
            const baseImage = await this._extractVideoFrame(videoBlob, spec);
            
            // Aplicar efectos visuales
            const enhancedImage = this._applyVisualEffects(baseImage, contentInfo, style);
            
            // Crear overlay de texto
            const textOverlay = this._createTextOverlay(title, contentInfo, spec, colorScheme);
            
            // Combinar imagen base con overlay
            const finalImage = this._combineImageAndOverlay(enhancedImage, textOverlay, spec);
            
            // Agregar elementos de marca Cine Norte
            const brandedImage = this._addCineNorteBranding(finalImage, spec, colorScheme);
            
            // Convertir a blob
            const thumbnailBlob = await this._canvasToBlob(brandedImage);
            
            // Calcular score de optimización
            const optimizationScore = this._calculateOptimizationScore(
                brandedImage, platform, contentInfo
            );
            
            return {
                platform: platform,
                thumbnail_blob: thumbnailBlob,
                thumbnail_spec: spec,
                text_overlay: title,
                color_scheme: colorScheme,
                optimization_score: optimizationScore
            };
            
        } catch (error) {
            console.error(`Error generando miniatura ${platform}:`, error);
            return null;
        }
    }
    
    /**
     * Extrae frame representativo del video
     * @param {Blob} videoBlob - Video fuente
     * @param {Object} spec - Especificación de la miniatura
     * @returns {Promise<HTMLCanvasElement>} Canvas con el frame
     */
    async _extractVideoFrame(videoBlob, spec) {
        return new Promise((resolve, reject) => {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(videoBlob);
            
            video.onloadeddata = () => {
                // Obtener frame en el 30% del video
                video.currentTime = video.duration * 0.3;
            };
            
            video.onseeked = () => {
                // Crear canvas
                const canvas = document.createElement('canvas');
                canvas.width = spec.width;
                canvas.height = spec.height;
                const ctx = canvas.getContext('2d');
                
                // Dibujar frame
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                URL.revokeObjectURL(video.src);
                resolve(canvas);
            };
            
            video.onerror = () => {
                URL.revokeObjectURL(video.src);
                reject(new Error('Error cargando video'));
            };
        });
    }
    
    /**
     * Aplica efectos visuales según el estilo
     * @param {HTMLCanvasElement} canvas - Canvas de la imagen
     * @param {Object} contentInfo - Información del contenido
     * @param {string} style - Estilo visual
     * @returns {HTMLCanvasElement} Canvas con efectos aplicados
     */
    _applyVisualEffects(canvas, contentInfo, style) {
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        // Aplicar filtros según el estilo
        switch (style) {
            case 'dramatic':
                // Aumentar contraste y saturación
                for (let i = 0; i < data.length; i += 4) {
                    data[i] = Math.min(255, data[i] * 1.3);     // R
                    data[i + 1] = Math.min(255, data[i + 1] * 1.2); // G
                    data[i + 2] = Math.min(255, data[i + 2] * 1.2); // B
                }
                break;
                
            case 'action':
                // Aumentar nitidez y brillo
                for (let i = 0; i < data.length; i += 4) {
                    data[i] = Math.min(255, data[i] * 1.1);     // R
                    data[i + 1] = Math.min(255, data[i + 1] * 1.1); // G
                    data[i + 2] = Math.min(255, data[i + 2] * 1.1); // B
                }
                break;
                
            case 'mystery':
                // Aplicar desaturación parcial
                for (let i = 0; i < data.length; i += 4) {
                    const gray = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
                    data[i] = data[i] * 0.7 + gray * 0.3;     // R
                    data[i + 1] = data[i + 1] * 0.7 + gray * 0.3; // G
                    data[i + 2] = data[i + 2] * 0.7 + gray * 0.3; // B
                }
                break;
        }
        
        // Aplicar viñeta sutil a todos los estilos
        this._addSubtleVignette(ctx, canvas.width, canvas.height);
        
        ctx.putImageData(imageData, 0, 0);
        return canvas;
    }
    
    /**
     * Agrega viñeta sutil
     * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
     * @param {number} width - Ancho del canvas
     * @param {number} height - Alto del canvas
     */
    _addSubtleVignette(ctx, width, height) {
        const gradient = ctx.createRadialGradient(
            width / 2, height / 2, 0,
            width / 2, height / 2, Math.max(width, height) / 2
        );
        
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.3)');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
    }
    
    /**
     * Crea overlay de texto
     * @param {string} title - Título del contenido
     * @param {Object} contentInfo - Información del contenido
     * @param {Object} spec - Especificación de la miniatura
     * @param {Object} colorScheme - Esquema de colores
     * @returns {HTMLCanvasElement} Canvas con overlay de texto
     */
    _createTextOverlay(title, contentInfo, spec, colorScheme) {
        const canvas = document.createElement('canvas');
        canvas.width = spec.width;
        canvas.height = spec.height;
        const ctx = canvas.getContext('2d');
        
        // Preparar texto
        const titleText = this._formatTitleText(title, spec.width);
        const subtitleText = this._getSubtitleText(contentInfo);
        
        // Calcular posiciones
        const titleY = spec.height - 150;
        const subtitleY = spec.height - 100;
        
        // Dibujar fondo del título
        ctx.fillStyle = `rgba(0, 0, 0, ${spec.overlayOpacity})`;
        ctx.fillRect(0, titleY - 20, spec.width, 80);
        
        // Dibujar título
        ctx.fillStyle = colorScheme.text;
        ctx.font = `bold ${spec.textSize}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Efecto de sombra
        ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 2;
        
        ctx.fillText(titleText, spec.width / 2, titleY);
        
        // Dibujar subtítulo
        ctx.fillStyle = colorScheme.secondary;
        ctx.font = `${spec.textSize / 2}px Arial`;
        ctx.shadowBlur = 5;
        
        ctx.fillText(subtitleText, spec.width / 2, subtitleY);
        
        return canvas;
    }
    
    /**
     * Formatea el título para que quepa en la miniatura
     * @param {string} title - Título original
     * @param {number} maxWidth - Ancho máximo
     * @returns {string} Título formateado
     */
    _formatTitleText(title, maxWidth) {
        // Dividir título en líneas si es muy largo
        const words = title.split(' ');
        const lines = [];
        let currentLine = '';
        
        for (const word of words) {
            const testLine = currentLine + (currentLine ? ' ' : '') + word;
            
            // Estimar ancho del texto (aproximado)
            const estimatedWidth = testLine.length * 20;
            
            if (estimatedWidth <= maxWidth - 100) {
                currentLine = testLine;
            } else {
                if (currentLine) {
                    lines.push(currentLine);
                }
                currentLine = word;
            }
        }
        
        if (currentLine) {
            lines.push(currentLine);
        }
        
        return lines.slice(0, 3).join('\n'); // Máximo 3 líneas
    }
    
    /**
     * Obtiene texto del subtítulo
     * @param {Object} contentInfo - Información del contenido
     * @returns {string} Texto del subtítulo
     */
    _getSubtitleText(contentInfo) {
        const platform = contentInfo.platform || '';
        const contentType = contentInfo.content_type || '';
        
        if (contentType === 'movie') {
            return `Película en ${platform}`;
        } else if (contentType === 'tv') {
            return `Serie en ${platform}`;
        } else {
            return `Contenido en ${platform}`;
        }
    }
    
    /**
     * Combina imagen base con overlay
     * @param {HTMLCanvasElement} baseCanvas - Canvas base
     * @param {HTMLCanvasElement} overlayCanvas - Canvas overlay
     * @param {Object} spec - Especificación de la miniatura
     * @returns {HTMLCanvasElement} Canvas combinado
     */
    _combineImageAndOverlay(baseCanvas, overlayCanvas, spec) {
        const canvas = document.createElement('canvas');
        canvas.width = spec.width;
        canvas.height = spec.height;
        const ctx = canvas.getContext('2d');
        
        // Dibujar imagen base
        ctx.drawImage(baseCanvas, 0, 0);
        
        // Dibujar overlay
        ctx.drawImage(overlayCanvas, 0, 0);
        
        return canvas;
    }
    
    /**
     * Agrega branding de Cine Norte
     * @param {HTMLCanvasElement} canvas - Canvas de la miniatura
     * @param {Object} spec - Especificación de la miniatura
     * @param {Object} colorScheme - Esquema de colores
     * @returns {HTMLCanvasElement} Canvas con branding
     */
    _addCineNorteBranding(canvas, spec, colorScheme) {
        const ctx = canvas.getContext('2d');
        
        // Texto de marca
        const brandText = 'CINE NORTE';
        const brandX = spec.width - 200;
        const brandY = 30;
        
        // Dibujar fondo de marca
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(brandX - 10, brandY - 20, 180, 40);
        
        // Dibujar texto de marca
        ctx.fillStyle = colorScheme.primary;
        ctx.font = 'bold 20px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Efecto de sombra
        ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
        ctx.shadowBlur = 5;
        ctx.shadowOffsetX = 1;
        ctx.shadowOffsetY = 1;
        
        ctx.fillText(brandText, brandX + 80, brandY);
        
        // Dibujar línea decorativa
        ctx.strokeStyle = colorScheme.accent;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(brandX, brandY + 15);
        ctx.lineTo(brandX + 160, brandY + 15);
        ctx.stroke();
        
        return canvas;
    }
    
    /**
     * Convierte canvas a blob
     * @param {HTMLCanvasElement} canvas - Canvas a convertir
     * @returns {Promise<Blob>} Blob de la imagen
     */
    async _canvasToBlob(canvas) {
        return new Promise((resolve) => {
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/jpeg', 0.95);
        });
    }
    
    /**
     * Calcula score de optimización de la miniatura
     * @param {HTMLCanvasElement} canvas - Canvas de la miniatura
     * @param {string} platform - Plataforma objetivo
     * @param {Object} contentInfo - Información del contenido
     * @returns {number} Score de optimización
     */
    _calculateOptimizationScore(canvas, platform, contentInfo) {
        let score = 0;
        
        // Score por contraste (0-25 puntos)
        const contrastScore = this._analyzeContrast(canvas);
        score += contrastScore * 25;
        
        // Score por legibilidad del texto (0-25 puntos)
        const readabilityScore = this._analyzeTextReadability(canvas);
        score += readabilityScore * 25;
        
        // Score por composición (0-25 puntos)
        const compositionScore = this._analyzeComposition(canvas);
        score += compositionScore * 25;
        
        // Score por branding (0-25 puntos)
        const brandingScore = this._analyzeBrandingPresence(canvas);
        score += brandingScore * 25;
        
        return Math.min(100, score);
    }
    
    /**
     * Analiza contraste de la imagen
     * @param {HTMLCanvasElement} canvas - Canvas de la imagen
     * @returns {number} Score de contraste
     */
    _analyzeContrast(canvas) {
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        let sum = 0;
        let sumSquares = 0;
        const pixelCount = data.length / 4;
        
        for (let i = 0; i < data.length; i += 4) {
            const gray = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
            sum += gray;
            sumSquares += gray * gray;
        }
        
        const mean = sum / pixelCount;
        const variance = (sumSquares / pixelCount) - (mean * mean);
        const stdDev = Math.sqrt(variance);
        
        // Normalizar a 0-1
        return Math.min(stdDev / 128, 1.0);
    }
    
    /**
     * Analiza legibilidad del texto
     * @param {HTMLCanvasElement} canvas - Canvas de la imagen
     * @returns {number} Score de legibilidad
     */
    _analyzeTextReadability(canvas) {
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        // Análisis de bordes como proxy de legibilidad
        let edgeCount = 0;
        for (let y = 1; y < canvas.height - 1; y++) {
            for (let x = 1; x < canvas.width - 1; x++) {
                const idx = (y * canvas.width + x) * 4;
                const current = data[idx] + data[idx + 1] + data[idx + 2];
                
                const right = data[idx + 4] + data[idx + 5] + data[idx + 6];
                const bottom = data[idx + canvas.width * 4] + 
                              data[idx + canvas.width * 4 + 1] + 
                              data[idx + canvas.width * 4 + 2];
                
                if (Math.abs(current - right) > 50 || Math.abs(current - bottom) > 50) {
                    edgeCount++;
                }
            }
        }
        
        const edgeDensity = edgeCount / (canvas.width * canvas.height);
        return Math.min(edgeDensity * 100, 1.0);
    }
    
    /**
     * Analiza composición de la imagen
     * @param {HTMLCanvasElement} canvas - Canvas de la imagen
     * @returns {number} Score de composición
     */
    _analyzeComposition(canvas) {
        // Análisis básico de composición
        const aspectRatio = canvas.width / canvas.height;
        
        let score = 50;
        
        // Verificar regla de tercios
        if (aspectRatio >= 1.7 && aspectRatio <= 1.8) {
            score += 20; // 16:9
        } else if (aspectRatio >= 0.5 && aspectRatio <= 0.6) {
            score += 20; // 9:16
        } else if (aspectRatio >= 0.9 && aspectRatio <= 1.1) {
            score += 15; // 1:1
        }
        
        return Math.min(score / 100, 1.0);
    }
    
    /**
     * Analiza presencia del branding
     * @param {HTMLCanvasElement} canvas - Canvas de la imagen
     * @returns {number} Score de branding
     */
    _analyzeBrandingPresence(canvas) {
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        // Buscar colores de marca en la imagen
        const brandColors = [
            [229, 9, 20],    // #E50914
            [192, 192, 192], // #C0C0C0
            [10, 10, 10]     // #0A0A0A
        ];
        
        let brandPixelCount = 0;
        const totalPixels = data.length / 4;
        
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            
            for (const [br, bg, bb] of brandColors) {
                if (Math.abs(r - br) < 30 && Math.abs(g - bg) < 30 && Math.abs(b - bb) < 30) {
                    brandPixelCount++;
                    break;
                }
            }
        }
        
        return Math.min(brandPixelCount / totalPixels * 10, 1.0);
    }
    
    /**
     * Obtiene especificaciones de miniaturas
     * @returns {Object} Especificaciones de miniaturas
     */
    getThumbnailSpecs() {
        return { ...this.thumbnailSpecs };
    }
    
    /**
     * Obtiene esquemas de color disponibles
     * @returns {Object} Esquemas de color
     */
    getColorSchemes() {
        return { ...this.colorSchemes };
    }
}

// Instancia global del generador
window.ThumbnailGenerator = ThumbnailGenerator;
window.thumbnailGenerator = new ThumbnailGenerator();
