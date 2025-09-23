# 🎬 Cine Norte Automation System

Sistema automatizado para generar contenido audiovisual de películas y series, optimizado para YouTube, Facebook, Instagram y TikTok con identidad visual Cine Norte.

## 🚀 Características

- **Generación automática de guiones** (1-3 min, sin spoilers)
- **Locución con IA** (voz personalizable)
- **Subtítulos automáticos** en español sincronizados
- **Edición con branding Cine Norte** (colores, tipografías, intro/outro)
- **Múltiples formatos**: 16:9 (YouTube/Facebook), 9:16 (TikTok/Reels), 1:1 (Instagram)
- **Miniaturas optimizadas** con identidad visual
- **SEO automático** (títulos, hashtags, descripciones)
- **Análisis de impacto visual** con IA

## 🎨 Identidad Visual

- **Colores**: Rojo #E50914, Negro #0A0A0A, Plateado #C0C0C0
- **Tipografías**: Bebas Neue (títulos), Inter (cuerpo)
- **Intro/Outro**: Logo animado con barrido de luz tipo reflector
- **Branding**: Lower-thirds, overlays, música libre de derechos

## 📋 Requisitos

- Python 3.8+
- FFmpeg instalado en el sistema
- APIs configuradas (OpenAI, ElevenLabs, TMDB)

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd cine-norte-automation
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar APIs**
```bash
cp config.yaml.example config.yaml
# Editar config.yaml con tus API keys
```

4. **Verificar FFmpeg**
```bash
ffmpeg -version
```

## ⚙️ Configuración

Edita `config.yaml` con tus credenciales:

```yaml
ai:
  openai_api_key: "tu_openai_api_key"
  elevenlabs_api_key: "tu_elevenlabs_api_key"
  elevenlabs_voice_id: "pNInz6obpgDQGcFmaJgB"

apis:
  tmdb:
    api_key: "tu_tmdb_api_key"
```

## 🎯 Uso

### Flujo completo automatizado

```bash
# Procesar contenido de Netflix
python cine_norte_automation.py --platform Netflix --limit 3

# Procesar por género
python cine_norte_automation.py --genre Thriller --limit 5

# Procesar todo el contenido disponible
python cine_norte_automation.py --limit 10
```

### Ejemplo paso a paso

```bash
# Ejecutar ejemplo completo
python example_workflow.py

# Verificar dependencias
python example_workflow.py --check-deps
```

### Uso programático

```python
from cine_norte_automation import CineNorteAutomation

# Inicializar sistema
automation = CineNorteAutomation('config.yaml')

# Seleccionar contenido
content_list = automation.select_content(platform="Netflix", limit=5)

# Procesar cada contenido
for content in content_list:
    results = automation.run_full_workflow(content)
    print(f"Procesado: {content['title']}")
```

## 📁 Estructura del Proyecto

```
cine-norte-automation/
├── cine_norte_automation.py    # Script principal
├── config.yaml                 # Configuración
├── requirements.txt            # Dependencias
├── ffmpeg_templates.py         # Plantillas FFmpeg
├── example_workflow.py         # Ejemplo de uso
├── prompts/                    # Prompts de IA
│   ├── 01_script_prompt.txt
│   ├── 02_seo_titles_hashtags.txt
│   ├── 03_scene_selection.txt
│   ├── 04_tts_prompt.txt
│   ├── 05_subtitles_prompt.txt
│   ├── 06_editing_prompt.txt
│   ├── 07_thumbnail_prompt.txt
│   └── 08_ai_recommendations.txt
├── projects/                   # Proyectos en proceso
├── exports/                    # Videos finales
├── assets/                     # Recursos (música, logos, etc.)
└── temp/                       # Archivos temporales
```

## 🎬 Flujo de Trabajo

1. **Selección de contenido** - TMDB API + JustWatch
2. **Análisis de escenas** - Detección de cortes + scoring de impacto
3. **Generación de guion** - LLM (GPT-4) con prompts especializados
4. **Locución IA** - ElevenLabs con voz personalizable
5. **Subtítulos** - Whisper + sincronización automática
6. **Edición** - FFmpeg con plantillas Cine Norte
7. **Exportación** - Múltiples formatos (16:9, 9:16, 1:1)
8. **SEO** - Títulos y hashtags optimizados
9. **Miniaturas** - Diseño con identidad visual

## 🎨 Personalización

### Colores y Branding

Edita `config.yaml`:

```yaml
branding:
  colors:
    primary: "#E50914"      # Rojo Cine Norte
    background: "#0A0A0A"   # Negro profundo
    accent: "#C0C0C0"       # Plateado metálico
  fonts:
    title: "Bebas Neue"
    body: "Inter"
```

### Voz IA

Cambia la voz en `config.yaml`:

```yaml
ai:
  elevenlabs_voice_id: "tu_voice_id_aqui"
```

### Formatos de Video

Ajusta resoluciones y bitrates:

```yaml
video:
  master_resolution: "1920x1080"
  master_fps: 24
  master_bitrate: "20M"
```

## 🔧 Troubleshooting

### Error: FFmpeg no encontrado
```bash
# Windows (con Chocolatey)
choco install ffmpeg

# macOS (con Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
```

### Error: API keys no configuradas
1. Verifica que `config.yaml` existe
2. Confirma que las API keys son válidas
3. Revisa los logs en `cine_norte.log`

### Error: Dependencias faltantes
```bash
pip install -r requirements.txt --upgrade
```

## 📊 Salida

### Archivos generados por proyecto:

- `script.txt` - Guion narrado
- `voiceover.wav` - Audio generado por IA
- `subtitles_es.srt` - Subtítulos en español
- `thumbnail.png` - Miniatura optimizada
- `video_16x9.mp4` - YouTube/Facebook
- `video_9x16.mp4` - TikTok/Reels
- `video_1x1.mp4` - Instagram/Facebook
- `metadata.json` - Títulos, hashtags, timestamps

### Estructura de exportación:

```
exports/
└── 20231201_Pelicula_Titulo/
    ├── video/
    │   ├── video_16x9.mp4
    │   ├── video_9x16.mp4
    │   └── video_1x1.mp4
    ├── audio/
    │   └── voiceover.wav
    ├── subtitles/
    │   └── subtitles_es.srt
    ├── script/
    │   └── script.txt
    ├── thumbnails/
    │   ├── thumb_yt.png
    │   └── thumb_ig.jpg
    └── metadata/
        └── meta.json
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-repo/issues)
- **Documentación**: [Wiki](https://github.com/tu-repo/wiki)
- **Email**: soporte@cinenorte.com

## 🎯 Roadmap

- [ ] Integración con más plataformas de streaming
- [ ] Análisis de sentimientos en guiones
- [ ] Plantillas de After Effects
- [ ] Dashboard web para gestión
- [ ] API REST para integración
- [ ] Machine Learning para optimización automática

---

**Cine Norte** - Automatizando la creación de contenido cinematográfico 🎬✨
