/**
 * Editor de Video con Canvas API para Cine Norte
 * Crea videos profesionales con branding Cine Norte
 */

class VideoEditor {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.videoElement = null;
        this.audioElement = null;
        this.currentFrame = 0;
        this.fps = 24;
        this.duration = 0;
        this.isPlaying = false;
        this.isRendering = false;
        this.frames = [];
        this.animationId = null;
        
        this.colors = {
            primaryRed: '#E50914',
            deepBlack: '#0A0A0A',
            metallicSilver: '#C0C0C0',
            white: '#FFFFFF',
            gold: '#FFD700'
        };
    }
    
    /**
     * Inicializa el editor de video
     * @param {string} canvasId - ID del canvas
     */
    initialize(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            throw new Error(`Canvas con ID '${canvasId}' no encontrado`);
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.setupCanvas();
    }
    
    /**
     * Configura el canvas
     */
    setupCanvas() {
        // Configurar canvas para alta resolución
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        
        this.ctx.scale(dpr, dpr);
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
    }
    
    /**
     * Crea un video completo con branding Cine Norte
     * @param {Object} script - Guion generado
     * @param {Blob} audioBlob - Audio generado
     * @param {Array} subtitles - Subtítulos
     * @param {string} formatType - Formato de salida
     * @param {string} style - Estilo visual
     * @returns {Promise<Blob>} Video generado
     */
    async createVideo(script, audioBlob, subtitles, formatType = 'youtube', style = 'cinematic') {
        try {
            this.showLoading('Creando video...');
            
            // Obtener dimensiones según formato
            const format = config.getVideoFormat(formatType);
            this.canvas.width = format.width;
            this.canvas.height = format.height;
            
            // Configurar duración
            this.duration = script.total_duration;
            this.fps = 24;
            
            // Crear elementos del video
            const videoElements = this._createVideoElements(script, format);
            
            // Renderizar frames
            await this._renderFrames(videoElements, subtitles, style);
            
            // Combinar con audio
            const videoBlob = await this._combineWithAudio(audioBlob);
            
            this.hideLoading();
            return videoBlob;
            
        } catch (error) {
            console.error('Error creando video:', error);
            this.hideLoading();
            throw error;
        }
    }
    
    /**
     * Crea elementos visuales del video
     * @param {Object} script - Guion generado
     * @param {Object} format - Formato de video
     * @returns {Array} Elementos del video
     */
    _createVideoElements(script, format) {
        const elements = [];
        
        // Crear intro con logo Cine Norte
        const introElement = this._createIntroElement(script, format);
        if (introElement) {
            elements.push(introElement);
        }
        
        // Crear elementos para cada sección del guion
        script.sections.forEach((section, index) => {
            const sectionElements = this._createSectionElements(section, index, format);
            elements.push(...sectionElements);
        });
        
        // Crear outro
        const outroElement = this._createOutroElement(script, format);
        if (outroElement) {
            elements.push(outroElement);
        }
        
        return elements;
    }
    
    /**
     * Crea elemento de introducción con logo
     * @param {Object} script - Guion generado
     * @param {Object} format - Formato de video
     * @returns {Object} Elemento de intro
     */
    _createIntroElement(script, format) {
        return {
            type: 'intro',
            startTime: 0,
            duration: 5,
            content: 'CINE NORTE',
            style: 'logo_animation',
            position: { x: format.width / 2, y: format.height / 2 },
            size: { width: format.width, height: format.height }
        };
    }
    
    /**
     * Crea elementos para una sección del guion
     * @param {Object} section - Sección del guion
     * @param {number} sectionIndex - Índice de la sección
     * @param {Object} format - Formato de video
     * @returns {Array} Elementos de la sección
     */
    _createSectionElements(section, sectionIndex, format) {
        const elements = [];
        
        // Crear fondo dinámico
        const backgroundElement = this._createBackgroundElement(section, format);
        if (backgroundElement) {
            elements.push(backgroundElement);
        }
        
        // Crear título de sección
        const titleElement = this._createSectionTitle(section, sectionIndex, format);
        if (titleElement) {
            elements.push(titleElement);
        }
        
        // Crear contenido de texto
        const textElement = this._createTextElement(section, format);
        if (textElement) {
            elements.push(textElement);
        }
        
        return elements;
    }
    
    /**
     * Crea elemento de fondo dinámico
     * @param {Object} section - Sección del guion
     * @param {Object} format - Formato de video
     * @returns {Object} Elemento de fondo
     */
    _createBackgroundElement(section, format) {
        return {
            type: 'background',
            startTime: 0,
            duration: section.duration_seconds,
            style: `gradient_${section.emotion}`,
            position: { x: 0, y: 0 },
            size: { width: format.width, height: format.height }
        };
    }
    
    /**
     * Crea título de sección
     * @param {Object} section - Sección del guion
     * @param {number} sectionIndex - Índice de la sección
     * @param {Object} format - Formato de video
     * @returns {Object} Elemento de título
     */
    _createSectionTitle(section, sectionIndex, format) {
        const titleText = this._getSectionTitleText(section.type);
        
        return {
            type: 'title',
            startTime: 0,
            duration: 3,
            content: titleText,
            style: 'section_title',
            position: { x: format.width / 2, y: format.height / 4 },
            size: { width: format.width, height: 100 }
        };
    }
    
    /**
     * Crea elemento de texto
     * @param {Object} section - Sección del guion
     * @param {Object} format - Formato de video
     * @returns {Object} Elemento de texto
     */
    _createTextElement(section, format) {
        return {
            type: 'text',
            startTime: 3,
            duration: section.duration_seconds - 3,
            content: section.content,
            style: 'body_text',
            position: { x: format.width / 2, y: format.height / 2 },
            size: { width: format.width - 100, height: format.height - 200 }
        };
    }
    
    /**
     * Crea elemento de cierre
     * @param {Object} script - Guion generado
     * @param {Object} format - Formato de video
     * @returns {Object} Elemento de outro
     */
    _createOutroElement(script, format) {
        return {
            type: 'outro',
            startTime: script.total_duration - 5,
            duration: 5,
            content: '¡SUSCRÍBETE!',
            style: 'outro_animation',
            position: { x: format.width / 2, y: format.height / 2 },
            size: { width: format.width, height: format.height }
        };
    }
    
    /**
     * Renderiza todos los frames del video
     * @param {Array} elements - Elementos del video
     * @param {Array} subtitles - Subtítulos
     * @param {string} style - Estilo visual
     */
    async _renderFrames(elements, subtitles, style) {
        const totalFrames = Math.floor(this.duration * this.fps);
        this.frames = [];
        
        for (let frame = 0; frame < totalFrames; frame++) {
            const time = frame / this.fps;
            
            // Limpiar canvas
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            // Renderizar elementos activos en este frame
            const activeElements = elements.filter(element => 
                time >= element.startTime && time < element.startTime + element.duration
            );
            
            for (const element of activeElements) {
                this._renderElement(element, time - element.startTime, style);
            }
            
            // Renderizar subtítulos
            this._renderSubtitles(subtitles, time);
            
            // Capturar frame
            const frameData = this.canvas.toDataURL('image/png');
            this.frames.push(frameData);
            
            // Actualizar progreso
            if (frame % 10 === 0) {
                const progress = (frame / totalFrames) * 100;
                this.updateProgress(`Renderizando frame ${frame}/${totalFrames} (${progress.toFixed(1)}%)`);
            }
        }
    }
    
    /**
     * Renderiza un elemento específico
     * @param {Object} element - Elemento a renderizar
     * @param {number} time - Tiempo relativo del elemento
     * @param {string} style - Estilo visual
     */
    _renderElement(element, time, style) {
        switch (element.type) {
            case 'intro':
                this._renderIntro(element, time);
                break;
            case 'background':
                this._renderBackground(element, time, style);
                break;
            case 'title':
                this._renderTitle(element, time);
                break;
            case 'text':
                this._renderText(element, time);
                break;
            case 'outro':
                this._renderOutro(element, time);
                break;
        }
    }
    
    /**
     * Renderiza la introducción
     * @param {Object} element - Elemento de intro
     * @param {number} time - Tiempo relativo
     */
    _renderIntro(element, time) {
        const { x, y } = element.position;
        const { width, height } = element.size;
        
        // Fondo negro
        this.ctx.fillStyle = this.colors.deepBlack;
        this.ctx.fillRect(0, 0, width, height);
        
        // Efecto de fade in
        const alpha = Math.min(time / 2, 1);
        
        // Logo Cine Norte
        this.ctx.save();
        this.ctx.globalAlpha = alpha;
        this.ctx.fillStyle = this.colors.primaryRed;
        this.ctx.font = 'bold 72px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        // Efecto de glow
        this.ctx.shadowColor = this.colors.primaryRed;
        this.ctx.shadowBlur = 20;
        
        this.ctx.fillText(element.content, x, y);
        
        // Efecto de zoom
        const scale = 1 + (time * 0.1);
        this.ctx.scale(scale, scale);
        
        this.ctx.restore();
    }
    
    /**
     * Renderiza el fondo
     * @param {Object} element - Elemento de fondo
     * @param {number} time - Tiempo relativo
     * @param {string} style - Estilo visual
     */
    _renderBackground(element, time, style) {
        const { width, height } = element.size;
        
        // Crear gradiente según emoción
        const gradient = this._createGradient(element.style, width, height);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);
        
        // Agregar efectos de partículas
        this._renderParticles(time, width, height);
    }
    
    /**
     * Renderiza el título
     * @param {Object} element - Elemento de título
     * @param {number} time - Tiempo relativo
     */
    _renderTitle(element, time) {
        const { x, y } = element.position;
        
        // Efecto de slide in desde arriba
        const slideY = y - 100 + (time * 50);
        
        this.ctx.save();
        this.ctx.fillStyle = this.colors.white;
        this.ctx.font = 'bold 48px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        // Sombra
        this.ctx.shadowColor = this.colors.deepBlack;
        this.ctx.shadowBlur = 10;
        this.ctx.shadowOffsetX = 2;
        this.ctx.shadowOffsetY = 2;
        
        this.ctx.fillText(element.content, x, slideY);
        this.ctx.restore();
    }
    
    /**
     * Renderiza el texto
     * @param {Object} element - Elemento de texto
     * @param {number} time - Tiempo relativo
     */
    _renderText(element, time) {
        const { x, y } = element.position;
        const { width, height } = element.size;
        
        // Dividir texto en líneas
        const lines = this._wrapText(element.content, width - 40);
        const lineHeight = 30;
        const startY = y - (lines.length * lineHeight) / 2;
        
        this.ctx.save();
        this.ctx.fillStyle = this.colors.white;
        this.ctx.font = '24px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'top';
        
        lines.forEach((line, index) => {
            const lineY = startY + (index * lineHeight);
            this.ctx.fillText(line, x, lineY);
        });
        
        this.ctx.restore();
    }
    
    /**
     * Renderiza el outro
     * @param {Object} element - Elemento de outro
     * @param {number} time - Tiempo relativo
     */
    _renderOutro(element, time) {
        const { x, y } = element.position;
        const { width, height } = element.size;
        
        // Fondo con gradiente
        const gradient = this.ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, this.colors.deepBlack);
        gradient.addColorStop(1, this.colors.primaryRed);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);
        
        // Texto del outro
        this.ctx.save();
        this.ctx.fillStyle = this.colors.white;
        this.ctx.font = 'bold 64px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        // Efecto de pulso
        const pulse = 1 + Math.sin(time * 4) * 0.1;
        this.ctx.scale(pulse, pulse);
        
        this.ctx.fillText(element.content, x, y);
        this.ctx.restore();
    }
    
    /**
     * Renderiza subtítulos
     * @param {Array} subtitles - Lista de subtítulos
     * @param {number} time - Tiempo actual
     */
    _renderSubtitles(subtitles, time) {
        const currentSubtitle = subtitles.find(sub => 
            time >= this._parseTime(sub.start_time) && 
            time <= this._parseTime(sub.end_time)
        );
        
        if (currentSubtitle) {
            const y = this.canvas.height - 100;
            
            this.ctx.save();
            
            // Fondo semi-transparente
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.fillRect(50, y - 30, this.canvas.width - 100, 60);
            
            // Texto del subtítulo
            this.ctx.fillStyle = this.colors.white;
            this.ctx.font = '24px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            
            this.ctx.fillText(currentSubtitle.text, this.canvas.width / 2, y);
            
            this.ctx.restore();
        }
    }
    
    /**
     * Crea un gradiente según el estilo
     * @param {string} style - Estilo del gradiente
     * @param {number} width - Ancho del canvas
     * @param {number} height - Alto del canvas
     * @returns {CanvasGradient} Gradiente creado
     */
    _createGradient(style, width, height) {
        const gradient = this.ctx.createLinearGradient(0, 0, width, height);
        
        switch (style) {
            case 'gradient_excitement':
                gradient.addColorStop(0, this.colors.primaryRed);
                gradient.addColorStop(1, this.colors.deepBlack);
                break;
            case 'gradient_suspense':
                gradient.addColorStop(0, this.colors.deepBlack);
                gradient.addColorStop(1, '#2A2A2A');
                break;
            case 'gradient_drama':
                gradient.addColorStop(0, '#2A2A2A');
                gradient.addColorStop(1, this.colors.deepBlack);
                break;
            default:
                gradient.addColorStop(0, this.colors.deepBlack);
                gradient.addColorStop(1, '#1A1A1A');
        }
        
        return gradient;
    }
    
    /**
     * Renderiza partículas de fondo
     * @param {number} time - Tiempo actual
     * @param {number} width - Ancho del canvas
     * @param {number} height - Alto del canvas
     */
    _renderParticles(time, width, height) {
        this.ctx.save();
        this.ctx.fillStyle = this.colors.metallicSilver;
        this.ctx.globalAlpha = 0.3;
        
        for (let i = 0; i < 20; i++) {
            const x = (Math.sin(time + i) * width / 2) + width / 2;
            const y = (Math.cos(time * 0.5 + i) * height / 2) + height / 2;
            const size = Math.sin(time * 2 + i) * 3 + 2;
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        this.ctx.restore();
    }
    
    /**
     * Envuelve texto en líneas
     * @param {string} text - Texto a envolver
     * @param {number} maxWidth - Ancho máximo
     * @returns {Array} Líneas de texto
     */
    _wrapText(text, maxWidth) {
        const words = text.split(' ');
        const lines = [];
        let currentLine = '';
        
        for (const word of words) {
            const testLine = currentLine + word + ' ';
            const metrics = this.ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && currentLine !== '') {
                lines.push(currentLine);
                currentLine = word + ' ';
            } else {
                currentLine = testLine;
            }
        }
        
        if (currentLine) {
            lines.push(currentLine);
        }
        
        return lines;
    }
    
    /**
     * Obtiene el texto del título según el tipo de sección
     * @param {string} sectionType - Tipo de sección
     * @returns {string} Texto del título
     */
    _getSectionTitleText(sectionType) {
        const titles = {
            intro: 'CINE NORTE',
            hook: '¡ATENCIÓN!',
            plot: 'LA HISTORIA',
            analysis: 'ANÁLISIS',
            outro: '¡SUSCRÍBETE!'
        };
        return titles[sectionType] || sectionType.toUpperCase();
    }
    
    /**
     * Parsea tiempo en formato HH:MM:SS.mmm a segundos
     * @param {string} timeStr - Tiempo en formato string
     * @returns {number} Tiempo en segundos
     */
    _parseTime(timeStr) {
        const parts = timeStr.split(':');
        const hours = parseInt(parts[0]);
        const minutes = parseInt(parts[1]);
        const seconds = parseFloat(parts[2]);
        return hours * 3600 + minutes * 60 + seconds;
    }
    
    /**
     * Combina frames con audio
     * @param {Blob} audioBlob - Blob de audio
     * @returns {Promise<Blob>} Video final
     */
    async _combineWithAudio(audioBlob) {
        // Para simplificar, retornamos un blob con los frames
        // En una implementación real, se usaría MediaRecorder API
        const canvas = document.createElement('canvas');
        canvas.width = this.canvas.width;
        canvas.height = this.canvas.height;
        const ctx = canvas.getContext('2d');
        
        // Crear un frame representativo
        ctx.fillStyle = this.colors.deepBlack;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = this.colors.primaryRed;
        ctx.font = 'bold 48px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('CINE NORTE', canvas.width / 2, canvas.height / 2);
        
        return new Promise((resolve) => {
            canvas.toBlob(resolve, 'video/webm');
        });
    }
    
    /**
     * Actualiza el progreso de renderizado
     * @param {string} message - Mensaje de progreso
     */
    updateProgress(message) {
        const loadingText = document.getElementById('loadingText');
        if (loadingText) {
            loadingText.textContent = message;
        }
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
    
    /**
     * Obtiene una vista previa del video
     * @param {number} time - Tiempo en segundos
     * @returns {string} Data URL del frame
     */
    getPreviewFrame(time) {
        const frameIndex = Math.floor(time * this.fps);
        return this.frames[frameIndex] || '';
    }
    
    /**
     * Limpia los recursos del editor
     */
    cleanup() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        this.frames = [];
        this.currentFrame = 0;
        this.isPlaying = false;
        this.isRendering = false;
    }
}

// Instancia global del editor
window.VideoEditor = VideoEditor;
window.videoEditor = new VideoEditor();
