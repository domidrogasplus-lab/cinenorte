/**
 * Utilidades para Cine Norte
 * Funciones auxiliares y helpers para la aplicación
 */

class Utils {
    constructor() {
        this.notifications = [];
        this.maxNotifications = 5;
    }
    
    /**
     * Muestra una notificación
     * @param {string} message - Mensaje de la notificación
     * @param {string} type - Tipo de notificación (success, warning, error, info)
     * @param {number} duration - Duración en milisegundos
     */
    showNotification(message, type = 'info', duration = 5000) {
        const notification = {
            id: Date.now(),
            message,
            type,
            duration
        };
        
        this.notifications.push(notification);
        this._renderNotification(notification);
        
        // Auto-remover después de la duración especificada
        setTimeout(() => {
            this.removeNotification(notification.id);
        }, duration);
    }
    
    /**
     * Renderiza una notificación en el DOM
     * @param {Object} notification - Objeto de notificación
     */
    _renderNotification(notification) {
        const container = document.getElementById('notifications');
        if (!container) return;
        
        const notificationEl = document.createElement('div');
        notificationEl.className = `notification ${notification.type}`;
        notificationEl.dataset.id = notification.id;
        notificationEl.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${notification.message}</span>
                <button class="notification-close" onclick="utils.removeNotification(${notification.id})">&times;</button>
            </div>
        `;
        
        container.appendChild(notificationEl);
        
        // Limitar número de notificaciones
        if (container.children.length > this.maxNotifications) {
            container.removeChild(container.firstChild);
        }
    }
    
    /**
     * Remueve una notificación
     * @param {number} id - ID de la notificación
     */
    removeNotification(id) {
        const notificationEl = document.querySelector(`[data-id="${id}"]`);
        if (notificationEl) {
            notificationEl.remove();
        }
        
        this.notifications = this.notifications.filter(n => n.id !== id);
    }
    
    /**
     * Muestra indicador de carga
     * @param {string} message - Mensaje de carga
     */
    showLoading(message = 'Procesando...') {
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
     * Actualiza el progreso de carga
     * @param {string} message - Mensaje de progreso
     * @param {number} percentage - Porcentaje de progreso (0-100)
     */
    updateProgress(message, percentage = null) {
        const loadingText = document.getElementById('loadingText');
        
        if (loadingText) {
            if (percentage !== null) {
                loadingText.textContent = `${message} (${percentage}%)`;
            } else {
                loadingText.textContent = message;
            }
        }
    }
    
    /**
     * Formatea tiempo en formato HH:MM:SS
     * @param {number} seconds - Segundos
     * @returns {string} Tiempo formateado
     */
    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }
    
    /**
     * Formatea número con separadores de miles
     * @param {number} number - Número a formatear
     * @returns {string} Número formateado
     */
    formatNumber(number) {
        return new Intl.NumberFormat('es-ES').format(number);
    }
    
    /**
     * Formatea tamaño de archivo
     * @param {number} bytes - Bytes del archivo
     * @returns {string} Tamaño formateado
     */
    formatFileSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Bytes';
        
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    /**
     * Descarga un archivo
     * @param {Blob} blob - Blob del archivo
     * @param {string} filename - Nombre del archivo
     */
    downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    /**
     * Descarga múltiples archivos como ZIP
     * @param {Array} files - Array de objetos {blob, filename}
     * @param {string} zipName - Nombre del archivo ZIP
     */
    async downloadZip(files, zipName = 'cine_norte_files.zip') {
        try {
            // Nota: Para una implementación real, se necesitaría una librería como JSZip
            // Por ahora, descargamos los archivos individualmente
            for (let i = 0; i < files.length; i++) {
                setTimeout(() => {
                    this.downloadFile(files[i].blob, files[i].filename);
                }, i * 1000); // Descargar con 1 segundo de diferencia
            }
            
            this.showNotification('Descargando archivos...', 'info');
        } catch (error) {
            console.error('Error descargando ZIP:', error);
            this.showNotification('Error al crear archivo ZIP', 'error');
        }
    }
    
    /**
     * Valida si un archivo es de tipo de video
     * @param {File} file - Archivo a validar
     * @returns {boolean} True si es video
     */
    isValidVideoFile(file) {
        const videoTypes = ['video/mp4', 'video/webm', 'video/ogg', 'video/avi', 'video/mov'];
        return videoTypes.includes(file.type);
    }
    
    /**
     * Valida si un archivo es de tipo de imagen
     * @param {File} file - Archivo a validar
     * @returns {boolean} True si es imagen
     */
    isValidImageFile(file) {
        const imageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'];
        return imageTypes.includes(file.type);
    }
    
    /**
     * Valida si un archivo es de tipo de audio
     * @param {File} file - Archivo a validar
     * @returns {boolean} True si es audio
     */
    isValidAudioFile(file) {
        const audioTypes = ['audio/mp3', 'audio/wav', 'audio/ogg', 'audio/m4a', 'audio/aac'];
        return audioTypes.includes(file.type);
    }
    
    /**
     * Genera un ID único
     * @returns {string} ID único
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    /**
     * Debounce de función
     * @param {Function} func - Función a debounce
     * @param {number} wait - Tiempo de espera en ms
     * @returns {Function} Función debounced
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    /**
     * Throttle de función
     * @param {Function} func - Función a throttle
     * @param {number} limit - Límite de tiempo en ms
     * @returns {Function} Función throttled
     */
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    /**
     * Copia texto al portapapeles
     * @param {string} text - Texto a copiar
     * @returns {Promise<boolean>} True si se copió exitosamente
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showNotification('Texto copiado al portapapeles', 'success');
            return true;
        } catch (error) {
            console.error('Error copiando al portapapeles:', error);
            this.showNotification('Error al copiar al portapapeles', 'error');
            return false;
        }
    }
    
    /**
     * Lee texto del portapapeles
     * @returns {Promise<string>} Texto del portapapeles
     */
    async readFromClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            return text;
        } catch (error) {
            console.error('Error leyendo del portapapeles:', error);
            return '';
        }
    }
    
    /**
     * Guarda datos en localStorage
     * @param {string} key - Clave
     * @param {any} data - Datos a guardar
     */
    saveToStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.error('Error guardando en localStorage:', error);
        }
    }
    
    /**
     * Lee datos de localStorage
     * @param {string} key - Clave
     * @param {any} defaultValue - Valor por defecto
     * @returns {any} Datos leídos
     */
    loadFromStorage(key, defaultValue = null) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : defaultValue;
        } catch (error) {
            console.error('Error leyendo de localStorage:', error);
            return defaultValue;
        }
    }
    
    /**
     * Remueve datos de localStorage
     * @param {string} key - Clave
     */
    removeFromStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Error removiendo de localStorage:', error);
        }
    }
    
    /**
     * Limpia todos los datos de localStorage
     */
    clearStorage() {
        try {
            localStorage.clear();
            this.showNotification('Datos limpiados', 'info');
        } catch (error) {
            console.error('Error limpiando localStorage:', error);
        }
    }
    
    /**
     * Valida email
     * @param {string} email - Email a validar
     * @returns {boolean} True si es válido
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    /**
     * Valida URL
     * @param {string} url - URL a validar
     * @returns {boolean} True si es válida
     */
    isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }
    
    /**
     * Sanitiza HTML
     * @param {string} html - HTML a sanitizar
     * @returns {string} HTML sanitizado
     */
    sanitizeHtml(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    }
    
    /**
     * Escapa caracteres especiales en HTML
     * @param {string} text - Texto a escapar
     * @returns {string} Texto escapado
     */
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
    
    /**
     * Genera un color aleatorio
     * @returns {string} Color en formato hex
     */
    generateRandomColor() {
        return '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
    }
    
    /**
     * Convierte color hex a RGB
     * @param {string} hex - Color en formato hex
     * @returns {Object} Objeto con r, g, b
     */
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }
    
    /**
     * Convierte RGB a color hex
     * @param {number} r - Componente rojo
     * @param {number} g - Componente verde
     * @param {number} b - Componente azul
     * @returns {string} Color en formato hex
     */
    rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }
    
    /**
     * Calcula la diferencia entre dos fechas
     * @param {Date} date1 - Primera fecha
     * @param {Date} date2 - Segunda fecha
     * @returns {Object} Diferencia en días, horas, minutos, segundos
     */
    getDateDifference(date1, date2) {
        const diff = Math.abs(date2 - date1);
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        return { days, hours, minutes, seconds };
    }
    
    /**
     * Formatea fecha relativa (hace X tiempo)
     * @param {Date} date - Fecha a formatear
     * @returns {string} Fecha relativa formateada
     */
    formatRelativeDate(date) {
        const now = new Date();
        const diff = this.getDateDifference(now, date);
        
        if (diff.days > 0) {
            return `hace ${diff.days} día${diff.days > 1 ? 's' : ''}`;
        } else if (diff.hours > 0) {
            return `hace ${diff.hours} hora${diff.hours > 1 ? 's' : ''}`;
        } else if (diff.minutes > 0) {
            return `hace ${diff.minutes} minuto${diff.minutes > 1 ? 's' : ''}`;
        } else {
            return 'hace unos segundos';
        }
    }
    
    /**
     * Detecta si el dispositivo es móvil
     * @returns {boolean} True si es móvil
     */
    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    /**
     * Detecta si el navegador soporta una característica
     * @param {string} feature - Característica a verificar
     * @returns {boolean} True si está soportada
     */
    supportsFeature(feature) {
        const features = {
            'webgl': () => !!document.createElement('canvas').getContext('webgl'),
            'webgl2': () => !!document.createElement('canvas').getContext('webgl2'),
            'webp': () => {
                const canvas = document.createElement('canvas');
                canvas.width = 1;
                canvas.height = 1;
                return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
            },
            'speech': () => 'speechSynthesis' in window,
            'audio': () => 'AudioContext' in window || 'webkitAudioContext' in window,
            'video': () => !!document.createElement('video').canPlayType,
            'canvas': () => !!document.createElement('canvas').getContext,
            'localStorage': () => {
                try {
                    localStorage.setItem('test', 'test');
                    localStorage.removeItem('test');
                    return true;
                } catch {
                    return false;
                }
            }
        };
        
        return features[feature] ? features[feature]() : false;
    }
    
    /**
     * Obtiene información del navegador
     * @returns {Object} Información del navegador
     */
    getBrowserInfo() {
        const ua = navigator.userAgent;
        const browsers = {
            chrome: /Chrome/.test(ua) && /Google Inc/.test(navigator.vendor),
            firefox: /Firefox/.test(ua),
            safari: /Safari/.test(ua) && /Apple Computer/.test(navigator.vendor),
            edge: /Edg/.test(ua),
            opera: /Opera/.test(ua) || /OPR/.test(ua)
        };
        
        const browser = Object.keys(browsers).find(b => browsers[b]) || 'unknown';
        
        return {
            name: browser,
            version: this._getBrowserVersion(ua, browser),
            userAgent: ua,
            language: navigator.language,
            platform: navigator.platform,
            cookieEnabled: navigator.cookieEnabled,
            onLine: navigator.onLine
        };
    }
    
    /**
     * Obtiene la versión del navegador
     * @param {string} ua - User agent
     * @param {string} browser - Nombre del navegador
     * @returns {string} Versión del navegador
     */
    _getBrowserVersion(ua, browser) {
        const patterns = {
            chrome: /Chrome\/(\d+)/,
            firefox: /Firefox\/(\d+)/,
            safari: /Version\/(\d+)/,
            edge: /Edg\/(\d+)/,
            opera: /(?:Opera|OPR)\/(\d+)/
        };
        
        const match = ua.match(patterns[browser]);
        return match ? match[1] : 'unknown';
    }
    
    /**
     * Limpia recursos y libera memoria
     */
    cleanup() {
        // Limpiar notificaciones
        this.notifications = [];
        const container = document.getElementById('notifications');
        if (container) {
            container.innerHTML = '';
        }
        
        // Limpiar URLs de objetos
        // (En una implementación real, se rastrearían las URLs creadas)
    }
}

// Instancia global de utilidades
window.Utils = Utils;
window.utils = new Utils();
