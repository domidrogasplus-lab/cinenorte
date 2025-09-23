# 🎬 Cine Norte - Sistema de Generación de Contenido Automatizado

Sistema completo para generar contenido audiovisual optimizado para redes sociales, especializado en análisis cinematográficos con identidad de marca Cine Norte.

## 🚀 Características Principales

### 📊 Análisis de Contenido Inteligente
- **Selección automática** de películas y series populares
- **Integración con TMDB** para datos actualizados
- **Filtrado por criterios** (rating, popularidad, géneros)
- **Soporte para múltiples plataformas** (Netflix, Disney+, HBO Max, etc.)

### ✍️ Generación de Guiones con IA
- **Guiones automáticos** optimizados para 2-3 minutos
- **Múltiples estilos**: engaging, dramatic, informative
- **Estructura profesional** con intro, desarrollo y cierre
- **Sin spoilers importantes** para mantener el interés
- **Exportación a .txt** para conversión a voz

### 🎤 Narración y Subtítulos
- **Text-to-Speech** con voz IA personalizable
- **Subtítulos automáticos** en español sincronizados
- **Múltiples opciones de voz** (gTTS, ElevenLabs)
- **Sincronización perfecta** con el contenido visual
- **Formatos SRT y VTT** para máxima compatibilidad

### 🎨 Editor Audiovisual con Branding
- **Identidad visual Cine Norte** integrada
- **Paleta de colores**: Rojo #E50914, Negro #0A0A0A, Plateado #C0C0C0
- **Intro y outro animados** con efectos de reflector
- **Elementos visuales dinámicos** y transiciones profesionales
- **Música de fondo** libre de derechos ajustada al tono

### 📱 Formatos Múltiples
- **YouTube/Facebook**: 16:9 (1920x1080)
- **TikTok/Instagram Reels**: 9:16 (1080x1920)
- **Instagram Posts**: 1:1 (1080x1080)
- **Twitter**: 16:9 (1280x720)
- **Facebook**: 1.91:1 (1200x630)

### 🎯 Optimización con IA
- **Análisis de impacto** y potencial viral
- **Optimización SEO** automática
- **Sugerencias de mejora** basadas en IA
- **Análisis de engagement** y atractivo visual
- **Recomendaciones personalizadas** para cada contenido

### 🖼️ Generación de Miniaturas
- **Miniaturas optimizadas** para cada plataforma
- **Estilos cinematográficos** profesionales
- **Elementos visuales dinámicos** basados en el contenido
- **Branding consistente** con Cine Norte
- **Múltiples variaciones** para A/B testing

## 🛠️ Instalación

### Requisitos del Sistema
- Python 3.8 o superior
- Windows 10/11 (recomendado)
- 8GB RAM mínimo
- 10GB espacio libre en disco

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/cine-norte.git
cd cine-norte

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

### Configuración de API Keys

Crear archivo `.env` con las siguientes variables:

```env
# OpenAI para generación de guiones
OPENAI_API_KEY=tu_openai_api_key

# TMDB para datos de películas/series
TMDB_API_KEY=tu_tmdb_api_key

# ElevenLabs para voz IA (opcional)
ELEVENLABS_API_KEY=tu_elevenlabs_api_key

# YouTube API (opcional)
YOUTUBE_API_KEY=tu_youtube_api_key
```

## 🚀 Uso

### Interfaz de Línea de Comandos

```bash
python main.py
```

### Uso Programático

```python
from main import CineNorteSystem

# Inicializar sistema
system = CineNorteSystem()

# Generar contenido individual
result = system.generate_content(
    content_query="Spider-Man: No Way Home",
    content_type="movie",
    style="engaging"
)

# Generar contenido en lote
results = system.generate_batch_content(count=5, content_type="movie")

# Optimizar contenido existente
suggestions = system.optimize_existing_content("mi_guion.txt")
```

### Ejemplo de Flujo Completo

```python
# 1. Seleccionar contenido
content = system.content_analyzer.get_recommended_content(limit=1)[0]

# 2. Generar guion
script = system.script_generator.generate_script(content, "engaging")

# 3. Generar voz
voice_path = system.voice_generator.generate_voice_from_script(script.raw_text)

# 4. Crear proyecto de video
video_project = system.video_editor.create_video_project(script)

# 5. Generar videos en múltiples formatos
video_paths = system.multi_format_generator.generate_all_formats(video_project)

# 6. Generar miniaturas
thumbnail_paths = system.multi_format_generator.generate_thumbnails(video_project)

# 7. Análisis de impacto
analysis = system.ai_optimizer.analyze_content_impact(video_project)
```

