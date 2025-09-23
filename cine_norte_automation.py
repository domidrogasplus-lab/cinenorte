#!/usr/bin/env python3
"""
Cine Norte Automation System
Sistema automatizado para generar contenido audiovisual de películas y series
"""

import os
import sys
import json
import yaml
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
import ffmpeg
from PIL import Image, ImageDraw, ImageFont
import openai
from elevenlabs import Voice, VoiceSettings, generate, save

class CineNorteAutomation:
    def __init__(self, config_path: str = "config.yaml"):
        """Inicializar el sistema de automatización"""
        self.config = self.load_config(config_path)
        self.project_dir = Path("projects")
        self.assets_dir = Path("assets")
        self.exports_dir = Path("exports")
        self.prompts_dir = Path("prompts")
        
        # Crear directorios necesarios
        self.setup_directories()
        
        # Configurar APIs
        self.setup_apis()
    
    def load_config(self, config_path: str) -> Dict:
        """Cargar configuración desde YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Archivo de configuración {config_path} no encontrado")
            sys.exit(1)
    
    def setup_directories(self):
        """Crear estructura de directorios"""
        directories = [
            self.project_dir,
            self.assets_dir / "stock",
            self.assets_dir / "music",
            self.assets_dir / "logos",
            self.exports_dir,
            self.prompts_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def setup_apis(self):
        """Configurar APIs externas"""
        # OpenAI
        if self.config.get('ai', {}).get('openai_api_key'):
            openai.api_key = self.config['ai']['openai_api_key']
        
        # ElevenLabs
        if self.config.get('ai', {}).get('elevenlabs_api_key'):
            os.environ['ELEVENLABS_API_KEY'] = self.config['ai']['elevenlabs_api_key']
    
    def select_content(self, platform: str = None, genre: str = None, limit: int = 5) -> List[Dict]:
        """Seleccionar contenido reciente y popular"""
        print("🎬 Seleccionando contenido...")
        
        # Simular selección de TMDB (en producción real, usar API real)
        sample_content = [
            {
                "id": 1,
                "title": "Oppenheimer",
                "year": 2023,
                "platform": "Netflix",
                "genres": ["Drama", "Thriller"],
                "synopsis": "La historia de J. Robert Oppenheimer y el desarrollo de la bomba atómica",
                "keywords": ["historia", "ciencia", "guerra", "moral"],
                "poster_url": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"
            },
            {
                "id": 2,
                "title": "Barbie",
                "year": 2023,
                "platform": "HBO Max",
                "genres": ["Comedia", "Aventura"],
                "synopsis": "Barbie vive en Barbieland hasta que es expulsada al mundo real",
                "keywords": ["comedia", "aventura", "feminismo", "color"],
                "poster_url": "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg"
            }
        ]
        
        # Filtrar por plataforma y género si se especifica
        if platform:
            sample_content = [c for c in sample_content if c['platform'] == platform]
        if genre:
            sample_content = [c for c in sample_content if genre.lower() in [g.lower() for g in c['genres']]]
        
        return sample_content[:limit]
    
    def generate_script(self, content: Dict) -> str:
        """Generar guion usando IA"""
        print(f"📝 Generando guion para {content['title']}...")
        
        # Cargar prompt de guion
        with open(self.prompts_dir / "01_script_prompt.txt", 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        # Reemplazar variables
        prompt = prompt_template.format(
            title=content['title'],
            year=content['year'],
            platform=content['platform'],
            genres=', '.join(content['genres']),
            region=self.config.get('project', {}).get('region', 'MX'),
            synopsis=content['synopsis'],
            keywords=', '.join(content['keywords'])
        )
        
        # Generar con OpenAI (simulado)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            script = response.choices[0].message.content
            
            # Guardar guion
            project_name = f"{datetime.now().strftime('%Y%m%d')}_{content['title'].replace(' ', '_')}"
            project_path = self.project_dir / project_name
            project_path.mkdir(exist_ok=True)
            
            with open(project_path / "script.txt", 'w', encoding='utf-8') as f:
                f.write(script)
            
            return script
            
        except Exception as e:
            print(f"❌ Error generando guion: {e}")
            return self.get_fallback_script(content)
    
    def get_fallback_script(self, content: Dict) -> str:
        """Guion de respaldo si falla la IA"""
        return f"""
{content['title']} ({content['year']}) - Disponible en {content['platform']}

{content['synopsis']}

Esta {content['genres'][0].lower()} promete mantenerte en el borde del asiento con su trama envolvente y personajes memorables.

¿La verías? Disponible ahora en {content['platform']}.

