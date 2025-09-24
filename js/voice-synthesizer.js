/**
 * Sistema de Síntesis de Voz para Cine Norte
 * Convierte guiones a audio y genera subtítulos sincronizados
 */

class VoiceSynthesizer {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.currentVoice = null;
        this.isPlaying = false;
        this.isPaused = false;
        this.currentUtterance = null;
        this.audioContext = null;
        this.audioBuffer = null;
        this.recorder = null;
        this.audioChunks = [];
        
        this.loadVoices();
        this.initializeAudioContext();
    }
    
    /**
     * Carga las voces disponibles
     */
    loadVoices() {
        this.voices = this.synth.getVoices();
        
        // Si no hay voces cargadas, esperar al evento voiceschanged
        if (this.voices.length === 0) {
            this.synth.addEventListener('voiceschanged', () => {
                this.voices = this.synth.getVoices();
                this.selectDefaultVoice();
            });
        } else {
            this.selectDefaultVoice();
        }
    }
    
    /**
     * Selecciona la voz por defecto
     */
    selectDefaultVoice() {
        // Buscar voces en español
        const spanishVoices = this.voices.filter(voice => 
            voice.lang.startsWith('es') || voice.lang.includes('Spanish')
        );
        
        if (spanishVoices.length > 0) {
            // Preferir voces masculinas para Cine Norte
            const maleVoice = spanishVoices.find(voice => 
                voice.name.toLowerCase().includes('male') || 
                voice.name.toLowerCase().includes('masculino')
            );
            this.currentVoice = maleVoice || spanishVoices[0];
        } else {
            this.currentVoice = this.voices[0] || null;
        }
    }
    
    /**
     * Inicializa el contexto de audio
     */
    async initializeAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (error) {
            console.warn('Web Audio API no soportada:', error);
        }
    }
    
    /**
     * Sintetiza un guion completo a audio
     * @param {Object} script - Guion generado
     * @param {string} voiceProfile - Perfil de voz
     * @returns {Promise<Object>} Resultado de la síntesis
     */
    async synthesizeScript(script, voiceProfile = 'male') {
        try {
            this.showLoading('Generando audio...');
            
            // Configurar perfil de voz
            this.setVoiceProfile(voiceProfile);
            
            // Procesar cada sección del guion
            const audioSegments = [];
            const subtitleCues = [];
            let currentTime = 0;
            
            for (const section of script.sections) {
                const segment = await this._synthesizeSection(section, currentTime);
                if (segment) {
                    audioSegments.push(segment);
                    
                    // Generar subtítulos para la sección
                    const sectionCues = this._generateSubtitlesForSection(section, currentTime);
                    subtitleCues.push(...sectionCues);
                    
                    currentTime += segment.duration;
                }
            }
            
            // Combinar segmentos de audio
            const finalAudio = await this._combineAudioSegments(audioSegments);
            
            this.hideLoading();
            
            return {
                audioBlob: finalAudio,
                subtitles: subtitleCues,
                duration: currentTime,
                segments: audioSegments
            };
            
        } catch (error) {
            console.error('Error sintetizando guion:', error);
            this.hideLoading();
            throw error;
        }
    }
    
    /**
     * Sintetiza una sección individual del guion
     * @param {Object} section - Sección del guion
     * @param {number} startTime - Tiempo de inicio
     * @returns {Promise<Object>} Segmento de audio
     */
    async _synthesizeSection(section, startTime) {
        return new Promise((resolve, reject) => {
            try {
                // Preparar texto para síntesis
                const processedText = this._prepareTextForSynthesis(section.content, section.emphasis_words);
                
                // Crear utterance
                const utterance = new SpeechSynthesisUtterance(processedText);
                
                // Configurar voz
                if (this.currentVoice) {
                    utterance.voice = this.currentVoice;
                }
                
                // Configurar parámetros según el perfil
                this._applyVoiceProfile(utterance, section.emotion);
                
                // Configurar eventos
                utterance.onstart = () => {
                    console.log(`Iniciando síntesis de sección: ${section.type}`);
                };
                
                utterance.onend = () => {
                    const duration = this._estimateDuration(processedText);
                    resolve({
                        type: section.type,
                        text: section.content,
                        duration: duration,
                        startTime: startTime,
                        endTime: startTime + duration,
                        emotion: section.emotion
                    });
                };
                
                utterance.onerror = (event) => {
                    console.error('Error en síntesis:', event.error);
                    reject(new Error(`Error en síntesis: ${event.error}`));
                };
                
                // Iniciar síntesis
                this.synth.speak(utterance);
                
            } catch (error) {
                reject(error);
            }
        });
    }
    
    /**
     * Prepara el texto para síntesis con énfasis
     * @param {string} text - Texto original
     * @param {Array} emphasisWords - Palabras de énfasis
     * @returns {string} Texto procesado
     */
    _prepareTextForSynthesis(text, emphasisWords) {
        let processedText = text;
        
        // Agregar pausas naturales
        processedText = processedText.replace(/([.!?])\s+/g, '$1... ');
        processedText = processedText.replace(/([,;:])\s+/g, '$1... ');
        
        // Agregar énfasis a palabras clave (usando pausas)
        for (const word of emphasisWords) {
            const regex = new RegExp(`\\b${word}\\b`, 'gi');
            processedText = processedText.replace(regex, `... ${word}... `);
        }
        
        return processedText;
    }
    
    /**
     * Aplica perfil de voz y efectos emocionales
     * @param {SpeechSynthesisUtterance} utterance - Utterance a configurar
     * @param {string} emotion - Emoción de la sección
     */
    _applyVoiceProfile(utterance, emotion) {
        const voiceConfig = config.getVoiceConfig('male'); // Usar configuración base
        
        // Configurar velocidad
        utterance.rate = voiceConfig.rate || 0.9;
        
        // Configurar tono
        utterance.pitch = voiceConfig.pitch || 0.8;
        
        // Configurar volumen
        utterance.volume = 1.0;
        
        // Aplicar efectos emocionales
        switch (emotion) {
            case 'excitement':
                utterance.rate *= 1.05;
                utterance.pitch *= 1.1;
                break;
            case 'suspense':
                utterance.rate *= 0.95;
                utterance.pitch *= 0.9;
                break;
            case 'drama':
                utterance.rate *= 0.9;
                utterance.pitch *= 0.8;
                break;
            case 'comedy':
                utterance.rate *= 1.1;
                utterance.pitch *= 1.2;
                break;
        }
    }
    
    /**
     * Estima la duración del texto
     * @param {string} text - Texto a analizar
     * @returns {number} Duración estimada en segundos
     */
    _estimateDuration(text) {
        const wordsPerMinute = 150; // Velocidad promedio de habla
        const wordCount = text.split(' ').length;
        return Math.max(5, (wordCount / wordsPerMinute) * 60);
    }
    
    /**
     * Genera subtítulos para una sección
     * @param {Object} section - Sección del guion
     * @param {number} startTime - Tiempo de inicio
     * @returns {Array} Cues de subtítulos
     */
    _generateSubtitlesForSection(section, startTime) {
        const cues = [];
        const lines = this._splitTextForSubtitles(section.content, section.duration_seconds);
        const lineDuration = section.duration_seconds / lines.length;
        
        lines.forEach((line, index) => {
            if (line.trim()) {
                const cueStart = startTime + (index * lineDuration);
                const cueEnd = cueStart + lineDuration;
                
                cues.push({
                    start_time: this._formatTime(cueStart),
                    end_time: this._formatTime(cueEnd),
                    text: line.trim(),
                    speaker: 'Cine Norte',
                    style: this._getSubtitleStyle(section.type)
                });
            }
        });
        
        return cues;
    }
    
    /**
     * Divide el texto en líneas apropiadas para subtítulos
     * @param {string} text - Texto a dividir
     * @param {number} duration - Duración en segundos
     * @returns {Array} Líneas de subtítulos
     */
    _splitTextForSubtitles(text, duration) {
        // Dividir por oraciones
        const sentences = text.split(/[.!?]+/).filter(s => s.trim());
        
        // Calcular palabras por segundo (aproximadamente 3 palabras por segundo)
        const wordsPerSecond = 3.0;
        const maxWordsPerLine = Math.max(5, Math.floor((duration / sentences.length) * wordsPerSecond));
        
        const lines = [];
        let currentLine = '';
        
        for (const sentence of sentences) {
            const words = sentence.trim().split(' ');
            
            if (currentLine.split(' ').length + words.length <= maxWordsPerLine) {
                if (currentLine) {
                    currentLine += ' ' + sentence.trim();
                } else {
                    currentLine = sentence.trim();
                }
            } else {
                if (currentLine) {
                    lines.push(currentLine);
                }
                currentLine = sentence.trim();
            }
        }
        
        if (currentLine) {
            lines.push(currentLine);
        }
        
        return lines;
    }
    
    /**
     * Obtiene el estilo de subtítulo según el tipo de sección
     * @param {string} sectionType - Tipo de sección
     * @returns {string} Estilo de subtítulo
     */
    _getSubtitleStyle(sectionType) {
        const styles = {
            intro: 'intro_style',
            hook: 'hook_style',
            plot: 'plot_style',
            analysis: 'analysis_style',
            outro: 'outro_style'
        };
        return styles[sectionType] || 'default';
    }
    
    /**
     * Formatea tiempo en formato HH:MM:SS.mmm
     * @param {number} seconds - Segundos
     * @returns {string} Tiempo formateado
     */
    _formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const milliseconds = Math.floor((seconds % 1) * 1000);
        
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`;
    }
    
    /**
     * Combina segmentos de audio
     * @param {Array} segments - Segmentos de audio
     * @returns {Promise<Blob>} Audio combinado
     */
    async _combineAudioSegments(segments) {
        // Para simplificar, retornamos un blob vacío
        // En una implementación real, se usaría Web Audio API para combinar
        const audioData = new Uint8Array(1024); // Datos de audio simulados
        return new Blob([audioData], { type: 'audio/wav' });
    }
    
    /**
     * Establece el perfil de voz
     * @param {string} profile - Perfil de voz
     */
    setVoiceProfile(profile) {
        const voiceConfig = config.getVoiceConfig(profile);
        
        // Buscar voz que coincida con el perfil
        const matchingVoice = this.voices.find(voice => 
            voice.lang.startsWith('es') && 
            (profile === 'female' ? 
                voice.name.toLowerCase().includes('female') || 
                voice.name.toLowerCase().includes('femenino') :
                voice.name.toLowerCase().includes('male') || 
                voice.name.toLowerCase().includes('masculino')
            )
        );
        
        if (matchingVoice) {
            this.currentVoice = matchingVoice;
        }
    }
    
    /**
     * Reproduce audio
     * @param {Blob} audioBlob - Blob de audio
     */
    playAudio(audioBlob) {
        if (this.isPlaying) {
            this.stopAudio();
        }
        
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        
        audio.onplay = () => {
            this.isPlaying = true;
            this.isPaused = false;
        };
        
        audio.onpause = () => {
            this.isPaused = true;
        };
        
        audio.onended = () => {
            this.isPlaying = false;
            this.isPaused = false;
            URL.revokeObjectURL(audioUrl);
        };
        
        audio.play();
        this.currentAudio = audio;
    }
    
    /**
     * Pausa el audio
     */
    pauseAudio() {
        if (this.currentAudio && this.isPlaying) {
            this.currentAudio.pause();
        }
    }
    
    /**
     * Reanuda el audio
     */
    resumeAudio() {
        if (this.currentAudio && this.isPaused) {
            this.currentAudio.play();
        }
    }
    
    /**
     * Detiene el audio
     */
    stopAudio() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.isPlaying = false;
            this.isPaused = false;
        }
    }
    
    /**
     * Exporta subtítulos en formato WebVTT
     * @param {Array} cues - Cues de subtítulos
     * @returns {string} Contenido WebVTT
     */
    exportSubtitlesWebVTT(cues) {
        let vttContent = 'WEBVTT\n\n';
        
        cues.forEach(cue => {
            vttContent += `${cue.start_time} --> ${cue.end_time}\n`;
            vttContent += `${cue.text}\n\n`;
        });
        
        return vttContent;
    }
    
    /**
     * Exporta subtítulos en formato SRT
     * @param {Array} cues - Cues de subtítulos
     * @returns {string} Contenido SRT
     */
    exportSubtitlesSRT(cues) {
        let srtContent = '';
        
        cues.forEach((cue, index) => {
            const startSrt = cue.start_time.replace('.', ',');
            const endSrt = cue.end_time.replace('.', ',');
            
            srtContent += `${index + 1}\n`;
            srtContent += `${startSrt} --> ${endSrt}\n`;
            srtContent += `${cue.text}\n\n`;
        });
        
        return srtContent;
    }
    
    /**
     * Obtiene las voces disponibles
     * @returns {Array} Lista de voces
     */
    getAvailableVoices() {
        return this.voices.map(voice => ({
            name: voice.name,
            lang: voice.lang,
            gender: this._detectVoiceGender(voice.name),
            isDefault: voice.default
        }));
    }
    
    /**
     * Detecta el género de la voz
     * @param {string} voiceName - Nombre de la voz
     * @returns {string} Género detectado
     */
    _detectVoiceGender(voiceName) {
        const name = voiceName.toLowerCase();
        if (name.includes('female') || name.includes('femenino') || name.includes('woman')) {
            return 'female';
        }
        if (name.includes('male') || name.includes('masculino') || name.includes('man')) {
            return 'male';
        }
        return 'unknown';
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
     * Verifica si la síntesis de voz está soportada
     * @returns {boolean} True si está soportada
     */
    isSupported() {
        return 'speechSynthesis' in window;
    }
    
    /**
     * Obtiene el estado actual de reproducción
     * @returns {Object} Estado de reproducción
     */
    getPlaybackState() {
        return {
            isPlaying: this.isPlaying,
            isPaused: this.isPaused,
            currentVoice: this.currentVoice?.name || 'Desconocida'
        };
    }
}

// Instancia global del sintetizador
window.VoiceSynthesizer = VoiceSynthesizer;
window.voiceSynthesizer = new VoiceSynthesizer();
