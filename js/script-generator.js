/**
 * Generador de Guiones con IA para Cine Norte
 * Crea guiones optimizados para videos de redes sociales
 */

class ScriptGenerator {
    constructor() {
        this.openaiBaseUrl = 'https://api.openai.com/v1';
        this.cache = new Map();
    }
    
    /**
     * Genera un guion completo para el contenido
     * @param {Object} content - Información del contenido
     * @param {string} targetPlatform - Plataforma objetivo
     * @param {number} durationTarget - Duración objetivo en segundos
     * @param {string} style - Estilo del guion
     * @returns {Promise<Object>} Guion generado
     */
    async generateScript(content, targetPlatform = 'youtube', durationTarget = 120, style = 'dynamic') {
        try {
            const apiKey = config.get('apis.openai.key');
            if (!apiKey) {
                throw new Error('OpenAI API key no configurada');
            }
            
            // Crear prompt base
            const prompt = this._createBasePrompt(content, targetPlatform, durationTarget, style);
            
            // Generar guion con OpenAI
            const response = await fetch(`${this.openaiBaseUrl}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'gpt-4',
                    messages: [
                        {
                            role: 'system',
                            content: this._getSystemPrompt()
                        },
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    max_tokens: 2000,
                    temperature: 0.7
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(`Error OpenAI: ${error.error?.message || 'Error desconocido'}`);
            }
            
            const data = await response.json();
            const scriptText = data.choices[0].message.content;
            
            // Procesar y estructurar el guion
            const sections = this._parseScriptSections(scriptText, content);
            
            // Generar metadatos adicionales
            const hashtags = config.generateHashtags(content, targetPlatform);
            const titleSuggestions = this._generateTitleSuggestions(content, targetPlatform);
            const visualStyle = this._determineVisualStyle(content, style);
            const musicSuggestion = this._suggestMusic(content, style);
            
            // Calcular duración total
            const totalDuration = sections.reduce((sum, section) => sum + section.duration_seconds, 0);
            
            return {
                title: content.title,
                content: content,
                sections: sections,
                total_duration: totalDuration,
                word_count: scriptText.split(' ').length,
                target_platform: targetPlatform,
                hashtags: hashtags,
                title_suggestions: titleSuggestions,
                visual_style: visualStyle,
                music_suggestion: musicSuggestion,
                raw_text: scriptText,
                generated_at: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('Error generando guion:', error);
            return this._createFallbackScript(content, targetPlatform);
        }
    }
    
    /**
     * Crea el prompt base para la generación
     * @param {Object} content - Información del contenido
     * @param {string} targetPlatform - Plataforma objetivo
     * @param {number} durationTarget - Duración objetivo
     * @param {string} style - Estilo del guion
     * @returns {string} Prompt completo
     */
    _createBasePrompt(content, targetPlatform, durationTarget, style) {
        const platformInstructions = {
            youtube: 'Optimizado para YouTube: guion más largo, análisis detallado, intros/outros elaborados',
            tiktok: 'Optimizado para TikTok: guion corto y directo, hooks inmediatos, ritmo acelerado',
            instagram: 'Optimizado para Instagram: visual, estético, historias en highlights',
            facebook: 'Optimizado para Facebook: contenido compartible, engagement alto',
            twitter: 'Optimizado para Twitter: conciso, impactante, fácil de compartir'
        };
        
        const styleInstructions = {
            dynamic: 'Estilo dinámico: ritmo rápido, cortes frecuentes, mucha energía',
            dramatic: 'Estilo dramático: pausas estratégicas, énfasis emocional, tensión',
            comedic: 'Estilo cómico: humor sutil, comentarios ingeniosos, tono ligero',
            analytical: 'Estilo analítico: enfoque en técnica, dirección, actuaciones'
        };
        
        return `
Crea un guion para un video de Cine Norte sobre:

TÍTULO: ${content.title}
TIPO: ${content.content_type.toUpperCase()}
GÉNERO: ${content.genre.join(', ')}
PLATAFORMA: ${content.platform}
RATING: ${content.rating}/10
SINOPSIS: ${content.overview}
FECHA DE ESTRENO: ${content.release_date}
DURACIÓN OBJETIVO: ${durationTarget} segundos

INSTRUCCIONES ESPECÍFICAS:
- Plataforma: ${platformInstructions[targetPlatform] || 'General'}
- Estilo: ${styleInstructions[style] || 'Dinámico'}
- Duración máxima: 3 minutos
- Idioma: Español (México)
- Sin spoilers importantes

ESTRUCTURA REQUERIDA:
1. INTRO (5-10 seg): Hook inmediato + presentación Cine Norte
2. HOOK (10-15 seg): Elemento más atractivo sin spoilers
3. PLOT (60-90 seg): Resumen de trama con análisis
4. ANÁLISIS (30-45 seg): Aspectos técnicos o temáticos
5. OUTRO (10-15 seg): Call-to-action + despedida

Para cada sección incluye:
- Texto del guion
- Duración estimada en segundos
- Indicaciones visuales específicas
- Palabras clave para énfasis
- Emoción objetivo

Formato de respuesta en JSON estructurado.
        `.trim();
    }
    
    /**
     * Obtiene el prompt del sistema para la IA
     * @returns {string} Prompt del sistema
     */
    _getSystemPrompt() {
        return `
Eres un experto editor audiovisual y creador de contenido para Cine Norte, 
una marca especializada en análisis cinematográfico para redes sociales.

Tu misión es crear guiones dinámicos, atractivos y optimizados para engagement
que mantengan la identidad de marca de Cine Norte.

Características de Cine Norte:
- Paleta de colores: Rojo #E50914, Negro #0A0A0A, Plateado #C0C0C0
- Estilo: Cinematográfico, profesional, con toque de misterio
- Audiencia: Cinéfilos, amantes del entretenimiento, usuarios de redes sociales
- Duración: Máximo 3 minutos por video

Reglas importantes:
1. NO reveles spoilers importantes de la trama
2. Mantén un tono dinámico y emocionante
3. Incluye elementos visuales y de audio específicos
4. Optimiza para la plataforma objetivo
5. Usa lenguaje natural y conversacional
6. Incluye call-to-actions para engagement

Responde SOLO con un JSON válido que contenga:
{
  "sections": [
    {
      "type": "intro|hook|plot|analysis|outro",
      "content": "texto del guion",
      "duration_seconds": 30,
      "visual_cues": ["indicación1", "indicación2"],
      "emotion": "excitement|suspense|drama|comedy|neutral",
      "emphasis_words": ["palabra1", "palabra2"]
    }
  ]
}
        `.trim();
    }
    
    /**
     * Parsea las secciones del guion desde el texto generado
     * @param {string} scriptText - Texto del guion
     * @param {Object} content - Información del contenido
     * @returns {Array} Secciones del guion
     */
    _parseScriptSections(scriptText, content) {
        try {
            // Intentar extraer JSON del texto
            const jsonMatch = scriptText.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                const data = JSON.parse(jsonMatch[0]);
                return data.sections || [];
            }
        } catch (error) {
            console.warn('Error parseando JSON del guion:', error);
        }
        
        // Fallback: parsear texto plano
        return this._parseTextSections(scriptText, content);
    }
    
    /**
     * Parsea secciones desde texto plano
     * @param {string} scriptText - Texto del guion
     * @param {Object} content - Información del contenido
     * @returns {Array} Secciones del guion
     */
    _parseTextSections(scriptText, content) {
        const sections = [];
        const lines = scriptText.split('\n').filter(line => line.trim());
        
        let currentSection = null;
        let currentContent = [];
        
        for (const line of lines) {
            const trimmedLine = line.trim();
            
            // Detectar inicio de nueva sección
            if (this._isSectionHeader(trimmedLine)) {
                // Guardar sección anterior
                if (currentSection && currentContent.length > 0) {
                    sections.push(this._createSectionFromText(
                        currentSection, 
                        currentContent.join('\n'),
                        content
                    ));
                }
                
                // Iniciar nueva sección
                currentSection = this._extractSectionType(trimmedLine);
                currentContent = [];
            } else if (currentSection && trimmedLine) {
                currentContent.push(trimmedLine);
            }
        }
        
        // Agregar última sección
        if (currentSection && currentContent.length > 0) {
            sections.push(this._createSectionFromText(
                currentSection,
                currentContent.join('\n'),
                content
            ));
        }
        
        // Si no se detectaron secciones, crear una sección general
        if (sections.length === 0) {
            sections.push(this._createSectionFromText(
                'plot',
                scriptText,
                content
            ));
        }
        
        return sections;
    }
    
    /**
     * Verifica si una línea es un encabezado de sección
     * @param {string} line - Línea a verificar
     * @returns {boolean} True si es encabezado
     */
    _isSectionHeader(line) {
        const sectionPatterns = [
            /^(?:INTRO|INTRODUCCIÓN)/i,
            /^(?:HOOK|GANCHO)/i,
            /^(?:PLOT|TRAMA|SINOPSIS)/i,
            /^(?:ANÁLISIS|ANALISIS)/i,
            /^(?:OUTRO|CIERRE|CONCLUSIÓN)/i
        ];
        
        return sectionPatterns.some(pattern => pattern.test(line));
    }
    
    /**
     * Extrae el tipo de sección de una línea
     * @param {string} line - Línea con encabezado
     * @returns {string} Tipo de sección
     */
    _extractSectionType(line) {
        if (/^(?:INTRO|INTRODUCCIÓN)/i.test(line)) return 'intro';
        if (/^(?:HOOK|GANCHO)/i.test(line)) return 'hook';
        if (/^(?:PLOT|TRAMA|SINOPSIS)/i.test(line)) return 'plot';
        if (/^(?:ANÁLISIS|ANALISIS)/i.test(line)) return 'analysis';
        if (/^(?:OUTRO|CIERRE|CONCLUSIÓN)/i.test(line)) return 'outro';
        return 'plot';
    }
    
    /**
     * Crea una sección desde texto plano
     * @param {string} sectionType - Tipo de sección
     * @param {string} content - Contenido de la sección
     * @param {Object} contentInfo - Información del contenido
     * @returns {Object} Sección del guion
     */
    _createSectionFromText(sectionType, content, contentInfo) {
        const wordCount = content.split(' ').length;
        const duration = Math.max(10, Math.round((wordCount / 150) * 60)); // 150 palabras por minuto
        
        const emotionMap = {
            intro: 'excitement',
            hook: 'suspense',
            plot: 'drama',
            analysis: 'neutral',
            outro: 'excitement'
        };
        
        return {
            type: sectionType,
            content: content,
            duration_seconds: duration,
            visual_cues: this._generateVisualCues(sectionType),
            emotion: emotionMap[sectionType] || 'neutral',
            emphasis_words: this._extractEmphasisWords(content)
        };
    }
    
    /**
     * Genera indicaciones visuales para una sección
     * @param {string} sectionType - Tipo de sección
     * @returns {Array} Indicaciones visuales
     */
    _generateVisualCues(sectionType) {
        const cues = {
            intro: ['Logo Cine Norte animado', 'Efecto de luces de reflector', 'Transición dinámica'],
            hook: ['Clip más impactante del tráiler', 'Texto en pantalla con título', 'Efecto de zoom dramático'],
            plot: ['Montaje de escenas clave', 'Texto descriptivo superpuesto', 'Transiciones suaves'],
            analysis: ['Split screen con comparaciones', 'Gráficos informativos', 'Efectos de partículas'],
            outro: ['Logo Cine Norte final', 'Call-to-action visual', 'Fade out elegante']
        };
        
        return cues[sectionType] || ['Elementos visuales dinámicos'];
    }
    
    /**
     * Extrae palabras de énfasis del texto
     * @param {string} text - Texto a analizar
     * @returns {Array} Palabras de énfasis
     */
    _extractEmphasisWords(text) {
        const emphasisPatterns = [
            /\b(?:increíble|espectacular|impresionante|sorprendente)\b/gi,
            /\b(?:nunca|siempre|definitivamente|absolutamente)\b/gi,
            /\b(?:¡.*!)\b/g,
            /\b(?:más|mejor|peor|único|especial)\b/gi
        ];
        
        const emphasisWords = [];
        for (const pattern of emphasisPatterns) {
            const matches = text.match(pattern);
            if (matches) {
                emphasisWords.push(...matches);
            }
        }
        
        return [...new Set(emphasisWords)].slice(0, 5);
    }
    
    /**
     * Genera sugerencias de títulos optimizados
     * @param {Object} content - Información del contenido
     * @param {string} targetPlatform - Plataforma objetivo
     * @returns {Array} Sugerencias de títulos
     */
    _generateTitleSuggestions(content, targetPlatform) {
        const baseTitle = content.title;
        const suggestions = [
            `¿Vale la pena ver ${baseTitle}? | Análisis Cine Norte`,
            `${baseTitle}: Todo lo que necesitas saber`,
            `Mi opinión sobre ${baseTitle} | Sin spoilers`,
            `${baseTitle} - Reseña completa en 3 minutos`,
            `¿${baseTitle} es tan buena como dicen? | Cine Norte`
        ];
        
        // Ajustar para TikTok (más cortos)
        if (targetPlatform === 'tiktok') {
            return [
                `${baseTitle} en 60 segundos`,
                `Mi veredicto: ${baseTitle}`,
                `${baseTitle} - ¿Sí o no?`,
                `Todo sobre ${baseTitle}`,
                `${baseTitle} - Sin spoilers`
            ];
        }
        
        return suggestions;
    }
    
    /**
     * Determina el estilo visual recomendado
     * @param {Object} content - Información del contenido
     * @param {string} style - Estilo del guion
     * @returns {string} Estilo visual
     */
    _determineVisualStyle(content, style) {
        if (content.genre.includes('Acción') || content.genre.includes('Ciencia Ficción')) {
            return 'high_energy';
        }
        if (content.genre.includes('Drama') || content.genre.includes('Romance')) {
            return 'cinematic';
        }
        if (content.genre.includes('Terror') || content.genre.includes('Suspenso')) {
            return 'dark_mysterious';
        }
        if (content.genre.includes('Comedia')) {
            return 'bright_playful';
        }
        return 'professional';
    }
    
    /**
     * Sugiere música de fondo
     * @param {Object} content - Información del contenido
     * @param {string} style - Estilo del guion
     * @returns {string} Sugerencia de música
     */
    _suggestMusic(content, style) {
        if (content.genre.includes('Acción')) return 'epic_action';
        if (content.genre.includes('Drama')) return 'emotional_drama';
        if (content.genre.includes('Terror')) return 'tense_horror';
        if (content.genre.includes('Comedia')) return 'light_comedy';
        return 'cinematic_ambient';
    }
    
    /**
     * Crea un guion de respaldo si falla la IA
     * @param {Object} content - Información del contenido
     * @param {string} targetPlatform - Plataforma objetivo
     * @returns {Object} Guion de respaldo
     */
    _createFallbackScript(content, targetPlatform) {
        const introText = `¡Hola cinéfilos! Bienvenidos a Cine Norte. Hoy analizamos ${content.title}.`;
        const plotText = `${content.overview.substring(0, 200)}...`;
        const outroText = '¿Qué opinas de esta película? Déjanos tu comentario y suscríbete para más análisis.';
        
        const sections = [
            {
                type: 'intro',
                content: introText,
                duration_seconds: 10,
                visual_cues: ['Logo Cine Norte'],
                emotion: 'excitement',
                emphasis_words: ['cinéfilos']
            },
            {
                type: 'plot',
                content: plotText,
                duration_seconds: 60,
                visual_cues: ['Montaje de escenas'],
                emotion: 'drama',
                emphasis_words: []
            },
            {
                type: 'outro',
                content: outroText,
                duration_seconds: 15,
                visual_cues: ['Call-to-action'],
                emotion: 'excitement',
                emphasis_words: ['comentario']
            }
        ];
        
        return {
            title: content.title,
            content: content,
            sections: sections,
            total_duration: 85,
            word_count: (introText + plotText + outroText).split(' ').length,
            target_platform: targetPlatform,
            hashtags: config.hashtags.slice(0, 10),
            title_suggestions: [`Análisis de ${content.title}`],
            visual_style: 'professional',
            music_suggestion: 'cinematic_ambient',
            raw_text: introText + '\n\n' + plotText + '\n\n' + outroText,
            generated_at: new Date().toISOString()
        };
    }
    
    /**
     * Exporta el guion a formato de texto
     * @param {Object} script - Guion generado
     * @returns {string} Contenido del archivo
     */
    exportScriptToText(script) {
        let content = `GUION CINE NORTE
================
Título: ${script.title}
Plataforma: ${script.target_platform}
Duración: ${script.total_duration} segundos
Palabras: ${script.word_count}

HASHTAGS:
${script.hashtags.join(', ')}

TÍTULOS SUGERIDOS:
${script.title_suggestions.map(title => `- ${title}`).join('\n')}

ESTILO VISUAL: ${script.visual_style}
MÚSICA: ${script.music_suggestion}

GUION:
======

`;
        
        script.sections.forEach((section, index) => {
            content += `
SECCIÓN ${index + 1}: ${section.type.toUpperCase()}
Duración: ${section.duration_seconds}s
Emoción: ${section.emotion}
Indicaciones visuales: ${section.visual_cues.join(', ')}

${section.content}

`;
        });
        
        return content;
    }
}

// Instancia global del generador
window.ScriptGenerator = ScriptGenerator;
window.scriptGenerator = new ScriptGenerator();
