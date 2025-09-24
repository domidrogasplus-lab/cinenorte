# 🎬 Cine Norte - Generador Automatizado de Contenido

Sistema web completo para generar contenido audiovisual optimizado para redes sociales, especializado en análisis cinematográfico con identidad de marca Cine Norte.

## ✨ Características Principales

### 🔍 Análisis de Contenido
- **Búsqueda Inteligente**: Conecta con TMDB API para encontrar películas y series
- **Contenido Trending**: Obtiene contenido popular en tiempo real
- **Análisis de Viabilidad**: Evalúa el potencial viral del contenido
- **Detección de Plataformas**: Identifica automáticamente la plataforma de streaming

### 📝 Generación de Guiones con IA
- **OpenAI GPT-4**: Crea guiones dinámicos y atractivos
- **Múltiples Estilos**: Cinematográfico, dramático, cómico, analítico
- **Optimización por Plataforma**: YouTube, TikTok, Instagram, Facebook, Twitter
- **Estructura Profesional**: Intro, hook, trama, análisis, outro
- **Sin Spoilers**: Mantiene el misterio sin revelar giros importantes

### 🎤 Síntesis de Voz Avanzada
- **Web Speech API**: Convierte texto a voz con múltiples perfiles
- **Voces Personalizables**: Masculino, femenino, dramático, energético
- **Subtítulos Automáticos**: Genera subtítulos sincronizados en formato VTT/SRT
- **Efectos Emocionales**: Ajusta tono y velocidad según la emoción

### 🎬 Editor de Video Profesional
- **Canvas API**: Crea videos con branding Cine Norte
- **Efectos Visuales**: Gradientes, partículas, transiciones dinámicas
- **Branding Automático**: Logo animado, colores corporativos, tipografía
- **Múltiples Estilos**: Cinematográfico, dramático, acción, misterio

### 📱 Formatos Múltiples
- **YouTube**: 1920x1080 (16:9) - Formato estándar
- **TikTok**: 1080x1920 (9:16) - Formato vertical
- **Instagram Reels**: 1080x1920 (9:16) - Optimizado para móviles
- **Instagram Square**: 1080x1080 (1:1) - Formato cuadrado
- **Facebook**: 1920x1080 (16:9) - Para redes sociales
- **Twitter**: 1280x720 (16:9) - Formato compacto

### 🖼️ Generador de Miniaturas
- **Múltiples Plataformas**: Optimizado para cada red social
- **Esquemas de Color**: Cinematográfico, dramático, acción, misterio
- **Branding Inteligente**: Overlay automático de Cine Norte
- **Análisis de Optimización**: Score de contraste, legibilidad, composición

### 🤖 Optimización con IA
- **Análisis Completo**: Contenido, engagement, viralidad, SEO
- **Recomendaciones Inteligentes**: Mejoras específicas para cada métrica
- **Score de Optimización**: Evaluación general del contenido
- **Sugerencias de Mejora**: Ritmo, cortes, duración, audio

## 🎨 Identidad Visual

### Paleta de Colores
- **Rojo Primario**: `#E50914` - Color principal de marca
- **Negro Profundo**: `#0A0A0A` - Fondo principal
- **Plateado Metálico**: `#C0C0C0` - Acentos y texto secundario
- **Oro**: `#FFD700` - Elementos destacados

### Elementos de Marca
- **Logo Animado**: Efecto de luces tipo reflector
- **Tipografía**: Impactante y cinematográfica
- **Efectos Visuales**: Gradientes, partículas, transiciones suaves
- **Consistencia**: Aplicada en todos los formatos y plataformas

## 🚀 Instalación y Uso

### Requisitos
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexión a internet
- APIs opcionales: OpenAI, TMDB

### Configuración Rápida
1. **Descarga los archivos** del proyecto
2. **Abre `index.html`** en tu navegador
3. **Configura las APIs** (opcional pero recomendado):
   - OpenAI API para generación de guiones
   - TMDB API para análisis de contenido
4. **¡Comienza a crear!**

### Configuración de APIs

