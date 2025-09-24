# 🎬 Cine Norte - Generador Automatizado de Contenido Audiovisual

Sistema completo de automatización para generar contenido audiovisual optimizado para redes sociales, especializado en análisis cinematográfico con identidad de marca Cine Norte.

## 🌟 Características Principales

### 🔍 Análisis de Contenido Inteligente
- **Conexión con APIs de streaming**: Netflix, Amazon Prime, Disney+, HBO Max, Paramount, Apple TV, MagisTV
- **Análisis de viabilidad**: Evalúa contenido para potencial viral y engagement
- **Detección automática de tendencias**: Identifica contenido popular y relevante
- **Extracción de metadatos**: Información completa de películas y series

### 📝 Generación de Guiones con IA
- **Guiones optimizados por plataforma**: YouTube, TikTok, Instagram, Facebook, Twitter
- **Múltiples estilos**: Dinámico, dramático, cómico, analítico
- **Estructura profesional**: Intro, hook, trama, análisis, outro
- **Sin spoilers importantes**: Mantiene el misterio y la intriga
- **Exportación a .txt**: Para conversión a voz con IA

### 🎤 Síntesis de Voz y Subtítulos
- **Voces personalizables**: Múltiples perfiles de voz (masculino, femenino, dramático, energético)
- **Subtítulos automáticos**: Sincronizados con el audio en español
- **Efectos emocionales**: Ajuste de velocidad, tono y volumen según el contexto
- **Múltiples formatos**: VTT, SRT para máxima compatibilidad

