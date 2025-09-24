"""
Sistema de optimización con IA para Cine Norte
Analiza y optimiza contenido para máximo engagement
"""
import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import json
import re
from datetime import datetime
import numpy as np

# Importaciones para análisis de video
try:
    import cv2
    from moviepy.editor import VideoFileClip
    import matplotlib.pyplot as plt
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("Instalando dependencias de optimización...")
    os.system("pip install opencv-python moviepy matplotlib scikit-learn")

# Importaciones para IA
try:
    import openai
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
except ImportError:
    print("Instalando dependencias de IA...")
    os.system("pip install openai transformers torch")

from config import config
from script_generator import GeneratedScript, ScriptSection
from content_analyzer import ContentInfo

@dataclass
class OptimizationAnalysis:
    """Análisis de optimización"""
    content_score: float
    engagement_potential: float
    viral_probability: float
    seo_score: float
    visual_impact: float
    audio_quality: float
    overall_score: float
    recommendations: List[str]
    improvements: List[str]

@dataclass
class SEOOptimization:
    """Optimización SEO"""
    title_suggestions: List[str]
    description_suggestions: List[str]
    hashtag_suggestions: List[str]
    keyword_density: Dict[str, float]
    trending_keywords: List[str]

@dataclass
class VisualAnalysis:
    """Análisis visual"""
    color_analysis: Dict[str, Any]
    motion_analysis: Dict[str, Any]
    composition_score: float
    visual_hooks: List[Tuple[float, str]]  # (tiempo, descripción)
    recommended_cuts: List[Tuple[float, float]]  # (inicio, fin)

@dataclass
class AudioAnalysis:
    """Análisis de audio"""
    volume_consistency: float
    speech_clarity: float
    music_balance: float
    silence_analysis: List[Tuple[float, float]]  # (inicio, fin) de silencios
    recommended_adjustments: List[str]