#### OpenAI API (Recomendado)
1. Obtén tu clave API en [OpenAI Platform](https://platform.openai.com/)
2. Ve a Configuración en la aplicación
3. Pega tu clave en el campo "OpenAI API Key"
4. Guarda la configuración

#### TMDB API (Opcional)
1. Regístrate en [TMDB](https://www.themoviedb.org/)
2. Obtén tu API key
3. Configúrala en la aplicación

## 📖 Guía de Uso

### 1. Análisis de Contenido
- **Buscar**: Ingresa el nombre de una película o serie
- **Seleccionar Tipo**: Película, Serie, o Todos
- **Ver Resultados**: Revisa información, rating, plataforma
- **Seleccionar**: Elige el contenido que más te guste

### 2. Generación de Guion
- **Configurar**: Selecciona plataforma objetivo y estilo
- **Ajustar Duración**: Usa el slider para definir duración (30-300s)
- **Generar**: Crea el guion con IA
- **Revisar**: Lee las secciones generadas

### 3. Creación de Video
- **Configurar Audio**: Selecciona perfil de voz
- **Configurar Visual**: Elige estilo cinematográfico
- **Generar**: Crea el video con branding Cine Norte
- **Ver Resultados**: Reproduce el video generado

### 4. Optimización
- **Analizar**: Ejecuta análisis con IA
- **Revisar Métricas**: Ve scores de engagement, viralidad, SEO
- **Aplicar Mejoras**: Sigue las recomendaciones sugeridas

### 5. Descargas
- **Guion**: Descarga el texto del guion
- **Audio**: Descarga el archivo de audio
- **Subtítulos**: Descarga subtítulos en formato VTT
- **Video**: Descarga el video principal
- **Formatos**: Descarga todos los formatos para redes sociales
- **Miniaturas**: Descarga miniaturas optimizadas

## 🛠️ Arquitectura Técnica

### Frontend Puro
- **HTML5**: Estructura semántica y accesible
- **CSS3**: Diseño responsivo con identidad visual
- **JavaScript ES6+**: Lógica de aplicación modular
- **Canvas API**: Generación de video y miniaturas
- **Web Speech API**: Síntesis de voz
- **Web Audio API**: Procesamiento de audio

### Módulos Principales
- **ContentAnalyzer**: Análisis de contenido con APIs
- **ScriptGenerator**: Generación de guiones con IA
- **VoiceSynthesizer**: Síntesis de voz y subtítulos
- **VideoEditor**: Edición de video con Canvas
- **FormatGenerator**: Generación de formatos múltiples
- **AIOptimizer**: Optimización con IA
- **ThumbnailGenerator**: Generación de miniaturas
- **Utils**: Utilidades y helpers

### APIs Externas
- **OpenAI GPT-4**: Generación de guiones
- **TMDB API**: Análisis de contenido cinematográfico
- **Web Speech API**: Síntesis de voz nativa

## 🎯 Casos de Uso

### Creadores de Contenido
- **YouTubers**: Genera análisis cinematográficos profesionales
- **TikTokers**: Crea contenido vertical optimizado
- **Instagramers**: Desarrolla reels y posts atractivos
- **Influencers**: Produce contenido de calidad con branding

### Empresas de Marketing
- **Agencias**: Automatiza la creación de contenido audiovisual
- **Estudios**: Genera promocionales y trailers
- **Streaming**: Crea contenido promocional para plataformas

### Educadores
- **Profesores**: Crea material educativo audiovisual
- **Instituciones**: Desarrolla contenido institucional
- **Cursos Online**: Genera videos educativos

## 🔧 Personalización

### Estilos Visuales
- **Cinematográfico**: Clásico y elegante
- **Dramático**: Intenso y emocional
- **Acción**: Dinámico y energético
- **Misterio**: Oscuro y enigmático

### Perfiles de Voz
- **Masculino**: Profesional y autoritativo
- **Femenino**: Elegante y expresivo
- **Dramático**: Intenso y emotivo
- **Energético**: Dinámico y vibrante

### Plataformas Soportadas
- **YouTube**: Análisis largos y detallados
- **TikTok**: Contenido corto y directo
- **Instagram**: Visual y estético
- **Facebook**: Compartible y social
- **Twitter**: Conciso e impactante

## 📊 Métricas y Análisis

### Scores de Optimización
- **Contenido**: Calidad del guion y estructura
- **Engagement**: Potencial de interacción
- **Viralidad**: Probabilidad de viralización
- **SEO**: Optimización para búsquedas
- **Visual**: Impacto visual del video
- **Audio**: Calidad del audio y voz

### Recomendaciones Inteligentes
- **Mejoras de Contenido**: Sugerencias específicas
- **Optimización SEO**: Títulos y hashtags
- **Ajustes Visuales**: Composición y efectos
- **Mejoras de Audio**: Volumen y claridad

## 🚀 Roadmap Futuro

### Próximas Características
- **IA de Video**: Análisis automático de escenas
- **Templates**: Plantillas predefinidas
- **Colaboración**: Trabajo en equipo
- **Analytics**: Métricas de rendimiento
- **Integraciones**: Más APIs de streaming

### Mejoras Técnicas
- **WebAssembly**: Rendimiento mejorado
- **PWA**: Aplicación web progresiva
- **Offline**: Funcionamiento sin conexión
- **Cloud**: Sincronización en la nube

## 🤝 Contribución

### Cómo Contribuir
1. **Fork** del repositorio
2. **Crea** una rama para tu feature
3. **Desarrolla** tu funcionalidad
4. **Prueba** exhaustivamente
5. **Envía** un Pull Request

### Áreas de Contribución
- **Nuevas Plataformas**: Agregar soporte para más redes
- **Efectos Visuales**: Nuevos estilos y animaciones
- **APIs**: Integrar más fuentes de contenido
- **IA**: Mejorar algoritmos de optimización
- **UI/UX**: Mejorar la experiencia de usuario

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **OpenAI** por la API de GPT-4
- **TMDB** por la base de datos cinematográfica
- **Web APIs** por las tecnologías nativas del navegador
- **Comunidad** por el feedback y contribuciones

## 📞 Soporte

### Documentación
- **Guía de Usuario**: Incluida en la aplicación
- **API Reference**: Documentación técnica
- **Ejemplos**: Casos de uso prácticos

### Contacto
- **Issues**: Reporta bugs en GitHub
- **Discussions**: Preguntas y sugerencias
- **Email**: soporte@cinenorte.com

---

**¡Crea contenido cinematográfico profesional con Cine Norte!** 🎬✨