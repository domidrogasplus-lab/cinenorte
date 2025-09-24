"""
Sistema de síntesis de voz y subtítulos para Cine Norte
Convierte guiones a audio y genera subtítulos sincronizados
"""
import os
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import json
from datetime import timedelta
import re

# Importaciones para síntesis de voz
try:
    from gtts import gTTS
    import pygame
    from pydub import AudioSegment
    from pydub.effects import normalize, compress_dynamic_range
    from pydub.silence import split_on_silence
except ImportError:
    print("Instalando dependencias de audio...")
    os.system("pip install gtts pygame pydub")

# Importaciones para subtítulos
try:
    import webvtt
    from webvtt import WebVTT
except ImportError:
    print("Instalando dependencias de subtítulos...")
    os.system("pip install webvtt-py")

from config import config
from script_generator import ScriptSection, GeneratedScript

@dataclass
class AudioSegment:
    """Segmento de audio con metadatos"""
    text: str
    audio_file: str
    start_time: float
    end_time: float
    duration: float
    emphasis_words: List[str]
    emotion: str
    volume_adjustment: float = 1.0

@dataclass
class SubtitleCue:
    """Cue de subtítulo"""
    start_time: str  # Formato HH:MM:SS.mmm
    end_time: str
    text: str
    speaker: str = "Narrador"
    style: str = "default"

@dataclass
class VoiceProfile:
    """Perfil de voz personalizado"""
    name: str
    language: str
    speed: float
    pitch: float
    volume: float
    voice_id: str = "default"

