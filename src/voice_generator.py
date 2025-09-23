"""
Sistema de generación de voz IA y subtítulos automáticos
"""

import os
import tempfile
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path

# Text-to-Speech
from gtts import gTTS
import pyttsx3

# Audio processing
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import librosa
import soundfile as sf

# Subtitle generation
import whisper
import pysrt

from config import AUDIO_CONFIG, API_KEYS

logger = logging.getLogger(__name__)

@dataclass
class VoiceSettings:
    """Configuración de voz para TTS"""
    language: str = "es"
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    voice_id: Optional[str] = None

@dataclass
class SubtitleEntry:
    """Entrada de subtítulo con timing"""
    start_time: float
    end_time: float
    text: str
    confidence: float = 1.0

class VoiceGenerator:
    """Generador de voz IA y subtítulos automáticos"""
    
    def __init__(self):
        self.voice_settings = VoiceSettings(**AUDIO_CONFIG["voice_settings"])
        self.temp_dir = Path("temp/audio")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Inicializar modelos de IA
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Carga el modelo Whisper para transcripción"""
        try:
            self.whisper_model = whisper.load_model("base")
            logger.info("Modelo Whisper cargado exitosamente")
        except Exception as e:
            logger.error(f"Error cargando modelo Whisper: {e}")
            self.whisper_model = None
    
    def generate_voice_from_script(self, script_text: str, output_path: str = None) -> str:
        """
        Genera archivo de audio a partir del texto del guion
        
        Args:
            script_text: Texto del guion
            output_path: Ruta de salida (opcional)
        """
        try:
            if not output_path:
                output_path = self.temp_dir / "generated_voice.mp3"
            
            # Usar gTTS como método principal
            tts = gTTS(
                text=script_text,
                lang=self.voice_settings.language,
                slow=False
            )
            
            # Guardar archivo temporal
            temp_file = self.temp_dir / "temp_voice.mp3"
            tts.save(str(temp_file))
            
            # Procesar audio para mejorar calidad
            processed_audio = self._process_audio(str(temp_file))
            
            # Guardar archivo final
            processed_audio.export(str(output_path), format="mp3", bitrate="192k")
            
            # Limpiar archivo temporal
            temp_file.unlink()
            
            logger.info(f"Voz generada exitosamente: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generando voz: {e}")
            return self._generate_fallback_voice(script_text, output_path)
    
    def generate_voice_with_elevenlabs(self, script_text: str, output_path: str = None) -> str:
        """
        Genera voz usando ElevenLabs (requiere API key)
        
        Args:
            script_text: Texto del guion
            output_path: Ruta de salida
        """
        try:
            elevenlabs_key = API_KEYS.get("elevenlabs")
            if not elevenlabs_key:
                logger.warning("API key de ElevenLabs no disponible, usando gTTS")
                return self.generate_voice_from_script(script_text, output_path)
            
            # Implementación con ElevenLabs
            import requests
            
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": elevenlabs_key
            }
            
            data = {
                "text": script_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            if not output_path:
                output_path = self.temp_dir / "elevenlabs_voice.mp3"
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Voz ElevenLabs generada: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error con ElevenLabs: {e}")
            return self.generate_voice_from_script(script_text, output_path)
    
    def _process_audio(self, audio_path: str) -> AudioSegment:
        """Procesa el audio para mejorar calidad"""
        try:
            # Cargar audio
            audio = AudioSegment.from_mp3(audio_path)
            
            # Normalizar volumen
            audio = normalize(audio)
            
            # Aplicar compresión dinámica
            audio = compress_dynamic_range(audio)
            
            # Ajustar velocidad si es necesario
            if self.voice_settings.speed != 1.0:
                audio = audio.speedup(playback_speed=self.voice_settings.speed)
            
            # Ajustar pitch si es necesario
            if self.voice_settings.pitch != 0.0:
                # Convertir a numpy array para procesamiento de pitch
                samples = audio.get_array_of_samples()
                samples = librosa.effects.pitch_shift(
                    samples, 
                    sr=audio.frame_rate, 
                    n_steps=self.voice_settings.pitch
                )
                audio = AudioSegment(
                    samples.tobytes(),
                    frame_rate=audio.frame_rate,
                    sample_width=audio.sample_width,
                    channels=audio.channels
                )
            
            return audio
            
        except Exception as e:
            logger.error(f"Error procesando audio: {e}")
            return AudioSegment.from_mp3(audio_path)
    
    def generate_subtitles(self, audio_path: str, script_text: str = None) -> List[SubtitleEntry]:
        """
        Genera subtítulos automáticos usando Whisper
        
        Args:
            audio_path: Ruta del archivo de audio
            script_text: Texto del guion (opcional, para mejor precisión)
        """
        try:
            if not self.whisper_model:
                logger.warning("Modelo Whisper no disponible, generando subtítulos básicos")
                return self._generate_basic_subtitles(script_text)
            
            # Transcribir audio con Whisper
            result = self.whisper_model.transcribe(audio_path, language="es")
            
            # Convertir a formato de subtítulos
            subtitles = []
            for segment in result["segments"]:
                subtitle = SubtitleEntry(
                    start_time=segment["start"],
                    end_time=segment["end"],
                    text=segment["text"].strip(),
                    confidence=segment.get("no_speech_prob", 0.0)
                )
                subtitles.append(subtitle)
            
            logger.info(f"Subtítulos generados: {len(subtitles)} entradas")
            return subtitles
            
        except Exception as e:
            logger.error(f"Error generando subtítulos: {e}")
            return self._generate_basic_subtitles(script_text)
    
    def _generate_basic_subtitles(self, script_text: str) -> List[SubtitleEntry]:
        """Genera subtítulos básicos basados en el texto del guion"""
        if not script_text:
            return []
        
        # Dividir texto en oraciones
        sentences = self._split_into_sentences(script_text)
        
        # Calcular timing basado en palabras por minuto
        words_per_minute = 150
        subtitles = []
        current_time = 0.0
        
        for sentence in sentences:
            word_count = len(sentence.split())
            duration = (word_count / words_per_minute) * 60
            
            subtitle = SubtitleEntry(
                start_time=current_time,
                end_time=current_time + duration,
                text=sentence.strip()
            )
            subtitles.append(subtitle)
            current_time += duration
        
        return subtitles
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Divide el texto en oraciones"""
        import re
        
        # Patrón para dividir en oraciones
        sentence_pattern = r'(?<=[.!?])\s+'
        sentences = re.split(sentence_pattern, text)
        
        # Filtrar oraciones vacías
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def save_subtitles_srt(self, subtitles: List[SubtitleEntry], output_path: str) -> str:
        """Guarda los subtítulos en formato SRT"""
        try:
            srt_file = pysrt.SubRipFile()
            
            for i, subtitle in enumerate(subtitles, 1):
                srt_item = pysrt.SubRipItem(
                    index=i,
                    start=pysrt.SubRipTime(seconds=subtitle.start_time),
                    end=pysrt.SubRipTime(seconds=subtitle.end_time),
                    text=subtitle.text
                )
                srt_file.append(srt_item)
            
            srt_file.save(output_path, encoding='utf-8')
            logger.info(f"Subtítulos SRT guardados: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error guardando subtítulos SRT: {e}")
            return ""
    
    def save_subtitles_vtt(self, subtitles: List[SubtitleEntry], output_path: str) -> str:
        """Guarda los subtítulos en formato VTT (WebVTT)"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("WEBVTT\n\n")
                
                for subtitle in subtitles:
                    start_time = self._format_vtt_time(subtitle.start_time)
                    end_time = self._format_vtt_time(subtitle.end_time)
                    
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{subtitle.text}\n\n")
            
            logger.info(f"Subtítulos VTT guardados: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error guardando subtítulos VTT: {e}")
            return ""
    
    def _format_vtt_time(self, seconds: float) -> str:
        """Formatea tiempo para formato VTT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
    
    def _generate_fallback_voice(self, script_text: str, output_path: str) -> str:
        """Genera voz de respaldo usando pyttsx3"""
        try:
            engine = pyttsx3.init()
            
            # Configurar propiedades de voz
            voices = engine.getProperty('voices')
            if voices:
                # Buscar voz en español
                for voice in voices:
                    if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            engine.setProperty('rate', int(150 * self.voice_settings.speed))
            engine.setProperty('volume', self.voice_settings.volume)
            
            # Generar audio
            engine.save_to_file(script_text, str(output_path))
            engine.runAndWait()
            
            logger.info(f"Voz de respaldo generada: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generando voz de respaldo: {e}")
            return ""
    
    def create_voice_with_music(self, voice_path: str, music_path: str, output_path: str) -> str:
        """
        Combina voz con música de fondo
        
        Args:
            voice_path: Ruta del archivo de voz
            music_path: Ruta del archivo de música
            output_path: Ruta de salida
        """
        try:
            # Cargar archivos de audio
            voice = AudioSegment.from_mp3(voice_path)
            music = AudioSegment.from_mp3(music_path)
            
            # Ajustar duración de la música a la voz
            if len(music) > len(voice):
                music = music[:len(voice)]
            elif len(music) < len(voice):
                # Repetir música si es más corta
                repeats = (len(voice) // len(music)) + 1
                music = music * repeats
                music = music[:len(voice)]
            
            # Reducir volumen de la música (fade in/out)
            music = music - 20  # Reducir 20dB
            music = music.fade_in(2000).fade_out(2000)
            
            # Combinar audio
            combined = voice.overlay(music)
            
            # Exportar resultado
            combined.export(output_path, format="mp3", bitrate="192k")
            
            logger.info(f"Audio con música generado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error combinando audio: {e}")
            return voice_path  # Retornar solo la voz si hay error
    
    def get_voice_duration(self, audio_path: str) -> float:
        """Obtiene la duración del archivo de audio en segundos"""
        try:
            audio = AudioSegment.from_mp3(audio_path)
            return len(audio) / 1000.0  # Convertir de ms a segundos
        except Exception as e:
            logger.error(f"Error obteniendo duración: {e}")
            return 0.0