class AIOptimizer:
    """Optimizador con IA para contenido de Cine Norte"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configurar OpenAI
        self.openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Cargar modelos de IA
        self._load_ai_models()
        
        # Configurar análisis de video
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def _load_ai_models(self):
        """Carga modelos de IA necesarios"""
        try:
            # Modelo para análisis de sentimientos
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
            
            # Modelo para análisis de texto
            self.text_analyzer = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium"
            )
            
            # Tokenizador para análisis de texto
            self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
            
        except Exception as e:
            self.logger.error(f"Error cargando modelos de IA: {e}")
            self.sentiment_analyzer = None
            self.text_analyzer = None
            self.tokenizer = None
    
    def optimize_content(self, script: GeneratedScript, content_info: ContentInfo,
                        video_path: str = None) -> OptimizationAnalysis:
        """
        Optimiza contenido completo con IA
        
        Args:
            script: Guion generado
            content_info: Información del contenido
            video_path: Ruta del video (opcional)
            
        Returns:
            Análisis de optimización completo
        """
        try:
            # Análisis de contenido
            content_score = self._analyze_content_quality(script, content_info)
            
            # Análisis de engagement
            engagement_potential = self._analyze_engagement_potential(script)
            
            # Análisis de viralidad
            viral_probability = self._analyze_viral_potential(script, content_info)
            
            # Análisis SEO
            seo_analysis = self._analyze_seo_optimization(script, content_info)
            
            # Análisis visual (si hay video)
            visual_analysis = None
            visual_impact = 0.0
            if video_path and os.path.exists(video_path):
                visual_analysis = self._analyze_visual_content(video_path)
                visual_impact = visual_analysis.composition_score
            
            # Análisis de audio
            audio_analysis = self._analyze_audio_quality(script)
            
            # Calcular score general
            overall_score = self._calculate_overall_score(
                content_score, engagement_potential, viral_probability,
                seo_analysis, visual_impact, audio_analysis
            )
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations(
                content_score, engagement_potential, viral_probability,
                seo_analysis, visual_analysis, audio_analysis
            )
            
            # Generar mejoras específicas
            improvements = self._generate_improvements(
                script, content_info, visual_analysis, audio_analysis
            )
            
            return OptimizationAnalysis(
                content_score=content_score,
                engagement_potential=engagement_potential,
                viral_probability=viral_probability,
                seo_score=seo_analysis.get("overall_score", 0.0),
                visual_impact=visual_impact,
                audio_quality=audio_analysis.volume_consistency,
                overall_score=overall_score,
                recommendations=recommendations,
                improvements=improvements
            )
            
        except Exception as e:
            self.logger.error(f"Error optimizando contenido: {e}")
            return self._create_fallback_analysis()
    
    def _analyze_content_quality(self, script: GeneratedScript, content_info: ContentInfo) -> float:
        """Analiza calidad del contenido"""
        try:
            score = 0.0
            
            # Análisis de longitud del guion
            word_count = script.word_count
            if 100 <= word_count <= 500:  # Rango óptimo
                score += 20
            elif 50 <= word_count <= 800:  # Rango aceptable
                score += 15
            else:
                score += 10
            
            # Análisis de estructura
            section_count = len(script.sections)
            if 3 <= section_count <= 6:  # Estructura óptima
                score += 20
            elif 2 <= section_count <= 8:  # Estructura aceptable
                score += 15
            else:
                score += 10
            
            # Análisis de duración
            duration = script.total_duration
            if 60 <= duration <= 180:  # Duración óptima
                score += 20
            elif 30 <= duration <= 240:  # Duración aceptable
                score += 15
            else:
                score += 10
            
            # Análisis de popularidad del contenido
            popularity_score = min(content_info.popularity / 100, 1) * 20
            score += popularity_score
            
            # Análisis de rating
            rating_score = (content_info.rating / 10) * 20
            score += rating_score
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error analizando calidad: {e}")
            return 50.0
    
    def _analyze_engagement_potential(self, script: GeneratedScript) -> float:
        """Analiza potencial de engagement"""
        try:
            score = 0.0
            
            # Análisis de palabras emocionales
            emotional_words = self._count_emotional_words(script.raw_text)
            emotional_score = min(emotional_words / 10, 1) * 25
            score += emotional_score
            
            # Análisis de preguntas y call-to-actions
            questions = len(re.findall(r'\?', script.raw_text))
            ctas = len(re.findall(r'(suscríbete|comenta|like|comparte)', script.raw_text, re.IGNORECASE))
            interaction_score = min((questions + ctas) / 5, 1) * 25
            score += interaction_score
            
            # Análisis de hooks y ganchos
            hooks = self._analyze_hooks(script)
            hook_score = min(hooks / 3, 1) * 25
            score += hook_score
            
            # Análisis de variedad de emociones
            emotion_variety = len(set(section.emotion for section in script.sections))
            variety_score = min(emotion_variety / 4, 1) * 25
            score += variety_score
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error analizando engagement: {e}")
            return 50.0
    
    def _analyze_viral_potential(self, script: GeneratedScript, content_info: ContentInfo) -> float:
        """Analiza potencial viral"""
        try:
            score = 0.0
            
            # Análisis de trending topics
            trending_score = self._analyze_trending_keywords(script.raw_text)
            score += trending_score * 30
            
            # Análisis de controversia (sin spoilers)
            controversy_score = self._analyze_controversy_potential(script, content_info)
            score += controversy_score * 20
            
            # Análisis de shareability
            shareability_score = self._analyze_shareability(script)
            score += shareability_score * 25
            
            # Análisis de timing
            timing_score = self._analyze_timing_relevance(content_info)
            score += timing_score * 25
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error analizando viralidad: {e}")
            return 50.0
    
    def _analyze_seo_optimization(self, script: GeneratedScript, content_info: ContentInfo) -> Dict:
        """Analiza optimización SEO"""
        try:
            # Análisis de keywords
            keywords = self._extract_keywords(script.raw_text)
            keyword_density = self._calculate_keyword_density(script.raw_text, keywords)
            
            # Análisis de títulos
            title_score = self._analyze_title_optimization(script.title_suggestions)
            
            # Análisis de hashtags
            hashtag_score = self._analyze_hashtag_optimization(script.hashtags)
            
            # Análisis de descripción
            description_score = self._analyze_description_optimization(script.raw_text)
            
            # Score general SEO
            overall_score = (title_score + hashtag_score + description_score) / 3
            
            return {
                "overall_score": overall_score,
                "keywords": keywords,
                "keyword_density": keyword_density,
                "title_score": title_score,
                "hashtag_score": hashtag_score,
                "description_score": description_score
            }
            
        except Exception as e:
            self.logger.error(f"Error analizando SEO: {e}")
            return {"overall_score": 50.0}
    
    def _analyze_visual_content(self, video_path: str) -> VisualAnalysis:
        """Analiza contenido visual del video"""
        try:
            # Cargar video
            cap = cv2.VideoCapture(video_path)
            
            color_analysis = self._analyze_colors(cap)
            motion_analysis = self._analyze_motion(cap)
            composition_score = self._analyze_composition(cap)
            visual_hooks = self._find_visual_hooks(cap)
            recommended_cuts = self._recommend_cuts(cap)
            
            cap.release()
            
            return VisualAnalysis(
                color_analysis=color_analysis,
                motion_analysis=motion_analysis,
                composition_score=composition_score,
                visual_hooks=visual_hooks,
                recommended_cuts=recommended_cuts
            )
            
        except Exception as e:
            self.logger.error(f"Error analizando contenido visual: {e}")
            return VisualAnalysis(
                color_analysis={},
                motion_analysis={},
                composition_score=50.0,
                visual_hooks=[],
                recommended_cuts=[]
            )
    
    def _analyze_audio_quality(self, script: GeneratedScript) -> AudioAnalysis:
        """Analiza calidad del audio"""
        try:
            # Análisis de consistencia de volumen
            volume_consistency = self._analyze_volume_consistency(script)
            
            # Análisis de claridad del habla
            speech_clarity = self._analyze_speech_clarity(script)
            
            # Análisis de balance musical
            music_balance = self._analyze_music_balance(script)
            
            # Análisis de silencios
            silence_analysis = self._analyze_silences(script)
            
            # Recomendaciones de ajuste
            adjustments = self._generate_audio_adjustments(
                volume_consistency, speech_clarity, music_balance
            )
            
            return AudioAnalysis(
                volume_consistency=volume_consistency,
                speech_clarity=speech_clarity,
                music_balance=music_balance,
                silence_analysis=silence_analysis,
                recommended_adjustments=adjustments
            )
            
        except Exception as e:
            self.logger.error(f"Error analizando audio: {e}")
            return AudioAnalysis(
                volume_consistency=50.0,
                speech_clarity=50.0,
                music_balance=50.0,
                silence_analysis=[],
                recommended_adjustments=[]
            )
    
    def _count_emotional_words(self, text: str) -> int:
        """Cuenta palabras emocionales en el texto"""
        emotional_words = [
            'increíble', 'espectacular', 'impresionante', 'sorprendente',
            'emocionante', 'intenso', 'dramático', 'épico', 'genial',
            'fantástico', 'excelente', 'maravilloso', 'asombroso'
        ]
        
        count = 0
        text_lower = text.lower()
        for word in emotional_words:
            count += text_lower.count(word)
        
        return count
    
    def _analyze_hooks(self, script: GeneratedScript) -> int:
        """Analiza hooks y ganchos en el guion"""
        hook_patterns = [
            r'¿.*\?',  # Preguntas
            r'¡.*!',   # Exclamaciones
            r'(nunca|siempre|definitivamente|absolutamente)',
            r'(descubre|conoce|aprende|mira)',
            r'(spoiler|revelación|sorpresa)'
        ]
        
        hook_count = 0
        for pattern in hook_patterns:
            hook_count += len(re.findall(pattern, script.raw_text, re.IGNORECASE))
        
        return hook_count
    
    def _analyze_trending_keywords(self, text: str) -> float:
        """Analiza keywords trending en el texto"""
        # Keywords trending en entretenimiento (ejemplo)
        trending_keywords = [
            'netflix', 'disney', 'marvel', 'dc', 'streaming',
            'película', 'serie', 'tráiler', 'estreno', 'nuevo'
        ]
        
        text_lower = text.lower()
        found_keywords = sum(1 for keyword in trending_keywords if keyword in text_lower)
        
        return min(found_keywords / len(trending_keywords), 1.0)
    
    def _analyze_controversy_potential(self, script: GeneratedScript, content_info: ContentInfo) -> float:
        """Analiza potencial de controversia (sin spoilers)"""
        # Palabras que generan controversia sin spoilers
        controversy_words = [
            'polémico', 'debate', 'discutido', 'controversial',
            'divisivo', 'opinión', 'crítico', 'revisión'
        ]
        
        text_lower = script.raw_text.lower()
        controversy_count = sum(1 for word in controversy_words if word in text_lower)
        
        return min(controversy_count / 5, 1.0)
    
    def _analyze_shareability(self, script: GeneratedScript) -> float:
        """Analiza potencial de compartir"""
        shareability_indicators = [
            'comparte', 'compartir', 'viral', 'tendencia',
            'recomienda', 'recomendación', 'debe ver', 'no te pierdas'
        ]
        
        text_lower = script.raw_text.lower()
        shareability_count = sum(1 for indicator in shareability_indicators if indicator in text_lower)
        
        return min(shareability_count / 3, 1.0)
    
    def _analyze_timing_relevance(self, content_info: ContentInfo) -> float:
        """Analiza relevancia temporal del contenido"""
        # Contenido reciente tiene mayor potencial viral
        try:
            from datetime import datetime
            release_date = datetime.strptime(content_info.release_date, "%Y-%m-%d")
            days_old = (datetime.now() - release_date).days
            
            if days_old <= 30:  # Muy reciente
                return 1.0
            elif days_old <= 90:  # Reciente
                return 0.8
            elif days_old <= 365:  # Moderadamente reciente
                return 0.6
            else:  # Antiguo
                return 0.4
        except:
            return 0.5
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae keywords del texto"""
        # Usar TF-IDF para extraer keywords importantes
        try:
            vectorizer = TfidfVectorizer(max_features=20, stop_words='spanish')
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Obtener scores
            scores = tfidf_matrix.toarray()[0]
            
            # Combinar keywords con scores
            keywords_with_scores = list(zip(feature_names, scores))
            keywords_with_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [kw[0] for kw in keywords_with_scores[:10]]
        except:
            return []
    
    def _calculate_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """Calcula densidad de keywords"""
        word_count = len(text.split())
        densities = {}
        
        for keyword in keywords:
            count = text.lower().count(keyword.lower())
            density = (count / word_count) * 100
            densities[keyword] = density
        
        return densities
    
    def _analyze_title_optimization(self, titles: List[str]) -> float:
        """Analiza optimización de títulos"""
        if not titles:
            return 0.0
        
        scores = []
        for title in titles:
            score = 0.0
            
            # Longitud óptima (50-60 caracteres)
            if 50 <= len(title) <= 60:
                score += 30
            elif 40 <= len(title) <= 70:
                score += 20
            else:
                score += 10
            
            # Palabras clave emocionales
            emotional_words = ['increíble', 'sorprendente', 'épico', 'mejor', 'peor']
            emotional_count = sum(1 for word in emotional_words if word in title.lower())
            score += min(emotional_count * 10, 30)
            
            # Números y símbolos
            if re.search(r'[0-9]', title):
                score += 10
            if re.search(r'[!?]', title):
                score += 10
            
            # Palabras de acción
            action_words = ['descubre', 'mira', 'conoce', 'aprende', 'revela']
            action_count = sum(1 for word in action_words if word in title.lower())
            score += min(action_count * 10, 20)
            
            scores.append(min(score, 100))
        
        return sum(scores) / len(scores)
    
    def _analyze_hashtag_optimization(self, hashtags: List[str]) -> float:
        """Analiza optimización de hashtags"""
        if not hashtags:
            return 0.0
        
        score = 0.0
        
        # Cantidad óptima (5-15 hashtags)
        if 5 <= len(hashtags) <= 15:
            score += 30
        elif 3 <= len(hashtags) <= 20:
            score += 20
        else:
            score += 10
        
        # Diversidad de hashtags
        unique_hashtags = len(set(hashtags))
        diversity_score = min(unique_hashtags / len(hashtags), 1) * 20
        score += diversity_score
        
        # Hashtags trending
        trending_hashtags = ['#viral', '#tendencia', '#nuevo', '#estreno', '#netflix']
        trending_count = sum(1 for tag in hashtags if tag.lower() in trending_hashtags)
        score += min(trending_count * 10, 30)
        
        # Longitud de hashtags
        avg_length = sum(len(tag) for tag in hashtags) / len(hashtags)
        if 5 <= avg_length <= 15:
            score += 20
        else:
            score += 10
        
        return min(score, 100)
    
    def _analyze_description_optimization(self, text: str) -> float:
        """Analiza optimización de descripción"""
        score = 0.0
        
        # Longitud óptima (150-300 caracteres)
        if 150 <= len(text) <= 300:
            score += 30
        elif 100 <= len(text) <= 400:
            score += 20
        else:
            score += 10
        
        # Call-to-action
        cta_words = ['suscríbete', 'comenta', 'comparte', 'like', 'síguenos']
        cta_count = sum(1 for word in cta_words if word in text.lower())
        score += min(cta_count * 15, 30)
        
        # Palabras clave
        keyword_density = len(re.findall(r'\b\w+\b', text)) / len(text.split())
        if 0.1 <= keyword_density <= 0.3:
            score += 20
        else:
            score += 10
        
        # Emojis (opcional)
        emoji_count = len(re.findall(r'[^\w\s]', text))
        if 1 <= emoji_count <= 5:
            score += 20
        else:
            score += 10
        
        return min(score, 100)
    
    def _calculate_overall_score(self, content_score: float, engagement_potential: float,
                               viral_probability: float, seo_analysis: Dict,
                               visual_impact: float, audio_analysis: AudioAnalysis) -> float:
        """Calcula score general de optimización"""
        weights = {
            'content': 0.25,
            'engagement': 0.25,
            'viral': 0.20,
            'seo': 0.15,
            'visual': 0.10,
            'audio': 0.05
        }
        
        seo_score = seo_analysis.get('overall_score', 0.0)
        audio_score = (audio_analysis.volume_consistency + audio_analysis.speech_clarity) / 2
        
        overall_score = (
            content_score * weights['content'] +
            engagement_potential * weights['engagement'] +
            viral_probability * weights['viral'] +
            seo_score * weights['seo'] +
            visual_impact * weights['visual'] +
            audio_score * weights['audio']
        )
        
        return min(100, overall_score)
    
    def _generate_recommendations(self, content_score: float, engagement_potential: float,
                                viral_probability: float, seo_analysis: Dict,
                                visual_analysis: Optional[VisualAnalysis],
                                audio_analysis: AudioAnalysis) -> List[str]:
        """Genera recomendaciones de optimización"""
        recommendations = []
        
        # Recomendaciones de contenido
        if content_score < 70:
            recommendations.append("Mejora la estructura del guion con más secciones definidas")
            recommendations.append("Ajusta la duración para estar entre 60-180 segundos")
        
        # Recomendaciones de engagement
        if engagement_potential < 70:
            recommendations.append("Agrega más preguntas y call-to-actions")
            recommendations.append("Incluye más palabras emocionales y hooks")
        
        # Recomendaciones de viralidad
        if viral_probability < 70:
            recommendations.append("Incorpora más keywords trending")
            recommendations.append("Aumenta el potencial de controversia sin spoilers")
        
        # Recomendaciones SEO
        seo_score = seo_analysis.get('overall_score', 0.0)
        if seo_score < 70:
            recommendations.append("Optimiza títulos con más palabras clave emocionales")
            recommendations.append("Mejora la diversidad y relevancia de hashtags")
        
        # Recomendaciones visuales
        if visual_analysis and visual_analysis.composition_score < 70:
            recommendations.append("Mejora la composición visual del video")
            recommendations.append("Agrega más elementos visuales llamativos")
        
        # Recomendaciones de audio
        if audio_analysis.volume_consistency < 70:
            recommendations.append("Normaliza el volumen del audio")
            recommendations.append("Mejora la claridad del habla")
        
        return recommendations
    
    def _generate_improvements(self, script: GeneratedScript, content_info: ContentInfo,
                             visual_analysis: Optional[VisualAnalysis],
                             audio_analysis: AudioAnalysis) -> List[str]:
        """Genera mejoras específicas"""
        improvements = []
        
        # Mejoras de guion
        if script.word_count < 100:
            improvements.append("Expandir el guion con más detalles y análisis")
        elif script.word_count > 500:
            improvements.append("Condensar el guion para mayor impacto")
        
        # Mejoras de estructura
        if len(script.sections) < 3:
            improvements.append("Agregar más secciones para mejor estructura")
        
        # Mejoras de duración
        if script.total_duration < 60:
            improvements.append("Extender la duración para mayor engagement")
        elif script.total_duration > 180:
            improvements.append("Reducir la duración para mantener atención")
        
        # Mejoras de audio
        if audio_analysis.silence_analysis:
            improvements.append("Reducir silencios largos en el audio")
        
        return improvements
    
    def _create_fallback_analysis(self) -> OptimizationAnalysis:
        """Crea análisis de respaldo si falla la optimización"""
        return OptimizationAnalysis(
            content_score=50.0,
            engagement_potential=50.0,
            viral_probability=50.0,
            seo_score=50.0,
            visual_impact=50.0,
            audio_quality=50.0,
            overall_score=50.0,
            recommendations=["Revisar configuración de IA", "Verificar calidad del contenido"],
            improvements=["Optimizar configuración", "Mejorar calidad general"]
        )
    
    # Métodos auxiliares para análisis visual y de audio
    def _analyze_colors(self, cap) -> Dict:
        """Analiza colores del video"""
        # Implementación simplificada
        return {"dominant_colors": [], "color_consistency": 0.5}
    
    def _analyze_motion(self, cap) -> Dict:
        """Analiza movimiento en el video"""
        # Implementación simplificada
        return {"motion_intensity": 0.5, "motion_consistency": 0.5}
    
    def _analyze_composition(self, cap) -> float:
        """Analiza composición del video"""
        # Implementación simplificada
        return 75.0
    
    def _find_visual_hooks(self, cap) -> List[Tuple[float, str]]:
        """Encuentra hooks visuales"""
        # Implementación simplificada
        return [(5.0, "Transición dramática"), (15.0, "Primer plano emocional")]
    
    def _recommend_cuts(self, cap) -> List[Tuple[float, float]]:
        """Recomienda cortes en el video"""
        # Implementación simplificada
        return [(10.0, 12.0), (25.0, 27.0)]
    
    def _analyze_volume_consistency(self, script: GeneratedScript) -> float:
        """Analiza consistencia de volumen"""
        # Implementación simplificada
        return 75.0
    
    def _analyze_speech_clarity(self, script: GeneratedScript) -> float:
        """Analiza claridad del habla"""
        # Implementación simplificada
        return 80.0
    
    def _analyze_music_balance(self, script: GeneratedScript) -> float:
        """Analiza balance musical"""
        # Implementación simplificada
        return 70.0
    
    def _analyze_silences(self, script: GeneratedScript) -> List[Tuple[float, float]]:
        """Analiza silencios en el audio"""
        # Implementación simplificada
        return [(5.0, 6.0), (15.0, 16.0)]
    
    def _generate_audio_adjustments(self, volume: float, clarity: float, balance: float) -> List[str]:
        """Genera recomendaciones de ajuste de audio"""
        adjustments = []
        
        if volume < 70:
            adjustments.append("Aumentar volumen general")
        if clarity < 70:
            adjustments.append("Mejorar claridad del habla")
        if balance < 70:
            adjustments.append("Ajustar balance musical")
        
        return adjustments

# Instancia global del optimizador
ai_optimizer = AIOptimizer()