Frases destacadas:
- "{content['title']} te sorprenderá"
- "Una historia que no puedes perderte"
- "Disponible en {content['platform']}"
"""
    
    def generate_voiceover(self, script: str, content: Dict) -> str:
        """Generar locución con IA"""
        print("🎤 Generando locución...")
        
        project_name = f"{datetime.now().strftime('%Y%m%d')}_{content['title'].replace(' ', '_')}"
        project_path = self.project_dir / project_name
        
        try:
            # Usar ElevenLabs para TTS
            voice_id = self.config.get('ai', {}).get('elevenlabs_voice_id', 'pNInz6obpgDQGcFmaJgB')
            
            audio = generate(
                text=script,
                voice=Voice(
                    voice_id=voice_id,
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.75,
                        style=0.0,
                        use_speaker_boost=True
                    )
                )
            )
            
            audio_path = project_path / "voiceover.wav"
            save(audio, str(audio_path))
            
            return str(audio_path)
            
        except Exception as e:
            print(f"❌ Error generando locución: {e}")
            return None
    
    def generate_subtitles(self, audio_path: str, script: str) -> str:
        """Generar subtítulos sincronizados"""
        print("📄 Generando subtítulos...")
        
        project_name = f"{datetime.now().strftime('%Y%m%d')}_{Path(audio_path).parent.name.split('_', 1)[1]}"
        project_path = self.project_dir / project_name
        
        try:
            # Usar Whisper para transcribir y obtener timestamps
            model = whisper.load_model("base")
            result = model.transcribe(audio_path, word_timestamps=True)
            
            # Generar SRT
            srt_content = ""
            for i, segment in enumerate(result["segments"], 1):
                start = self.format_timestamp(segment["start"])
                end = self.format_timestamp(segment["end"])
                text = segment["text"].strip()
                
                srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
            
            srt_path = project_path / "subtitles_es.srt"
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            return str(srt_path)
            
        except Exception as e:
            print(f"❌ Error generando subtítulos: {e}")
            return None
    
    def format_timestamp(self, seconds: float) -> str:
        """Formatear timestamp para SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def create_thumbnail(self, content: Dict) -> str:
        """Crear miniatura con branding Cine Norte"""
        print("🖼️ Creando miniatura...")
        
        project_name = f"{datetime.now().strftime('%Y%m%d')}_{content['title'].replace(' ', '_')}"
        project_path = self.project_dir / project_name
        
        # Crear imagen base
        width, height = 1280, 720
        img = Image.new('RGB', (width, height), color='#0A0A0A')
        draw = ImageDraw.Draw(img)
        
        # Gradiente de fondo
        for y in range(height):
            color_value = int(10 + (y / height) * 50)  # Negro a gris
            draw.line([(0, y), (width, y)], fill=(color_value, color_value, color_value))
        
        # Barra roja diagonal
        draw.polygon([(0, height-100), (width, height-50), (width, height), (0, height)], fill='#E50914')
        
        # Texto del título
        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 30)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Título principal
        title_text = content['title']
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = height // 2 - 50
        
        # Sombra del título
        draw.text((title_x + 3, title_y + 3), title_text, font=title_font, fill='#000000')
        # Título principal
        draw.text((title_x, title_y), title_text, font=title_font, fill='#C0C0C0')
        
        # Subtítulo
        subtitle_text = f"Disponible en {content['platform']}"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = title_y + 80
        
        draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill='#E50914')
        
        # Logo Cine Norte
        logo_text = "CINE NORTE"
        logo_bbox = draw.textbbox((0, 0), logo_text, font=subtitle_font)
        logo_width = logo_bbox[2] - logo_bbox[0]
        logo_x = (width - logo_width) // 2
        logo_y = height - 40
        
        draw.text((logo_x, logo_y), logo_text, font=subtitle_font, fill='#E50914')
        
        # Guardar miniatura
        thumbnail_path = project_path / "thumbnail.png"
        img.save(thumbnail_path)
        
        return str(thumbnail_path)
    
    def generate_seo_content(self, content: Dict) -> Dict:
        """Generar títulos y hashtags optimizados"""
        print("🔍 Generando contenido SEO...")
        
        # Cargar prompt de SEO
        with open(self.prompts_dir / "02_seo_titles_hashtags.txt", 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        prompt = prompt_template.format(
            title=content['title'],
            platform=content['platform'],
            genres=', '.join(content['genres'])
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            seo_content = response.choices[0].message.content
            
            # Parsear respuesta
            lines = seo_content.split('\n')
            titles = []
            hashtags = []
            
            in_titles = False
            in_hashtags = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('Títulos:'):
                    in_titles = True
                    continue
                elif line.startswith('Hashtags:'):
                    in_titles = False
                    in_hashtags = True
                    continue
                elif line and in_titles and line[0].isdigit():
                    titles.append(line.split(')', 1)[1].strip())
                elif line and in_hashtags and line.startswith('#'):
                    hashtags.append(line)
            
            return {
                'titles': titles,
                'hashtags': hashtags
            }
            
        except Exception as e:
            print(f"❌ Error generando SEO: {e}")
            return {
                'titles': [f"{content['title']} - {content['platform']}", f"Nueva en {content['platform']}: {content['title']}"],
                'hashtags': ['#CineNorte', f'#{content["platform"]}', f'#{content["genres"][0]}', '#Estrenos']
            }
    
    def create_video(self, content: Dict, audio_path: str, subtitles_path: str) -> Dict:
        """Crear video final con branding Cine Norte"""
        print("🎬 Creando video final...")
        
        project_name = f"{datetime.now().strftime('%Y%m%d')}_{content['title'].replace(' ', '_')}"
        project_path = self.project_dir / project_name
        export_path = self.exports_dir / project_name
        export_path.mkdir(exist_ok=True)
        
        try:
            # Crear video simple con texto (en producción real, usar clips reales)
            duration = 30  # 30 segundos de ejemplo
            
            # Video base negro
            video = VideoFileClip("assets/black_screen.mp4") if os.path.exists("assets/black_screen.mp4") else None
            
            if not video:
                # Crear video negro si no existe
                from moviepy.editor import ColorClip
                video = ColorClip(size=(1920, 1080), color=(10, 10, 10), duration=duration)
            
            # Audio
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                video = video.set_audio(audio)
            
            # Texto del título
            title_text = TextClip(
                content['title'],
                fontsize=80,
                color='#C0C0C0',
                font='Arial-Bold'
            ).set_position('center').set_duration(duration)
            
            # Texto de plataforma
            platform_text = TextClip(
                f"Disponible en {content['platform']}",
                fontsize=40,
                color='#E50914',
                font='Arial'
            ).set_position(('center', 200)).set_duration(duration)
            
            # Compositar video
            final_video = CompositeVideoClip([video, title_text, platform_text])
            
            # Exportar en diferentes formatos
            outputs = {}
            
            # 16:9 (YouTube/Facebook)
            final_video.write_videofile(
                str(export_path / "video_16x9.mp4"),
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            outputs['16x9'] = str(export_path / "video_16x9.mp4")
            
            # 9:16 (TikTok/Reels) - recortar y redimensionar
            vertical_video = final_video.crop(x_center=960, width=540, height=960)
            vertical_video.write_videofile(
                str(export_path / "video_9x16.mp4"),
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            outputs['9x16'] = str(export_path / "video_9x16.mp4")
            
            # 1:1 (Instagram/Facebook)
            square_video = final_video.crop(x_center=960, y_center=540, width=1080, height=1080)
            square_video.write_videofile(
                str(export_path / "video_1x1.mp4"),
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            outputs['1x1'] = str(export_path / "video_1x1.mp4")
            
            return outputs
            
        except Exception as e:
            print(f"❌ Error creando video: {e}")
            return {}
    
    def run_full_workflow(self, content: Dict) -> Dict:
        """Ejecutar flujo completo de automatización"""
        print(f"🚀 Iniciando flujo completo para: {content['title']}")
        
        results = {
            'content': content,
            'script': None,
            'audio': None,
            'subtitles': None,
            'thumbnail': None,
            'seo': None,
            'videos': {}
        }
        
        try:
            # 1. Generar guion
            results['script'] = self.generate_script(content)
            
            # 2. Generar locución
            results['audio'] = self.generate_voiceover(results['script'], content)
            
            # 3. Generar subtítulos
            if results['audio']:
                results['subtitles'] = self.generate_subtitles(results['audio'], results['script'])
            
            # 4. Crear miniatura
            results['thumbnail'] = self.create_thumbnail(content)
            
            # 5. Generar contenido SEO
            results['seo'] = self.generate_seo_content(content)
            
            # 6. Crear videos
            results['videos'] = self.create_video(content, results['audio'], results['subtitles'])
            
            print("✅ Flujo completo finalizado exitosamente")
            
        except Exception as e:
            print(f"❌ Error en el flujo: {e}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Cine Norte Automation System')
    parser.add_argument('--config', default='config.yaml', help='Archivo de configuración')
    parser.add_argument('--platform', help='Plataforma específica (Netflix, HBO Max, etc.)')
    parser.add_argument('--genre', help='Género específico')
    parser.add_argument('--limit', type=int, default=1, help='Número de contenidos a procesar')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    automation = CineNorteAutomation(args.config)
    
    # Seleccionar contenido
    content_list = automation.select_content(args.platform, args.genre, args.limit)
    
    if not content_list:
        print("❌ No se encontró contenido para procesar")
        return
    
    # Procesar cada contenido
    for content in content_list:
        print(f"\n🎬 Procesando: {content['title']} ({content['year']})")
        results = automation.run_full_workflow(content)
        
        # Mostrar resultados
        print(f"\n📊 Resultados para {content['title']}:")
        print(f"  ✅ Guion: {'✓' if results['script'] else '✗'}")
        print(f"  ✅ Audio: {'✓' if results['audio'] else '✗'}")
        print(f"  ✅ Subtítulos: {'✓' if results['subtitles'] else '✗'}")
        print(f"  ✅ Miniatura: {'✓' if results['thumbnail'] else '✗'}")
        print(f"  ✅ Videos: {len(results['videos'])} formatos generados")
        
        if results['seo']:
            print(f"  📝 Títulos sugeridos: {len(results['seo']['titles'])}")
            print(f"  #️⃣ Hashtags: {len(results['seo']['hashtags'])}")

if __name__ == "__main__":
    main()