## 📁 Estructura del Proyecto

```
cine-norte/
├── src/                          # Código fuente
│   ├── content_analyzer.py       # Análisis de contenido
│   ├── script_generator.py       # Generación de guiones
│   ├── voice_generator.py        # Narración y subtítulos
│   ├── video_editor.py           # Editor audiovisual
│   ├── multi_format_generator.py # Formatos múltiples
│   ├── ai_optimizer.py           # Optimización con IA
│   └── thumbnail_generator.py    # Miniaturas y SEO
├── output/                       # Archivos generados
│   ├── videos/                   # Videos en múltiples formatos
│   ├── thumbnails/               # Miniaturas
│   ├── scripts/                  # Guiones en texto
│   ├── audio/                    # Archivos de voz
│   └── subtitles/                # Subtítulos
├── assets/                       # Recursos estáticos
├── temp/                         # Archivos temporales
├── logs/                         # Logs del sistema
├── config.py                     # Configuración
├── main.py                       # Interfaz principal
└── requirements.txt              # Dependencias
```

## 🎯 Características Avanzadas

### Análisis de Impacto con IA
- **Score de engagement** (0-1)
- **Potencial viral** basado en tendencias
- **Optimización SEO** automática
- **Atractivo visual** evaluado por IA
- **Recomendaciones personalizadas**

### Optimización Automática
- **Títulos optimizados** para SEO
- **Hashtags trending** automáticos
- **Descripciones optimizadas** para cada plataforma
- **Keywords relevantes** extraídas automáticamente
- **Sugerencias de mejora** basadas en datos

### Branding Consistente
- **Logo Cine Norte** integrado
- **Paleta de colores** consistente
- **Tipografías** profesionales
- **Elementos visuales** reconocibles
- **Identidad de marca** en todos los formatos

## 📊 Métricas y Análisis

El sistema genera reportes detallados incluyendo:

- **Análisis de impacto** completo
- **Métricas de engagement** predichas
- **Optimización SEO** aplicada
- **Sugerencias de mejora** específicas
- **Datos de rendimiento** esperado

## 🔧 Configuración Avanzada

### Personalización de Voz
```python
# Configurar voz personalizada
voice_settings = VoiceSettings(
    language="es",
    speed=1.0,
    pitch=0.0,
    volume=1.0
)
```

### Personalización de Branding
```python
# Modificar colores de marca
BRANDING = {
    "colors": {
        "primary": "#E50914",    # Rojo Netflix
        "secondary": "#0A0A0A",  # Negro profundo
        "accent": "#C0C0C0"      # Plateado metálico
    }
}
```

### Configuración de Formatos
```python
# Añadir nuevos formatos
VIDEO_CONFIG["formats"]["custom"] = {
    "width": 1920,
    "height": 1080,
    "ratio": "16:9"
}
```

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de API Keys**
   - Verificar que las API keys estén configuradas correctamente
   - Asegurar que las keys tengan los permisos necesarios

2. **Error de Dependencias**
   - Ejecutar `pip install -r requirements.txt`
   - Verificar versión de Python (3.8+)

3. **Error de Memoria**
   - Reducir el número de contenidos en lote
   - Cerrar otras aplicaciones

4. **Error de Red**
   - Verificar conexión a internet
   - Verificar configuración de proxy si aplica

### Logs y Debugging

Los logs se guardan en `logs/cine_norte.log` con información detallada para debugging.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **TMDB** por la API de datos cinematográficos
- **OpenAI** por la generación de guiones con IA
- **MoviePy** por el procesamiento de video
- **PIL/Pillow** por el procesamiento de imágenes
- **gTTS** por la síntesis de voz

## 📞 Soporte

Para soporte técnico o preguntas:

- 📧 Email: soporte@cinenorte.com
- 💬 Discord: Cine Norte Community
- 📱 Twitter: @CineNorteAI

---

**Cine Norte** - Tu canal de análisis cinematográfico automatizado 🎬✨