class VoiceSynthesizer:
    """Sintetizador de voz para Cine Norte"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp()
        
        # Perfiles de voz predefinidos
        self.voice_profiles = {
            "cinenorte_male": VoiceProfile(
                name="Cine Norte Masculino",
                language="es",
                speed=0.9,
                pitch=0.8,
                volume=1.0,
                voice_id="es-mx-male"
            ),
            "cinenorte_female": VoiceProfile(
                name="Cine Norte Femenino", 
                language="es",
                speed=0.95,
                pitch=1.1,
                volume=1.0,
                voice_id="es-mx-female"
            ),
            "dramatic": VoiceProfile(
                name="Dramático",
                language="es",
                speed=0.8,
                pitch=0.7,
                volume=1.1,
                voice_id="es-mx-dramatic"
            ),
            "energetic": VoiceProfile(
                name="Energético",
                language="es", 
                speed=1.1,
                pitch=1.2,
                volume=1.0,
                voice_id="es-mx-energetic"
            )
        }
        
        self.current_profile = self.voice_profiles["cinenorte_male"]
        
    def synthesize_script(self, script: GeneratedScript, 
                         voice_profile: str = "cinenorte_male",
                         output_format: str = "mp3") -> Tuple[str, List[SubtitleCue]]:
        """
        Sintetiza un guion completo a audio con subtítulos
        
        Args:
            script: Guion generado
            voice_profile: Perfil de voz a usar
            output_format: Formato de salida (mp3, wav, ogg)
            
        Returns:
            Tuple con (ruta_audio, lista_subtitulos)
        """
        try:
            # Configurar perfil de voz
            if voice_profile in self.voice_profiles:
                self.current_profile = self.voice_profiles[voice_profile]
            
            # Procesar cada sección del guion
            audio_segments = []
            subtitle_cues = []
            current_time = 0.0
            
            for section in script.sections:
                # Generar audio para la sección
                segment = self._synthesize_section(
                    section, 
                    current_time,
                    script.target_platform
                )
                
                if segment:
                    audio_segments.append(segment)
                    
                    # Generar subtítulos para la sección
                    section_cues = self._generate_subtitles_for_section(
                        section, 
                        current_time,
                        segment.duration
                    )
                    subtitle_cues.extend(section_cues)
                    
                    current_time += segment.duration
            
            # Combinar todos los segmentos de audio
            final_audio_path = self._combine_audio_segments(
                audio_segments, 
                script.title,
                output_format
            )
            
            # Aplicar efectos finales
            final_audio_path = self._apply_final_effects(final_audio_path, script)
            
            return final_audio_path, subtitle_cues
            
        except Exception as e:
            self.logger.error(f"Error sintetizando guion: {e}")
            return None, []
    
    def _synthesize_section(self, section: ScriptSection, start_time: float, 
                           platform: str) -> Optional[AudioSegment]:
        """Sintetiza una sección individual del guion"""
        try:
            # Preparar texto para síntesis
            processed_text = self._prepare_text_for_synthesis(section.content, section.emphasis_words)
            
            # Generar audio con gTTS
            tts = gTTS(
                text=processed_text,
                lang=self.current_profile.language,
                slow=False
            )
            
            # Guardar audio temporal
            temp_audio_path = os.path.join(self.temp_dir, f"section_{section.type}_{start_time}.mp3")
            tts.save(temp_audio_path)
            
            # Cargar y procesar audio
            audio = AudioSegment.from_mp3(temp_audio_path)
            
            # Aplicar ajustes de perfil de voz
            audio = self._apply_voice_profile(audio, section.emotion)
            
            # Ajustar duración si es necesario
            target_duration = section.duration_seconds * 1000  # Convertir a ms
            if len(audio) > target_duration:
                audio = audio[:target_duration]
            elif len(audio) < target_duration * 0.8:  # Si es muy corto, ajustar velocidad
                speed_factor = len(audio) / (target_duration * 0.9)
                audio = audio.speedup(playback_speed=speed_factor)
            
            # Guardar audio procesado
            processed_audio_path = os.path.join(self.temp_dir, f"processed_{section.type}_{start_time}.mp3")
            audio.export(processed_audio_path, format="mp3")
            
            return AudioSegment(
                text=section.content,
                audio_file=processed_audio_path,
                start_time=start_time,
                end_time=start_time + (len(audio) / 1000.0),
                duration=len(audio) / 1000.0,
                emphasis_words=section.emphasis_words,
                emotion=section.emotion
            )
            
        except Exception as e:
            self.logger.error(f"Error sintetizando sección {section.type}: {e}")
            return None
    
    def _prepare_text_for_synthesis(self, text: str, emphasis_words: List[str]) -> str:
        """Prepara el texto para síntesis con énfasis"""
        processed_text = text
        
        # Agregar pausas naturales
        processed_text = re.sub(r'([.!?])\s+', r'\1... ', processed_text)
        processed_text = re.sub(r'([,;:])\s+', r'\1... ', processed_text)
        
        # Agregar énfasis a palabras clave
        for word in emphasis_words:
            if word.lower() in processed_text.lower():
                # Envolver palabra en tags de énfasis (gTTS no soporta SSML completo)
                processed_text = re.sub(
                    f'\\b{re.escape(word)}\\b', 
                    f'<emphasis level="strong">{word}</emphasis>',
                    processed_text, 
                    flags=re.IGNORECASE
                )
        
        return processed_text
    
    def _apply_voice_profile(self, audio: AudioSegment, emotion: str) -> AudioSegment:
        """Aplica el perfil de voz y efectos emocionales"""
        # Aplicar velocidad
        if self.current_profile.speed != 1.0:
            audio = audio.speedup(playback_speed=self.current_profile.speed)
        
        # Aplicar volumen
        if self.current_profile.volume != 1.0:
            audio = audio + (self.current_profile.volume - 1.0) * 20  # dB
        
        # Aplicar efectos emocionales
        if emotion == "excitement":
            # Aumentar ligeramente la velocidad y volumen
            audio = audio.speedup(playback_speed=1.05)
            audio = audio + 2  # +2dB
        elif emotion == "suspense":
            # Reducir velocidad y volumen para crear tensión
            audio = audio.speedup(playback_speed=0.95)
            audio = audio - 1  # -1dB
        elif emotion == "drama":
            # Velocidad ligeramente más lenta para dramatismo
            audio = audio.speedup(playback_speed=0.9)
        
        # Normalizar audio
        audio = normalize(audio)
        
        # Aplicar compresión dinámica suave
        audio = compress_dynamic_range(audio, threshold=-20.0, ratio=4.0, attack=5.0, release=50.0)
        
        return audio
    
    def _generate_subtitles_for_section(self, section: ScriptSection, start_time: float, 
                                       duration: float) -> List[SubtitleCue]:
        """Genera subtítulos para una sección"""
        cues = []
        
        # Dividir texto en líneas apropiadas para subtítulos
        lines = self._split_text_for_subtitles(section.content, duration)
        
        line_duration = duration / len(lines) if lines else 1.0
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            cue_start = start_time + (i * line_duration)
            cue_end = cue_start + line_duration
            
            cue = SubtitleCue(
                start_time=self._format_time(cue_start),
                end_time=self._format_time(cue_end),
                text=line.strip(),
                speaker="Cine Norte",
                style=self._get_subtitle_style(section.type)
            )
            cues.append(cue)
        
        return cues
    
    def _split_text_for_subtitles(self, text: str, duration: float) -> List[str]:
        """Divide el texto en líneas apropiadas para subtítulos"""
        # Dividir por oraciones primero
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calcular palabras por segundo (aproximadamente 3 palabras por segundo)
        words_per_second = 3.0
        max_words_per_line = int((duration / len(sentences)) * words_per_second) if sentences else 10
        
        lines = []
        current_line = ""
        
        for sentence in sentences:
            words = sentence.split()
            
            if len(current_line.split()) + len(words) <= max_words_per_line:
                if current_line:
                    current_line += " " + sentence
                else:
                    current_line = sentence
            else:
                if current_line:
                    lines.append(current_line)
                current_line = sentence
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _get_subtitle_style(self, section_type: str) -> str:
        """Obtiene el estilo de subtítulo según el tipo de sección"""
        styles = {
            "intro": "intro_style",
            "hook": "hook_style", 
            "plot": "plot_style",
            "analysis": "analysis_style",
            "outro": "outro_style"
        }
        return styles.get(section_type, "default")
    
    def _format_time(self, seconds: float) -> str:
        """Formatea tiempo en formato HH:MM:SS.mmm"""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"
    
    def _combine_audio_segments(self, segments: List[AudioSegment], title: str, 
                               output_format: str) -> str:
        """Combina todos los segmentos de audio en un archivo final"""
        if not segments:
            return None
        
        # Cargar primer segmento
        combined_audio = AudioSegment.from_mp3(segments[0].audio_file)
        
        # Agregar pausa inicial
        silence = AudioSegment.silent(duration=500)  # 0.5 segundos
        combined_audio = silence + combined_audio
        
        # Combinar con el resto de segmentos
        for i, segment in enumerate(segments[1:], 1):
            # Agregar pausa entre segmentos
            pause_duration = 200 if segment.emotion != "suspense" else 500  # 0.2-0.5 segundos
            silence = AudioSegment.silent(duration=pause_duration)
            
            segment_audio = AudioSegment.from_mp3(segment.audio_file)
            combined_audio = combined_audio + silence + segment_audio
        
        # Agregar pausa final
        final_silence = AudioSegment.silent(duration=1000)  # 1 segundo
        combined_audio = combined_audio + final_silence
        
        # Guardar archivo final
        output_filename = f"audio_{title.replace(' ', '_')}.{output_format}"
        output_path = os.path.join(self.temp_dir, output_filename)
        combined_audio.export(output_path, format=output_format)
        
        return output_path
    
    def _apply_final_effects(self, audio_path: str, script: GeneratedScript) -> str:
        """Aplica efectos finales al audio"""
        try:
            audio = AudioSegment.from_file(audio_path)
            
            # Normalizar volumen final
            audio = normalize(audio)
            
            # Aplicar fade in/out
            fade_duration = 1000  # 1 segundo
            audio = audio.fade_in(fade_duration).fade_out(fade_duration)
            
            # Aplicar compresión final
            audio = compress_dynamic_range(audio, threshold=-18.0, ratio=3.0, attack=3.0, release=30.0)
            
            # Guardar audio final
            final_path = audio_path.replace('.mp3', '_final.mp3')
            audio.export(final_path, format="mp3", bitrate="192k")
            
            return final_path
            
        except Exception as e:
            self.logger.error(f"Error aplicando efectos finales: {e}")
            return audio_path
    
    def export_subtitles(self, cues: List[SubtitleCue], filename: str = None) -> str:
        """Exporta subtítulos en formato WebVTT"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"subtitulos_{timestamp}.vtt"
        
        # Crear archivo WebVTT
        vtt = WebVTT()
        
        for cue in cues:
            vtt.cues.append(webvtt.Cue(
                start=cue.start_time,
                end=cue.end_time,
                text=cue.text
            ))
        
        # Guardar archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(vtt))
        
        return filename
    
    def export_subtitles_srt(self, cues: List[SubtitleCue], filename: str = None) -> str:
        """Exporta subtítulos en formato SRT"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"subtitulos_{timestamp}.srt"
        
        srt_content = ""
        
        for i, cue in enumerate(cues, 1):
            # Convertir formato de tiempo
            start_srt = cue.start_time.replace('.', ',')
            end_srt = cue.end_time.replace('.', ',')
            
            srt_content += f"{i}\n"
            srt_content += f"{start_srt} --> {end_srt}\n"
            srt_content += f"{cue.text}\n\n"
        
        # Guardar archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        return filename
    
    def create_voice_profile(self, name: str, language: str = "es", 
                           speed: float = 1.0, pitch: float = 1.0, 
                           volume: float = 1.0) -> VoiceProfile:
        """Crea un perfil de voz personalizado"""
        profile = VoiceProfile(
            name=name,
            language=language,
            speed=speed,
            pitch=pitch,
            volume=volume,
            voice_id=f"custom_{name.lower().replace(' ', '_')}"
        )
        
        self.voice_profiles[profile.voice_id] = profile
        return profile
    
    def get_available_voices(self) -> List[VoiceProfile]:
        """Obtiene lista de voces disponibles"""
        return list(self.voice_profiles.values())
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.error(f"Error limpiando archivos temporales: {e}")

# Instancia global del sintetizador
voice_synthesizer = VoiceSynthesizer()
