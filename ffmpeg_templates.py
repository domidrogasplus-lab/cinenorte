#!/usr/bin/env python3
"""
FFmpeg Templates para Cine Norte
Plantillas predefinidas para edición de video con branding
"""

import ffmpeg
import os
from pathlib import Path

class CineNorteFFmpeg:
    def __init__(self, config: dict):
        self.config = config
        self.colors = config.get('branding', {}).get('colors', {})
        self.video_config = config.get('video', {})
        self.audio_config = config.get('audio', {})
    
    def create_intro_logo(self, duration: float = 3.0) -> ffmpeg.Stream:
        """Crear intro con logo Cine Norte animado"""
        # Crear fondo negro con gradiente
        background = ffmpeg.input(
            f"color=c={self.colors.get('background', '#0A0A0A')}:size=1920x1080:duration={duration}",
            f="lavfi"
        )
        
        # Efecto de barrido de luz (simulado con overlay)
        light_sweep = ffmpeg.input(
            f"color=c=white:size=1920x1080:duration={duration}",
            f="lavfi"
        ).filter('geq', r='if(lt(X/W*T*2,1),255,0)', g='if(lt(X/W*T*2,1),255,0)', b='if(lt(X/W*T*2,1),255,0)')
        
        # Logo Cine Norte (texto por ahora)
        logo_text = ffmpeg.input(
            f"color=c=black:size=1920x1080:duration={duration}",
            f="lavfi"
        ).drawtext(
            text="CINE NORTE",
            fontfile="arial.ttf",
            fontsize=120,
            fontcolor=self.colors.get('primary', '#E50914'),
            x="(w-text_w)/2",
            y="(h-text_h)/2",
            shadowcolor="black",
            shadowx=5,
            shadowy=5
        )
        
        # Compositar elementos
        intro = ffmpeg.filter([background, light_sweep, logo_text], 'overlay')
        
        return intro
    
    def create_outro_logo(self, duration: float = 3.0) -> ffmpeg.Stream:
        """Crear outro con logo Cine Norte"""
        # Fondo negro
        background = ffmpeg.input(
            f"color=c={self.colors.get('background', '#0A0A0A')}:size=1920x1080:duration={duration}",
            f="lavfi"
        )
        
        # Logo con CTA
        outro_text = ffmpeg.input(
            f"color=c=black:size=1920x1080:duration={duration}",
            f="lavfi"
        ).drawtext(
            text="CINE NORTE",
            fontfile="arial.ttf",
            fontsize=100,
            fontcolor=self.colors.get('primary', '#E50914'),
            x="(w-text_w)/2",
            y="(h-text_h)/2-50",
            shadowcolor="black",
            shadowx=3,
            shadowy=3
        ).drawtext(
            text="¡Suscríbete para más contenido!",
            fontfile="arial.ttf",
            fontsize=40,
            fontcolor=self.colors.get('accent', '#C0C0C0'),
            x="(w-text_w)/2",
            y="(h-text_h)/2+80",
            shadowcolor="black",
            shadowx=2,
            shadowy=2
        )
        
        outro = ffmpeg.filter([background, outro_text], 'overlay')
        return outro
    
    def add_branding_overlay(self, video_input: ffmpeg.Stream, platform: str) -> ffmpeg.Stream:
        """Agregar overlay de branding (lower-third con plataforma)"""
        # Lower-third con plataforma
        platform_config = self.config.get('platforms', {}).get(platform.lower().replace(' ', '_'), {})
        platform_color = platform_config.get('color', self.colors.get('primary', '#E50914'))
        
        # Fondo del lower-third
        lower_third = ffmpeg.input(
            f"color=c={platform_color}:size=400x80:duration=10",
            f="lavfi"
        ).drawtext(
            text=f"Disponible en {platform}",
            fontfile="arial.ttf",
            fontsize=24,
            fontcolor="white",
            x="20",
            y="(h-text_h)/2",
            shadowcolor="black",
            shadowx=1,
            shadowy=1
        )
        
        # Posicionar en esquina inferior izquierda
        positioned_lower_third = lower_third.filter('scale', 400, 80).filter(
            'overlay', x=20, y='h-h-20'
        )
        
        # Aplicar overlay al video
        branded_video = ffmpeg.filter([video_input, positioned_lower_third], 'overlay')
        
        return branded_video
    
    def add_subtitles(self, video_input: ffmpeg.Stream, subtitle_file: str) -> ffmpeg.Stream:
        """Agregar subtítulos con estilo Cine Norte"""
        subtitle_config = self.config.get('subtitles', {})
        
        video_with_subs = video_input.filter(
            'subtitles',
            subtitle_file,
            force_style=f"Fontname={subtitle_config.get('font', 'Inter')},"
                       f"Fontsize={subtitle_config.get('font_size', 24)},"
                       f"Outline={subtitle_config.get('outline', 2)},"
                       f"Shadow={subtitle_config.get('shadow', 1)},"
                       f"PrimaryColour=&H00C0C0C0&,"  # Plateado
                       f"OutlineColour=&H00000000&,"  # Negro
                       f"ShadowColour=&H80000000&"    # Sombra
        )
        
        return video_with_subs
    
    def normalize_audio(self, audio_input: ffmpeg.Stream) -> ffmpeg.Stream:
        """Normalizar audio con loudness y ducking"""
        target_lufs = self.audio_config.get('target_lufs', -16)
        ducking_db = self.audio_config.get('ducking_db', -8)
        
        # Normalizar loudness
        normalized_audio = audio_input.filter(
            'loudnorm',
            I=target_lufs,
            LRA=11,
            TP=-1.5
        )
        
        return normalized_audio
    
    def create_16x9_video(self, video_input: ffmpeg.Stream, audio_input: ffmpeg.Stream, 
                         output_path: str, intro_duration: float = 3.0, outro_duration: float = 3.0) -> ffmpeg.Stream:
        """Crear video 16:9 completo con intro, contenido y outro"""
        
        # Crear intro
        intro = self.create_intro_logo(intro_duration)
        
        # Crear outro
        outro = self.create_outro_logo(outro_duration)
        
        # Procesar video principal
        processed_video = self.add_branding_overlay(video_input, "Netflix")  # Por defecto
        processed_video = self.add_subtitles(processed_video, "subtitles.srt")
        
        # Normalizar audio
        processed_audio = self.normalize_audio(audio_input)
        
        # Concatenar intro + video + outro
        full_video = ffmpeg.concat(intro, processed_video, outro, v=1, a=0)
        
        # Configurar salida
        output = ffmpeg.output(
            full_video,
            processed_audio,
            output_path,
            vcodec=self.video_config.get('codec', 'libx264'),
            acodec=self.video_config.get('audio_codec', 'aac'),
            **{
                'b:v': self.video_config.get('master_bitrate', '20M'),
                'b:a': f"{self.audio_config.get('bitrate', 320)}k",
                'r': self.video_config.get('master_fps', 24),
                'pix_fmt': 'yuv420p'
            }
        )
        
        return output
    
    def create_9x16_video(self, video_input: ffmpeg.Stream, audio_input: ffmpeg.Stream, 
                         output_path: str) -> ffmpeg.Stream:
        """Crear video 9:16 para TikTok/Reels"""
        
        # Recortar y redimensionar a 9:16
        cropped_video = video_input.filter(
            'crop',
            'ih*9/16',  # Ancho = altura * 9/16
            'ih',       # Altura original
            '(iw-ih*9/16)/2',  # X centrado
            '0'         # Y = 0
        ).filter(
            'scale',
            1080, 1920  # Resolución final 9:16
        )
        
        # Aplicar branding y subtítulos
        processed_video = self.add_branding_overlay(cropped_video, "TikTok")
        processed_video = self.add_subtitles(processed_video, "subtitles.srt")
        
        # Normalizar audio
        processed_audio = self.normalize_audio(audio_input)
        
        # Configurar salida
        output = ffmpeg.output(
            processed_video,
            processed_audio,
            output_path,
            vcodec=self.video_config.get('codec', 'libx264'),
            acodec=self.video_config.get('audio_codec', 'aac'),
            **{
                'b:v': '15M',  # Bitrate menor para móviles
                'b:a': f"{self.audio_config.get('bitrate', 320)}k",
                'r': self.video_config.get('master_fps', 24),
                'pix_fmt': 'yuv420p'
            }
        )
        
        return output
    
    def create_1x1_video(self, video_input: ffmpeg.Stream, audio_input: ffmpeg.Stream, 
                        output_path: str) -> ffmpeg.Stream:
        """Crear video 1:1 para Instagram/Facebook"""
        
        # Recortar a cuadrado centrado
        square_video = video_input.filter(
            'crop',
            'ih',       # Ancho = altura (cuadrado)
            'ih',       # Altura original
            '(iw-ih)/2',  # X centrado
            '0'         # Y = 0
        ).filter(
            'scale',
            1080, 1080  # Resolución final 1:1
        )
        
        # Aplicar branding y subtítulos
        processed_video = self.add_branding_overlay(square_video, "Instagram")
        processed_video = self.add_subtitles(processed_video, "subtitles.srt")
        
        # Normalizar audio
        processed_audio = self.normalize_audio(audio_input)
        
        # Configurar salida
        output = ffmpeg.output(
            processed_video,
            processed_audio,
            output_path,
            vcodec=self.video_config.get('codec', 'libx264'),
            acodec=self.video_config.get('audio_codec', 'aac'),
            **{
                'b:v': '12M',  # Bitrate para redes sociales
                'b:a': f"{self.audio_config.get('bitrate', 320)}k",
                'r': self.video_config.get('master_fps', 24),
                'pix_fmt': 'yuv420p'
            }
        )
        
        return output
    
    def create_thumbnail(self, video_input: ffmpeg.Stream, output_path: str, 
                        timestamp: str = "00:00:05") -> ffmpeg.Stream:
        """Crear miniatura desde frame específico"""
        
        # Extraer frame en timestamp específico
        thumbnail = video_input.filter(
            'select',
            f'eq(n,{self.timestamp_to_frame(timestamp)})'
        ).filter(
            'scale',
            1280, 720  # Resolución YouTube
        )
        
        # Agregar overlay de branding
        branded_thumbnail = thumbnail.drawtext(
            text="CINE NORTE",
            fontfile="arial.ttf",
            fontsize=60,
            fontcolor=self.colors.get('primary', '#E50914'),
            x="(w-text_w)/2",
            y="h-100",
            shadowcolor="black",
            shadowx=3,
            shadowy=3
        )
        
        # Configurar salida como imagen
        output = ffmpeg.output(
            branded_thumbnail,
            output_path,
            vframes=1,
            f='image2'
        )
        
        return output
    
    def timestamp_to_frame(self, timestamp: str, fps: int = 24) -> int:
        """Convertir timestamp a número de frame"""
        parts = timestamp.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds * fps
    
    def run_ffmpeg_command(self, output_stream: ffmpeg.Stream, overwrite: bool = True) -> bool:
        """Ejecutar comando FFmpeg"""
        try:
            cmd = ffmpeg.compile(output_stream, overwrite_output=overwrite)
            ffmpeg.run(cmd, quiet=True)
            return True
        except ffmpeg.Error as e:
            print(f"❌ Error FFmpeg: {e}")
            return False

# Ejemplo de uso
if __name__ == "__main__":
    import yaml
    
    # Cargar configuración
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Crear instancia
    ffmpeg_templates = CineNorteFFmpeg(config)
    
    # Ejemplo: crear video 16:9
    video_input = ffmpeg.input('input_video.mp4')
    audio_input = ffmpeg.input('input_audio.wav')
    
    output_stream = ffmpeg_templates.create_16x9_video(
        video_input, 
        audio_input, 
        'output_16x9.mp4'
    )
    
    # Ejecutar
    success = ffmpeg_templates.run_ffmpeg_command(output_stream)
    print(f"Video creado: {'✅' if success else '❌'}")
