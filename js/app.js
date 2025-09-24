/**
 * Aplicación Principal de Cine Norte
 * Conecta todos los módulos y maneja la interfaz de usuario
 */

class CineNorteApp {
    constructor() {
        this.currentContent = null;
        this.currentScript = null;
        this.currentVideo = null;
        this.currentAudio = null;
        this.currentSubtitles = null;
        this.currentFormats = [];
        this.currentThumbnails = [];
        this.currentOptimization = null;
        
        this.init();
    }
    
    /**
     * Inicializa la aplicación
     */
    init() {
        this.setupEventListeners();
        this.loadSettings();
        this.checkAPIs();
        this.setupNavigation();
        
        // Mostrar mensaje de bienvenida
        utils.showNotification('¡Bienvenido a Cine Norte!', 'success', 3000);
    }
    
    /**
     * Configura los event listeners
     */
    setupEventListeners() {
        // Navegación
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                this.switchTab(tab);
            });
        });
        
        // Búsqueda de contenido
        document.getElementById('searchBtn')?.addEventListener('click', () => {
            this.searchContent();
        });
        
        document.getElementById('contentSearch')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchContent();
            }
        });
        
        // Contenido trending
        document.getElementById('getTrendingBtn')?.addEventListener('click', () => {
            this.getTrendingContent();
        });
        
        // Generación de guion
        document.getElementById('generateScriptBtn')?.addEventListener('click', () => {
            this.generateScript();
        });
        
        // Generación de video
        document.getElementById('generateVideoBtn')?.addEventListener('click', () => {
            this.generateVideo();
        });
        
        // Análisis de optimización
        document.getElementById('analyzeBtn')?.addEventListener('click', () => {
            this.analyzeOptimization();
        });
        
        // Descargas
        document.getElementById('downloadScript')?.addEventListener('click', () => {
            this.downloadScript();
        });
        
        document.getElementById('downloadAudio')?.addEventListener('click', () => {
            this.downloadAudio();
        });
        
        document.getElementById('downloadSubtitles')?.addEventListener('click', () => {
            this.downloadSubtitles();
        });
        
        document.getElementById('downloadVideo')?.addEventListener('click', () => {
            this.downloadVideo();
        });
        
        document.getElementById('downloadFormats')?.addEventListener('click', () => {
            this.downloadFormats();
        });
        
        document.getElementById('downloadThumbnails')?.addEventListener('click', () => {
            this.downloadThumbnails();
        });
        
        // Configuración
        document.getElementById('settingsBtn')?.addEventListener('click', () => {
            this.showSettingsModal();
        });
        
        document.getElementById('saveSettings')?.addEventListener('click', () => {
            this.saveSettings();
        });
        
        // Ayuda
        document.getElementById('helpBtn')?.addEventListener('click', () => {
            this.showHelpModal();
        });
        
        // Cerrar modales
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.closeModal(e.target.closest('.modal'));
            });
        });
        
        // Cerrar modales al hacer clic fuera
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal);
                }
            });
        });
        
        // Actualizar duración del guion
        document.getElementById('scriptDuration')?.addEventListener('input', (e) => {
            document.getElementById('durationValue').textContent = e.target.value + 's';
        });
    }
    
    /**
     * Carga la configuración guardada
     */
    loadSettings() {
        const openaiKey = utils.loadFromStorage('openai_key', '');
        const tmdbKey = utils.loadFromStorage('tmdb_key', '');
        
        if (openaiKey) {
            config.set('apis.openai.key', openaiKey);
            document.getElementById('openaiKey').value = openaiKey;
        }
        
        if (tmdbKey) {
            config.set('apis.tmdb.key', tmdbKey);
            document.getElementById('tmdbKey').value = tmdbKey;
        }
    }
    
    /**
     * Verifica el estado de las APIs
     */
    checkAPIs() {
        const apiStatus = config.checkAPIs();
        
        if (!apiStatus.openai) {
            utils.showNotification('Configura tu clave de OpenAI para generar guiones', 'warning');
        }
        
        if (!apiStatus.tmdb) {
            utils.showNotification('Configura tu clave de TMDB para análisis de contenido', 'warning');
        }
    }
    
    /**
     * Configura la navegación
     */
    setupNavigation() {
        // Activar primera pestaña por defecto
        this.switchTab('content-analysis');
    }
    
    /**
     * Cambia de pestaña
     * @param {string} tabId - ID de la pestaña
     */
    switchTab(tabId) {
        // Ocultar todas las pestañas
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Desactivar todos los botones de navegación
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Mostrar pestaña seleccionada
        const targetTab = document.getElementById(tabId);
        if (targetTab) {
            targetTab.classList.add('active');
        }
        
        // Activar botón de navegación
        const targetBtn = document.querySelector(`[data-tab="${tabId}"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
    }
    
    /**
     * Busca contenido
     */
    async searchContent() {
        const query = document.getElementById('contentSearch').value.trim();
        const type = document.getElementById('contentType').value;
        
        if (!query) {
            utils.showNotification('Ingresa un término de búsqueda', 'warning');
            return;
        }
        
        try {
            utils.showLoading('Buscando contenido...');
            
            const results = await contentAnalyzer.searchContent(query, type);
            
            if (results.length > 0) {
                this.displaySearchResults(results);
                utils.showNotification(`Encontrados ${results.length} resultados`, 'success');
            } else {
                utils.showNotification('No se encontraron resultados', 'warning');
            }
            
        } catch (error) {
            console.error('Error buscando contenido:', error);
            utils.showNotification('Error buscando contenido: ' + error.message, 'error');
        } finally {
            utils.hideLoading();
        }
    }
    
    /**
     * Muestra resultados de búsqueda
     * @param {Array} results - Resultados de búsqueda
     */
    displaySearchResults(results) {
        const container = document.getElementById('searchResults');
        if (!container) return;
        
        container.innerHTML = '';
        
        results.forEach((content, index) => {
            const card = this.createContentCard(content, index);
            container.appendChild(card);
        });
    }
    
    /**
     * Crea una tarjeta de contenido
     * @param {Object} content - Información del contenido
     * @param {number} index - Índice del contenido
     * @returns {HTMLElement} Elemento de la tarjeta
     */
    createContentCard(content, index) {
        const card = document.createElement('div');
        card.className = 'content-card';
        card.innerHTML = `
            <div class="content-poster">
                ${content.poster_url ? 
                    `<img src="${content.poster_url}" alt="${content.title}" loading="lazy">` :
                    '<div class="no-poster">🎬</div>'
                }
            </div>
            <div class="content-info">
                <h3 class="content-title">${content.title}</h3>
                <div class="content-meta">
                    <span class="content-rating">⭐ ${content.rating}/10</span>
                    <span class="content-platform">📺 ${content.platform}</span>
                </div>
                <div class="content-genres">${content.genre.join(', ')}</div>
                <p class="content-overview">${content.overview}</p>
                <button class="btn btn-primary" onclick="app.selectContent(${index})">
                    Seleccionar
                </button>
            </div>
        `;
        
        return card;
    }
    
    /**
     * Selecciona contenido
     * @param {number} index - Índice del contenido
     */
    selectContent(index) {
        const results = document.querySelectorAll('.content-card');
        if (results[index]) {
            const content = this.extractContentFromCard(results[index]);
            this.currentContent = content;
            this.displaySelectedContent(content);
            utils.showNotification(`Contenido seleccionado: ${content.title}`, 'success');
        }
    }
    
    /**
     * Extrae información del contenido de una tarjeta
     * @param {HTMLElement} card - Tarjeta del contenido
     * @returns {Object} Información del contenido
     */
    extractContentFromCard(card) {
        const title = card.querySelector('.content-title').textContent;
        const rating = parseFloat(card.querySelector('.content-rating').textContent.match(/\d+\.?\d*/)[0]);
        const platform = card.querySelector('.content-platform').textContent.replace('📺 ', '');
        const genres = card.querySelector('.content-genres').textContent.split(', ');
        const overview = card.querySelector('.content-overview').textContent;
        
        return {
            title,
            rating,
            platform,
            genre: genres,
            overview,
            content_type: 'movie', // Por defecto
            popularity: 50, // Valor por defecto
            release_date: new Date().toISOString().split('T')[0]
        };
    }
    
    /**
     * Muestra contenido seleccionado
     * @param {Object} content - Información del contenido
     */
    displaySelectedContent(content) {
        const container = document.getElementById('selectedContent');
        if (!container) return;
        
        container.innerHTML = `
            <h3>✅ Contenido Seleccionado</h3>
            <div class="selected-content-info">
                <h4>${content.title}</h4>
                <p><strong>Tipo:</strong> ${content.content_type.toUpperCase()}</p>
                <p><strong>Plataforma:</strong> ${content.platform}</p>
                <p><strong>Géneros:</strong> ${content.genre.join(', ')}</p>
                <p><strong>Rating:</strong> ${content.rating}/10</p>
                <p><strong>Sinopsis:</strong> ${content.overview}</p>
            </div>
        `;
    }
    
    /**
     * Obtiene contenido trending
     */
    async getTrendingContent() {
        try {
            utils.showLoading('Obteniendo contenido trending...');
            
            const trending = await contentAnalyzer.getTrendingContent();
            
            if (trending.length > 0) {
                this.displayTrendingContent(trending);
                utils.showNotification(`Obtenidos ${trending.length} contenidos trending`, 'success');
            } else {
                utils.showNotification('No se pudo obtener contenido trending', 'warning');
            }
            
        } catch (error) {
            console.error('Error obteniendo contenido trending:', error);
            utils.showNotification('Error obteniendo contenido trending: ' + error.message, 'error');
        } finally {
            utils.hideLoading();
        }
    }
    
    /**
     * Muestra contenido trending
     * @param {Array} trending - Contenido trending
     */
    displayTrendingContent(trending) {
        const container = document.getElementById('trendingContent');
        if (!container) return;
        
        container.innerHTML = '';
        
        trending.forEach((content, index) => {
            const card = this.createTrendingCard(content, index);
            container.appendChild(card);
        });
    }
    
    /**
     * Crea una tarjeta de contenido trending
     * @param {Object} content - Información del contenido
     * @param {number} index - Índice del contenido
     * @returns {HTMLElement} Elemento de la tarjeta
     */
    createTrendingCard(content, index) {
        const card = document.createElement('div');
        card.className = 'content-card trending-card';
        card.innerHTML = `
            <div class="content-info">
                <h4>${content.title}</h4>
                <p>⭐ ${content.rating}/10 | 📺 ${content.platform}</p>
                <p>🎭 ${content.genre.slice(0, 2).join(', ')}</p>
                <button class="btn btn-secondary" onclick="app.selectTrendingContent(${index})">
                    Seleccionar
                </button>
            </div>
        `;
        
        return card;
    }
    
    /**
     * Selecciona contenido trending
     * @param {number} index - Índice del contenido
     */
    selectTrendingContent(index) {
        const cards = document.querySelectorAll('.trending-card');
        if (cards[index]) {
            const content = this.extractTrendingContentFromCard(cards[index]);
            this.currentContent = content;
            this.displaySelectedContent(content);
            utils.showNotification(`Contenido seleccionado: ${content.title}`, 'success');
        }
    }
    
    /**
     * Extrae información del contenido trending de una tarjeta
     * @param {HTMLElement} card - Tarjeta del contenido
     * @returns {Object} Información del contenido
     */
    extractTrendingContentFromCard(card) {
        const title = card.querySelector('h4').textContent;
        const ratingText = card.querySelector('p').textContent;
        const rating = parseFloat(ratingText.match(/\d+\.?\d*/)[0]);
        const platform = ratingText.split('|')[1].trim().replace('📺 ', '');
        const genres = card.querySelectorAll('p')[1].textContent.replace('🎭 ', '').split(', ');
        
        return {
            title,
            rating,
            platform,
            genre: genres,
            content_type: 'movie',
            popularity: 75,
            overview: 'Contenido trending',
            release_date: new Date().toISOString().split('T')[0]
        };
    }
    
    /**
     * Genera guion
     */
    async generateScript() {
        if (!this.currentContent) {
            utils.showNotification('Primero selecciona un contenido', 'warning');
            return;
        }
        
        try {
            const platform = document.getElementById('scriptPlatform').value;
            const style = document.getElementById('scriptStyle').value;
            const duration = parseInt(document.getElementById('scriptDuration').value);
            const includeSpoilers = document.getElementById('includeSpoilers').checked;
            
            utils.showLoading('Generando guion con IA...');
            
            const script = await scriptGenerator.generateScript(
                this.currentContent,
                platform,
                duration,
                style
            );
            
            this.currentScript = script;
            this.displayScript(script);
            utils.showNotification('Guion generado exitosamente', 'success');
            
        } catch (error) {
            console.error('Error generando guion:', error);
            utils.showNotification('Error generando guion: ' + error.message, 'error');
        } finally {
            utils.hideLoading();
        }
    }
    
    /**
     * Muestra el guion generado
     * @param {Object} script - Guion generado
     */
    displayScript(script) {
        const container = document.getElementById('scriptResults');
        if (!container) return;
        
        container.innerHTML = `
            <div class="script-meta">
                <div class="meta-item">
                    <div class="meta-value">${script.total_duration}s</div>
                    <div class="meta-label">Duración</div>
                </div>
                <div class="meta-item">
                    <div class="meta-value">${script.word_count}</div>
                    <div class="meta-label">Palabras</div>
                </div>
                <div class="meta-item">
                    <div class="meta-value">${script.sections.length}</div>
                    <div class="meta-label">Secciones</div>
                </div>
                <div class="meta-item">
                    <div class="meta-value">${script.target_platform.toUpperCase()}</div>
                    <div class="meta-label">Plataforma</div>
                </div>
            </div>
            
            <div class="script-content">
                <h3>Guion Completo</h3>
                <div class="script-text">${script.raw_text}</div>
            </div>
            
            <div class="script-sections">
                ${script.sections.map((section, index) => `
                    <div class="script-section">
                        <h4 class="section-header-small">Sección ${index + 1}: ${section.type.toUpperCase()}</h4>
                        <div class="section-content">${section.content}</div>
                        <div class="section-meta">
                            <span>Duración: ${section.duration_seconds}s</span>
                            <span>Emoción: ${section.emotion}</span>
                            <span>Indicaciones: ${section.visual_cues.join(', ')}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    /**
     * Genera video
     */
    async generateVideo() {
        if (!this.currentScript) {
            utils.showNotification('Primero genera un guion', 'warning');
            return;
        }
        
        try {
            const style = document.getElementById('videoStyle').value;
            const voiceProfile = document.getElementById('voiceProfile').value;
            const quality = document.getElementById('videoQuality').value;
            const includeSubtitles = document.getElementById('includeSubtitles').checked;
            const includeMusic = document.getElementById('includeMusic').checked;
            
            utils.showLoading('Generando audio y video...');
            
            // Generar audio
            const audioResult = await voiceSynthesizer.synthesizeScript(
                this.currentScript,
                voiceProfile,
                'mp3'
            );
            
            this.currentAudio = audioResult.audioBlob;
            this.currentSubtitles = audioResult.subtitles;
            
            // Generar video
            const videoBlob = await videoEditor.createVideo(
                this.currentScript,
                this.currentAudio,
                this.currentSubtitles,
                this.currentScript.target_platform,
                style
            );
            
            this.currentVideo = videoBlob;
            this.displayVideo(videoBlob);
            
            // Generar formatos múltiples
            await this.generateFormats(videoBlob);
            
            utils.showNotification('Video generado exitosamente', 'success');
            
        } catch (error) {
            console.error('Error generando video:', error);
            utils.showNotification('Error generando video: ' + error.message, 'error');
        } finally {
            utils.hideLoading();
        }
    }
    
    /**
     * Muestra el video generado
     * @param {Blob} videoBlob - Video generado
     */
    displayVideo(videoBlob) {
        const container = document.getElementById('videoResults');
        if (!container) return;
        
        const videoUrl = URL.createObjectURL(videoBlob);
        
        container.innerHTML = `
            <div class="video-player">
                <video controls width="100%">
                    <source src="${videoUrl}" type="video/webm">
                    Tu navegador no soporta el elemento video.
                </video>
            </div>
            <div class="video-meta">
                <div class="meta-item">
                    <div class="meta-value">${this.currentScript.total_duration}s</div>
                    <div class="meta-label">Duración</div>
                </div>
                <div class="meta-item">
                    <div class="meta-value">${this.currentScript.target_platform.toUpperCase()}</div>
                    <div class="meta-label">Formato</div>
                </div>
                <div class="meta-item">
                    <div class="meta-value">1080p</div>
                    <div class="meta-label">Calidad</div>
                </div>
            </div>
        `;
    }
    
    /**
     * Genera formatos múltiples
     * @param {Blob} videoBlob - Video fuente
     */
    async generateFormats(videoBlob) {
        try {
            const contentInfo = {
                title: this.currentScript.title,
                platform: this.currentScript.content.platform,
                content_type: this.currentScript.content.content_type
            };
            
            const formats = await formatGenerator.generateAllFormats(
                videoBlob,
                this.currentScript.title,
                contentInfo
            );
            
            this.currentFormats = formats;
            this.displayFormats(formats);
            
        } catch (error) {
            console.error('Error generando formatos:', error);
            utils.showNotification('Error generando formatos: ' + error.message, 'error');
        }
    }
    
    /**
     * Muestra formatos generados
     * @param {Array} formats - Formatos generados
     */
    displayFormats(formats) {
        const container = document.getElementById('formatGeneration');
        if (!container) return;
        
        container.innerHTML = `
            <h3>📱 Formatos Múltiples</h3>
            <div class="format-grid">
                ${formats.map(format => `
                    <div class="format-card">
                        <div class="format-thumbnail">
                            <img src="${URL.createObjectURL(format.thumbnail_blob)}" alt="${format.format_type}">
                        </div>
                        <h4 class="format-title">${format.format_type.toUpperCase()}</h4>
                        <div class="format-info">
                            <p>${format.metadata.dimensions}</p>
                            <p>Score: ${format.optimization_score.toFixed(1)}/100</p>
                        </div>
                        <button class="btn btn-download" onclick="app.downloadFormat('${format.format_type}')">
                            Descargar
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    /**
     * Analiza optimización
     */
    async analyzeOptimization() {
        if (!this.currentScript) {
            utils.showNotification('Primero genera un guion', 'warning');
            return;
        }
        
        try {
            utils.showLoading('Analizando con IA...');
            
            const analysis = await aiOptimizer.optimizeContent(
                this.currentScript,
                this.currentScript.content,
                this.currentVideo
            );
            
            this.currentOptimization = analysis;
            this.displayOptimization(analysis);
            utils.showNotification('Análisis completado', 'success');
            
        } catch (error) {
            console.error('Error analizando optimización:', error);
            utils.showNotification('Error en el análisis: ' + error.message, 'error');
        } finally {
            utils.hideLoading();
        }
    }
    
    /**
     * Muestra análisis de optimización
     * @param {Object} analysis - Análisis de optimización
     */
    displayOptimization(analysis) {
        const container = document.getElementById('optimizationResults');
        if (!container) return;
        
        container.innerHTML = `
            <div class="optimization-metrics">
                <div class="metric-card">
                    <div class="metric-value">${analysis.overall_score.toFixed(1)}</div>
                    <div class="metric-label">Score General</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.engagement_potential.toFixed(1)}</div>
                    <div class="metric-label">Engagement</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.viral_probability.toFixed(1)}</div>
                    <div class="metric-label">Viralidad</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.seo_score.toFixed(1)}</div>
                    <div class="metric-label">SEO</div>
                </div>
            </div>
            
            <div class="recommendations">
                <h4>🎯 Recomendaciones</h4>
                <ul>
                    ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
            
            ${analysis.improvements.length > 0 ? `
                <div class="recommendations">
                    <h4>🔧 Mejoras Sugeridas</h4>
                    <ul>
                        ${analysis.improvements.map(imp => `<li>${imp}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
    }
    
    /**
     * Descarga guion
     */
    downloadScript() {
        if (!this.currentScript) {
            utils.showNotification('No hay guion para descargar', 'warning');
            return;
        }
        
        const content = scriptGenerator.exportScriptToText(this.currentScript);
        const blob = new Blob([content], { type: 'text/plain' });
        const filename = `guion_${this.currentScript.title.replace(/\s+/g, '_')}.txt`;
        
        utils.downloadFile(blob, filename);
    }
    
    /**
     * Descarga audio
     */
    downloadAudio() {
        if (!this.currentAudio) {
            utils.showNotification('No hay audio para descargar', 'warning');
            return;
        }
        
        const filename = `audio_${this.currentScript.title.replace(/\s+/g, '_')}.mp3`;
        utils.downloadFile(this.currentAudio, filename);
    }
    
    /**
     * Descarga subtítulos
     */
    downloadSubtitles() {
        if (!this.currentSubtitles) {
            utils.showNotification('No hay subtítulos para descargar', 'warning');
            return;
        }
        
        const vttContent = voiceSynthesizer.exportSubtitlesWebVTT(this.currentSubtitles);
        const blob = new Blob([vttContent], { type: 'text/vtt' });
        const filename = `subtitulos_${this.currentScript.title.replace(/\s+/g, '_')}.vtt`;
        
        utils.downloadFile(blob, filename);
    }
    
    /**
     * Descarga video
     */
    downloadVideo() {
        if (!this.currentVideo) {
            utils.showNotification('No hay video para descargar', 'warning');
            return;
        }
        
        const filename = `video_${this.currentScript.title.replace(/\s+/g, '_')}.webm`;
        utils.downloadFile(this.currentVideo, filename);
    }
    
    /**
     * Descarga formatos
     */
    downloadFormats() {
        if (this.currentFormats.length === 0) {
            utils.showNotification('No hay formatos para descargar', 'warning');
            return;
        }
        
        const files = this.currentFormats.map(format => ({
            blob: format.video_blob,
            filename: `${this.currentScript.title.replace(/\s+/g, '_')}_${format.format_type}.webm`
        }));
        
        utils.downloadZip(files, 'formatos_cine_norte.zip');
    }
    
    /**
     * Descarga miniaturas
     */
    downloadThumbnails() {
        if (this.currentFormats.length === 0) {
            utils.showNotification('No hay miniaturas para descargar', 'warning');
            return;
        }
        
        const files = this.currentFormats.map(format => ({
            blob: format.thumbnail_blob,
            filename: `thumbnail_${this.currentScript.title.replace(/\s+/g, '_')}_${format.format_type}.jpg`
        }));
        
        utils.downloadZip(files, 'miniaturas_cine_norte.zip');
    }
    
    /**
     * Descarga formato específico
     * @param {string} formatType - Tipo de formato
     */
    downloadFormat(formatType) {
        const format = this.currentFormats.find(f => f.format_type === formatType);
        if (format) {
            const filename = `${this.currentScript.title.replace(/\s+/g, '_')}_${formatType}.webm`;
            utils.downloadFile(format.video_blob, filename);
        }
    }
    
    /**
     * Muestra modal de configuración
     */
    showSettingsModal() {
        const modal = document.getElementById('settingsModal');
        if (modal) {
            modal.classList.add('active');
        }
    }
    
    /**
     * Guarda configuración
     */
    saveSettings() {
        const openaiKey = document.getElementById('openaiKey').value;
        const tmdbKey = document.getElementById('tmdbKey').value;
        
        if (openaiKey) {
            config.set('apis.openai.key', openaiKey);
            utils.saveToStorage('openai_key', openaiKey);
        }
        
        if (tmdbKey) {
            config.set('apis.tmdb.key', tmdbKey);
            utils.saveToStorage('tmdb_key', tmdbKey);
        }
        
        this.closeModal(document.getElementById('settingsModal'));
        utils.showNotification('Configuración guardada', 'success');
    }
    
    /**
     * Muestra modal de ayuda
     */
    showHelpModal() {
        const modal = document.getElementById('helpModal');
        if (modal) {
            modal.classList.add('active');
        }
    }
    
    /**
     * Cierra un modal
     * @param {HTMLElement} modal - Modal a cerrar
     */
    closeModal(modal) {
        if (modal) {
            modal.classList.remove('active');
        }
    }
    
    /**
     * Limpia todos los datos
     */
    cleanup() {
        this.currentContent = null;
        this.currentScript = null;
        this.currentVideo = null;
        this.currentAudio = null;
        this.currentSubtitles = null;
        this.currentFormats = [];
        this.currentThumbnails = [];
        this.currentOptimization = null;
        
        // Limpiar contenedores
        document.getElementById('searchResults').innerHTML = '';
        document.getElementById('selectedContent').innerHTML = '';
        document.getElementById('scriptResults').innerHTML = '';
        document.getElementById('videoResults').innerHTML = '';
        document.getElementById('formatGeneration').innerHTML = '';
        document.getElementById('optimizationResults').innerHTML = '';
        
        utils.cleanup();
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CineNorteApp();
});

// Exportar para uso global
window.CineNorteApp = CineNorteApp;