### 🎬 Editor Audiovisual Profesional
- **Branding Cine Norte**: Paleta de colores consistente (#E50914, #0A0A0A, #C0C0C0)
- **Efectos visuales**: Transiciones, animaciones, overlays dinámicos
- **Logo animado**: Con efectos de luces tipo reflector
- **Música de fondo**: Libre de derechos, ajustada al tono del contenido

### 📱 Formatos Múltiples
- **YouTube**: 16:9 (1920x1080) - Optimizado para desktop y TV
- **TikTok**: 9:16 (1080x1920) - Formato vertical para móviles
- **Instagram**: 1:1 (1080x1080) - Posts cuadrados
- **Facebook**: 16:9 (1920x1080) - Videos de feed
- **Twitter**: 16:9 (1280x720) - Videos de timeline

### 🖼️ Generación de Miniaturas
- **Miniaturas optimizadas**: Para cada plataforma con especificaciones únicas
- **Múltiples estilos**: Cinematográfico, dramático, acción, misterio
- **Branding automático**: Logo Cine Norte integrado
- **Análisis de optimización**: Score de contraste, legibilidad y composición

### 🤖 Optimización con IA
- **Análisis de engagement**: Predicción de potencial viral
- **Optimización SEO**: Títulos, descripciones y hashtags optimizados
- **Análisis visual**: Composición, colores y elementos llamativos
- **Análisis de audio**: Calidad, claridad y balance musical
- **Recomendaciones inteligentes**: Mejoras específicas para cada contenido

## 🚀 Instalación

### Requisitos del Sistema
- Python 3.8 o superior
- 8GB RAM mínimo (16GB recomendado)
- 10GB espacio en disco
- GPU compatible con CUDA (opcional, para procesamiento acelerado)

### Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/cine-norte.git
cd cine-norte
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp env_example.txt .env
# Editar .env con tus claves de API
```

4. **Ejecutar la aplicación**
```bash
streamlit run main_app.py
```

### Configuración de APIs

#### OpenAI API (Requerido)
```bash
OPENAI_API_KEY=tu_clave_openai_aqui
```

#### TMDB API (Recomendado)
```bash
TMDB_API_KEY=tu_clave_tmdb_aqui
```

#### Otras APIs (Opcionales)
```bash
HUGGINGFACE_API_KEY=tu_clave_huggingface_aqui
OMDB_API_KEY=tu_clave_omdb_aqui
```

## 📖 Guía de Uso

### 1. Análisis de Contenido
1. Ve a la pestaña "🔍 Análisis de Contenido"
2. Busca películas o series por nombre
3. Revisa los resultados y selecciona el contenido deseado
4. Analiza la viabilidad del contenido para crear videos

### 2. Generación de Guion
1. Ve a la pestaña "📝 Generación de Guion"
2. Configura la plataforma objetivo y estilo
3. Ajusta la duración deseada
4. Haz clic en "Generar Guion" y espera el resultado
5. Revisa el guion generado y descárgalo si es necesario

### 3. Creación de Video
1. Ve a la pestaña "🎬 Creación de Video"
2. Configura el estilo visual y perfil de voz
3. Selecciona opciones adicionales (subtítulos, música)
4. Haz clic en "Generar Video" y espera el procesamiento
5. Genera formatos múltiples para todas las plataformas

### 4. Optimización con IA
1. Ve a la pestaña "📊 Optimización IA"
2. Haz clic en "Analizar con IA"
3. Revisa el análisis de engagement y viralidad
4. Implementa las recomendaciones sugeridas

### 5. Descargas
1. Ve a la pestaña "📁 Descargas"
2. Descarga todos los archivos generados
3. Limpia archivos temporales cuando termines

## 🎨 Personalización

### Esquemas de Color
```python
# En config.py
PRIMARY_RED = "#E50914"
DEEP_BLACK = "#0A0A0A"
METALLIC_SILVER = "#C0C0C0"
```

### Perfiles de Voz
```python
# Crear perfil personalizado
custom_voice = voice_synthesizer.create_voice_profile(
    name="Mi Voz",
    language="es",
    speed=1.0,
    pitch=1.0,
    volume=1.0
)
```

### Estilos Visuales
- **Cinematográfico**: Clásico, elegante, profesional
- **Dinámico**: Energético, moderno, llamativo
- **Dramático**: Intenso, emocional, impactante

## 📊 Métricas y Análisis

### Score de Optimización
- **Calidad de Contenido**: 0-100 puntos
- **Potencial de Engagement**: 0-100 puntos
- **Probabilidad Viral**: 0-100 puntos
- **Optimización SEO**: 0-100 puntos
- **Impacto Visual**: 0-100 puntos
- **Calidad de Audio**: 0-100 puntos

### Análisis de Viabilidad
- **Popularidad**: Basado en datos de TMDB
- **Rating**: Calificación de usuarios
- **Disponibilidad de tráiler**: Contenido visual disponible
- **Calidad de descripción**: Riqueza de información
- **Género**: Impacto visual del género

## 🔧 Configuración Avanzada

### Ajustes de Video
```python
# En config.py
VIDEO_QUALITY = "1080p"
VIDEO_DURATION_MAX = 180  # segundos
AUDIO_SAMPLE_RATE = 44100
AUDIO_BITRATE = "192k"
```

### Formatos Personalizados
```python
# Agregar nuevo formato
custom_format = FormatSpec(
    name="Mi Plataforma",
    width=1920,
    height=1080,
    aspect_ratio="16:9",
    platform="custom",
    max_duration=120,
    recommended_fps=30,
    bitrate="4000k",
    description="Formato personalizado"
)
```

## 🐛 Solución de Problemas

### Errores Comunes

#### Error de API Key
```
Error: OpenAI API key not found
```
**Solución**: Configura tu clave de OpenAI en el archivo .env

#### Error de Memoria
```
Error: Out of memory
```
**Solución**: Reduce la calidad del video o usa un sistema con más RAM

#### Error de Dependencias
```
ModuleNotFoundError: No module named 'moviepy'
```
**Solución**: Instala las dependencias con `pip install -r requirements.txt`

### Logs y Debugging
```python
# Habilitar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuciones

### Cómo Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

### Estándares de Código
- Usar Python 3.8+
- Seguir PEP 8
- Documentar funciones y clases
- Incluir tests para nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **OpenAI** por la API de GPT-4
- **TMDB** por la base de datos de películas
- **MoviePy** por el procesamiento de video
- **Streamlit** por el framework de interfaz
- **Hugging Face** por los modelos de IA

## 📞 Soporte

- **Email**: soporte@cinenorte.com
- **Discord**: [Servidor de Cine Norte](https://discord.gg/cinenorte)
- **GitHub Issues**: [Reportar problemas](https://github.com/tu-usuario/cine-norte/issues)

## 🔄 Actualizaciones

### Versión 1.0.0
- ✅ Análisis de contenido con APIs de streaming
- ✅ Generación de guiones con IA
- ✅ Síntesis de voz y subtítulos
- ✅ Editor audiovisual con branding
- ✅ Formatos múltiples
- ✅ Optimización con IA
- ✅ Generación de miniaturas
- ✅ Interfaz web completa

### Próximas Versiones
- 🔄 Integración con más plataformas de streaming
- 🔄 Análisis de sentimientos en tiempo real
- 🔄 Automatización de subida a redes sociales
- 🔄 Dashboard de analytics
- 🔄 Colaboración en equipo

---

**Cine Norte** - Donde la tecnología se encuentra con el arte cinematográfico 🎬✨
