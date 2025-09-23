"""
Sistema de optimización con IA para análisis de impacto y mejoras
"""

import os
import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
from datetime import datetime
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import openai

from config import API_KEYS, SEO_CONFIG
from src.script_generator import GeneratedScript, ScriptSegment
from src.video_editor import VideoProject

logger = logging.getLogger(__name__)

@dataclass
class ImpactAnalysis:
    """Análisis de impacto de contenido"""
    engagement_score: float
    viral_potential: float
    seo_score: float
    visual_appeal: float
    overall_score: float
    recommendations: List[str]
    strengths: List[str]
    weaknesses: List[str]

@dataclass
class OptimizationSuggestion:
    """Sugerencia de optimización"""
    type: str  # 'title', 'thumbnail', 'script', 'timing', 'visual'
    priority: str  # 'high', 'medium', 'low'
    description: str
    impact: float  # 0-1
    implementation: str

@dataclass
class SEOAnalysis:
    """Análisis SEO del contenido"""
    title_score: float
    description_score: float
    hashtag_score: float
    keyword_density: Dict[str, float]
    trending_keywords: List[str]
    suggestions: List[str]

class AIOptimizer:
    """Sistema de optimización con IA para contenido de Cine Norte"""
    
    def __init__(self):
        self.openai_api_key = API_KEYS.get("openai")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Cargar datos de referencia
        self._load_reference_data()
        
        # Inicializar modelos de análisis
        self._initialize_models()
    
    def _load_reference_data(self):
        """Carga datos de referencia para análisis"""
        try:
            # Datos de palabras clave trending
            self.trending_keywords = [
                "netflix", "disney", "hbo", "prime video", "streaming",
                "película", "serie", "análisis", "reseña", "spoiler",
                "acción", "drama", "comedia", "terror", "ciencia ficción",
                "marvel", "dc", "anime", "documental", "thriller"
            ]
            
            # Patrones de títulos exitosos
            self.successful_title_patterns = [
                r".*ANÁLISIS.*",
                r".*RESEÑA.*",
                r".*REACCIÓN.*",
                r".*SPOILERS.*",
                r".*EXPLICADO.*",
                r".*DETALLES.*"
            ]
            
            # Palabras de alto impacto
            self.high_impact_words = [
                "increíble", "espectacular", "sorprendente", "impactante",
                "brillante", "genial", "perfecto", "excelente", "magnífico",
                "terrible", "decepcionante", "aburrido", "confuso", "revelador"
            ]
            
            logger.info("Datos de referencia cargados exitosamente")
            
        except Exception as e:
            logger.error(f"Error cargando datos de referencia: {e}")
            self.trending_keywords = []
            self.successful_title_patterns = []
            self.high_impact_words = []
    
    def _initialize_models(self):
        """Inicializa modelos de machine learning"""
        try:
            # Vectorizador TF-IDF para análisis de texto
            self.text_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Modelo de clustering para categorización
            self.clustering_model = KMeans(n_clusters=5, random_state=42)
            
            logger.info("Modelos de ML inicializados exitosamente")
            
        except Exception as e:
            logger.error(f"Error inicializando modelos: {e}")
            self.text_vectorizer = None
            self.clustering_model = None
    
    def analyze_content_impact(self, project: VideoProject) -> ImpactAnalysis:
        """
        Analiza el impacto potencial del contenido
        
        Args:
            project: Proyecto de video a analizar
            
        Returns:
            Análisis de impacto completo
        """
        try:
            # Análisis de engagement
            engagement_score = self._analyze_engagement(project)
            
            # Análisis de potencial viral
            viral_potential = self._analyze_viral_potential(project)
            
            # Análisis SEO
            seo_score = self._analyze_seo(project)
            
            # Análisis de atractivo visual
            visual_appeal = self._analyze_visual_appeal(project)
            
            # Calcular score general
            overall_score = (engagement_score + viral_potential + seo_score + visual_appeal) / 4
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations(project, {
                'engagement': engagement_score,
                'viral': viral_potential,
                'seo': seo_score,
                'visual': visual_appeal
            })
            
            # Identificar fortalezas y debilidades
            strengths, weaknesses = self._identify_strengths_weaknesses(project, {
                'engagement': engagement_score,
                'viral': viral_potential,
                'seo': seo_score,
                'visual': visual_appeal
            })
            
            return ImpactAnalysis(
                engagement_score=engagement_score,
                viral_potential=viral_potential,
                seo_score=seo_score,
                visual_appeal=visual_appeal,
                overall_score=overall_score,
                recommendations=recommendations,
                strengths=strengths,
                weaknesses=weaknesses
            )
            
        except Exception as e:
            logger.error(f"Error analizando impacto: {e}")
            return self._create_fallback_analysis()
    
    def _analyze_engagement(self, project: VideoProject) -> float:
        """Analiza el potencial de engagement del contenido"""
        try:
            score = 0.0
            
            # Análisis del título
            title_score = self._analyze_title_engagement(project.title)
            score += title_score * 0.3
            
            # Análisis del guion
            script_score = self._analyze_script_engagement(project.script)
            score += script_score * 0.4
            
            # Análisis de duración
            duration_score = self._analyze_duration_engagement(project.duration)
            score += duration_score * 0.2
            
            # Análisis de hashtags
            hashtag_score = self._analyze_hashtag_engagement(project.script.hashtags)
            score += hashtag_score * 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando engagement: {e}")
            return 0.5
    
    def _analyze_title_engagement(self, title: str) -> float:
        """Analiza el engagement del título"""
        try:
            score = 0.0
            title_lower = title.lower()
            
            # Palabras de alto impacto
            impact_words = sum(1 for word in self.high_impact_words if word in title_lower)
            score += min(impact_words * 0.2, 0.6)
            
            # Patrones exitosos
            import re
            pattern_matches = sum(1 for pattern in self.successful_title_patterns 
                               if re.search(pattern, title, re.IGNORECASE))
            score += min(pattern_matches * 0.3, 0.4)
            
            # Longitud óptima (50-60 caracteres)
            length = len(title)
            if 50 <= length <= 60:
                score += 0.2
            elif 40 <= length <= 70:
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando título: {e}")
            return 0.5
    
    def _analyze_script_engagement(self, script: GeneratedScript) -> float:
        """Analiza el engagement del guion"""
        try:
            score = 0.0
            
            # Análisis de longitud del guion
            word_count = len(script.raw_text.split())
            if 200 <= word_count <= 500:  # Rango óptimo
                score += 0.3
            elif 150 <= word_count <= 600:
                score += 0.2
            
            # Análisis de estructura
            segment_count = len(script.segments)
            if 3 <= segment_count <= 6:  # Estructura óptima
                score += 0.2
            
            # Análisis de palabras de impacto
            impact_word_count = sum(1 for word in self.high_impact_words 
                                  if word in script.raw_text.lower())
            score += min(impact_word_count * 0.1, 0.3)
            
            # Análisis de preguntas retóricas
            question_count = script.raw_text.count('?')
            score += min(question_count * 0.05, 0.2)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando guion: {e}")
            return 0.5
    
    def _analyze_duration_engagement(self, duration: float) -> float:
        """Analiza el engagement basado en duración"""
        try:
            # Duración óptima: 2-3 minutos
            if 120 <= duration <= 180:
                return 1.0
            elif 90 <= duration <= 240:
                return 0.8
            elif 60 <= duration <= 300:
                return 0.6
            else:
                return 0.4
                
        except Exception as e:
            logger.error(f"Error analizando duración: {e}")
            return 0.5
    
    def _analyze_hashtag_engagement(self, hashtags: List[str]) -> float:
        """Analiza el engagement de los hashtags"""
        try:
            if not hashtags:
                return 0.0
            
            score = 0.0
            
            # Número óptimo de hashtags (5-10)
            hashtag_count = len(hashtags)
            if 5 <= hashtag_count <= 10:
                score += 0.4
            elif 3 <= hashtag_count <= 15:
                score += 0.2
            
            # Hashtags trending
            trending_hashtags = sum(1 for tag in hashtags 
                                  if any(keyword in tag.lower() for keyword in self.trending_keywords))
            score += min(trending_hashtags * 0.1, 0.4)
            
            # Diversidad de hashtags
            unique_hashtags = len(set(hashtags))
            if unique_hashtags == len(hashtags):  # Todos únicos
                score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando hashtags: {e}")
            return 0.5
    
    def _analyze_viral_potential(self, project: VideoProject) -> float:
        """Analiza el potencial viral del contenido"""
        try:
            score = 0.0
            
            # Análisis del contenido
            content = project.script.content
            
            # Géneros populares
            popular_genres = ["Acción", "Ciencia ficción", "Terror", "Drama", "Comedia"]
            genre_score = sum(1 for genre in content.genres if genre in popular_genres)
            score += min(genre_score * 0.2, 0.4)
            
            # Rating alto
            if content.rating >= 7.0:
                score += 0.3
            elif content.rating >= 6.0:
                score += 0.2
            
            # Popularidad
            if content.popularity >= 50:
                score += 0.2
            elif content.popularity >= 20:
                score += 0.1
            
            # Contenido controversial o trending
            controversial_keywords = ["spoiler", "polémico", "revelación", "secreto"]
            controversial_score = sum(1 for keyword in controversial_keywords 
                                   if keyword in project.script.raw_text.lower())
            score += min(controversial_score * 0.1, 0.1)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando potencial viral: {e}")
            return 0.5
    
    def _analyze_seo(self, project: VideoProject) -> float:
        """Analiza el SEO del contenido"""
        try:
            score = 0.0
            
            # Análisis del título
            title_seo = self._analyze_title_seo(project.title)
            score += title_seo * 0.4
            
            # Análisis de la descripción
            description_seo = self._analyze_description_seo(project.script.description)
            score += description_seo * 0.3
            
            # Análisis de hashtags
            hashtag_seo = self._analyze_hashtag_seo(project.script.hashtags)
            score += hashtag_seo * 0.3
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando SEO: {e}")
            return 0.5
    
    def _analyze_title_seo(self, title: str) -> float:
        """Analiza el SEO del título"""
        try:
            score = 0.0
            
            # Longitud óptima para SEO (50-60 caracteres)
            length = len(title)
            if 50 <= length <= 60:
                score += 0.4
            elif 40 <= length <= 70:
                score += 0.2
            
            # Palabras clave relevantes
            relevant_keywords = sum(1 for keyword in self.trending_keywords 
                                  if keyword in title.lower())
            score += min(relevant_keywords * 0.2, 0.4)
            
            # Palabras de alto impacto
            impact_words = sum(1 for word in self.high_impact_words 
                             if word in title.lower())
            score += min(impact_words * 0.1, 0.2)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando SEO del título: {e}")
            return 0.5
    
    def _analyze_description_seo(self, description: str) -> float:
        """Analiza el SEO de la descripción"""
        try:
            score = 0.0
            
            # Longitud óptima (150-160 caracteres)
            length = len(description)
            if 150 <= length <= 160:
                score += 0.4
            elif 120 <= length <= 200:
                score += 0.2
            
            # Palabras clave en descripción
            relevant_keywords = sum(1 for keyword in self.trending_keywords 
                                  if keyword in description.lower())
            score += min(relevant_keywords * 0.2, 0.4)
            
            # Call-to-action
            cta_words = ["suscríbete", "like", "comenta", "comparte"]
            cta_score = sum(1 for word in cta_words if word in description.lower())
            score += min(cta_score * 0.1, 0.2)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando SEO de descripción: {e}")
            return 0.5
    
    def _analyze_hashtag_seo(self, hashtags: List[str]) -> float:
        """Analiza el SEO de los hashtags"""
        try:
            if not hashtags:
                return 0.0
            
            score = 0.0
            
            # Hashtags trending
            trending_hashtags = sum(1 for tag in hashtags 
                                  if any(keyword in tag.lower() for keyword in self.trending_keywords))
            score += min(trending_hashtags * 0.2, 0.6)
            
            # Diversidad de hashtags
            unique_hashtags = len(set(hashtags))
            if unique_hashtags == len(hashtags):
                score += 0.2
            
            # Hashtags específicos de la industria
            industry_hashtags = ["#cine", "#pelicula", "#serie", "#streaming", "#análisis"]
            industry_score = sum(1 for tag in hashtags if tag.lower() in industry_hashtags)
            score += min(industry_score * 0.1, 0.2)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando SEO de hashtags: {e}")
            return 0.5
    
    def _analyze_visual_appeal(self, project: VideoProject) -> float:
        """Analiza el atractivo visual del contenido"""
        try:
            score = 0.0
            
            # Análisis de elementos visuales
            visual_elements = len(project.elements)
            if 5 <= visual_elements <= 15:  # Número óptimo
                score += 0.3
            elif 3 <= visual_elements <= 20:
                score += 0.2
            
            # Análisis de variedad de elementos
            element_types = set(element.type for element in project.elements)
            if len(element_types) >= 3:  # Variedad de tipos
                score += 0.2
            
            # Análisis de timing
            timing_score = self._analyze_visual_timing(project)
            score += timing_score * 0.3
            
            # Análisis de branding
            branding_score = self._analyze_branding_consistency(project)
            score += branding_score * 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando atractivo visual: {e}")
            return 0.5
    
    def _analyze_visual_timing(self, project: VideoProject) -> float:
        """Analiza el timing de elementos visuales"""
        try:
            if not project.elements:
                return 0.0
            
            # Análisis de distribución temporal
            durations = [element.end_time - element.start_time for element in project.elements]
            avg_duration = np.mean(durations)
            
            # Duración óptima: 3-8 segundos por elemento
            if 3 <= avg_duration <= 8:
                return 1.0
            elif 2 <= avg_duration <= 12:
                return 0.7
            else:
                return 0.4
                
        except Exception as e:
            logger.error(f"Error analizando timing visual: {e}")
            return 0.5
    
    def _analyze_branding_consistency(self, project: VideoProject) -> float:
        """Analiza la consistencia del branding"""
        try:
            score = 0.0
            
            # Verificar presencia de logo Cine Norte
            logo_elements = [elem for elem in project.elements if "logo" in elem.content.lower()]
            if logo_elements:
                score += 0.4
            
            # Verificar uso de colores de marca
            brand_colors = [BRANDING["colors"]["primary"], BRANDING["colors"]["accent"]]
            color_usage = 0
            for element in project.elements:
                if element.style and "color" in element.style:
                    if element.style["color"] in brand_colors:
                        color_usage += 1
            
            if color_usage > 0:
                score += min(color_usage * 0.1, 0.3)
            
            # Verificar consistencia en títulos
            title_elements = [elem for elem in project.elements if elem.type == "text"]
            if len(title_elements) > 0:
                score += 0.3
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analizando branding: {e}")
            return 0.5
    
    def _generate_recommendations(self, project: VideoProject, scores: Dict[str, float]) -> List[str]:
        """Genera recomendaciones de optimización"""
        try:
            recommendations = []
            
            # Recomendaciones basadas en scores
            if scores['engagement'] < 0.6:
                recommendations.append("Mejora el título con palabras de mayor impacto")
                recommendations.append("Añade más preguntas retóricas al guion")
            
            if scores['viral'] < 0.6:
                recommendations.append("Considera contenido más trending o controversial")
                recommendations.append("Incluye más referencias a géneros populares")
            
            if scores['seo'] < 0.6:
                recommendations.append("Optimiza el título para palabras clave")
                recommendations.append("Mejora la descripción con más keywords")
            
            if scores['visual'] < 0.6:
                recommendations.append("Añade más elementos visuales variados")
                recommendations.append("Mejora el timing de las transiciones")
            
            # Recomendaciones específicas del contenido
            if project.duration < 120:
                recommendations.append("Considera extender el video para mayor engagement")
            elif project.duration > 240:
                recommendations.append("Considera acortar el video para mantener atención")
            
            # Recomendaciones de hashtags
            if len(project.script.hashtags) < 5:
                recommendations.append("Añade más hashtags relevantes")
            elif len(project.script.hashtags) > 15:
                recommendations.append("Reduce el número de hashtags para mejor legibilidad")
            
            return recommendations[:5]  # Máximo 5 recomendaciones
            
        except Exception as e:
            logger.error(f"Error generando recomendaciones: {e}")
            return ["Revisa el contenido general para mejoras"]
    
    def _identify_strengths_weaknesses(self, project: VideoProject, scores: Dict[str, float]) -> Tuple[List[str], List[str]]:
        """Identifica fortalezas y debilidades del contenido"""
        try:
            strengths = []
            weaknesses = []
            
            # Análisis de fortalezas
            if scores['engagement'] >= 0.7:
                strengths.append("Alto potencial de engagement")
            if scores['viral'] >= 0.7:
                strengths.append("Fuerte potencial viral")
            if scores['seo'] >= 0.7:
                strengths.append("Excelente optimización SEO")
            if scores['visual'] >= 0.7:
                strengths.append("Atractivo visual destacado")
            
            # Análisis de debilidades
            if scores['engagement'] < 0.5:
                weaknesses.append("Bajo potencial de engagement")
            if scores['viral'] < 0.5:
                weaknesses.append("Limitado potencial viral")
            if scores['seo'] < 0.5:
                weaknesses.append("SEO necesita mejoras")
            if scores['visual'] < 0.5:
                weaknesses.append("Atractivo visual limitado")
            
            # Análisis específico del contenido
            if project.script.content.rating >= 7.0:
                strengths.append("Contenido de alta calidad")
            elif project.script.content.rating < 5.0:
                weaknesses.append("Contenido de baja calificación")
            
            if len(project.script.hashtags) >= 8:
                strengths.append("Buena estrategia de hashtags")
            elif len(project.script.hashtags) < 3:
                weaknesses.append("Estrategia de hashtags insuficiente")
            
            return strengths, weaknesses
            
        except Exception as e:
            logger.error(f"Error identificando fortalezas/debilidades: {e}")
            return ["Análisis en progreso"], ["Revisar contenido"]
    
    def generate_optimization_suggestions(self, project: VideoProject) -> List[OptimizationSuggestion]:
        """Genera sugerencias específicas de optimización"""
        try:
            suggestions = []
            
            # Sugerencias de título
            title_suggestions = self._generate_title_suggestions(project)
            suggestions.extend(title_suggestions)
            
            # Sugerencias de guion
            script_suggestions = self._generate_script_suggestions(project)
            suggestions.extend(script_suggestions)
            
            # Sugerencias de timing
            timing_suggestions = self._generate_timing_suggestions(project)
            suggestions.extend(timing_suggestions)
            
            # Sugerencias visuales
            visual_suggestions = self._generate_visual_suggestions(project)
            suggestions.extend(visual_suggestions)
            
            # Ordenar por prioridad e impacto
            suggestions.sort(key=lambda x: (x.priority == 'high', x.impact), reverse=True)
            
            return suggestions[:10]  # Top 10 sugerencias
            
        except Exception as e:
            logger.error(f"Error generando sugerencias: {e}")
            return []
    
    def _generate_title_suggestions(self, project: VideoProject) -> List[OptimizationSuggestion]:
        """Genera sugerencias para el título"""
        suggestions = []
        
        try:
            title = project.title
            
            # Sugerencia de palabras de impacto
            if not any(word in title.lower() for word in self.high_impact_words):
                suggestions.append(OptimizationSuggestion(
                    type="title",
                    priority="high",
                    description="Añade palabras de alto impacto al título",
                    impact=0.8,
                    implementation="Incluye palabras como 'increíble', 'espectacular', 'sorprendente'"
                ))
            
            # Sugerencia de longitud
            if len(title) < 50:
                suggestions.append(OptimizationSuggestion(
                    type="title",
                    priority="medium",
                    description="El título es muy corto para SEO",
                    impact=0.6,
                    implementation="Extiende el título a 50-60 caracteres"
                ))
            elif len(title) > 70:
                suggestions.append(OptimizationSuggestion(
                    type="title",
                    priority="medium",
                    description="El título es muy largo",
                    impact=0.5,
                    implementation="Acorta el título a 50-60 caracteres"
                ))
            
            # Sugerencia de keywords
            if not any(keyword in title.lower() for keyword in self.trending_keywords):
                suggestions.append(OptimizationSuggestion(
                    type="title",
                    priority="high",
                    description="Incluye palabras clave trending",
                    impact=0.7,
                    implementation="Añade keywords como 'streaming', 'análisis', 'reseña'"
                ))
            
        except Exception as e:
            logger.error(f"Error generando sugerencias de título: {e}")
        
        return suggestions
    
    def _generate_script_suggestions(self, project: VideoProject) -> List[OptimizationSuggestion]:
        """Genera sugerencias para el guion"""
        suggestions = []
        
        try:
            script = project.script
            
            # Sugerencia de longitud
            word_count = len(script.raw_text.split())
            if word_count < 200:
                suggestions.append(OptimizationSuggestion(
                    type="script",
                    priority="high",
                    description="El guion es muy corto",
                    impact=0.7,
                    implementation="Extiende el contenido a 200-500 palabras"
                ))
            elif word_count > 600:
                suggestions.append(OptimizationSuggestion(
                    type="script",
                    priority="medium",
                    description="El guion es muy largo",
                    impact=0.5,
                    implementation="Condensa el contenido a 200-500 palabras"
                ))
            
            # Sugerencia de preguntas retóricas
            question_count = script.raw_text.count('?')
            if question_count < 2:
                suggestions.append(OptimizationSuggestion(
                    type="script",
                    priority="medium",
                    description="Añade más preguntas retóricas",
                    impact=0.6,
                    implementation="Incluye 2-3 preguntas para aumentar engagement"
                ))
            
            # Sugerencia de palabras de impacto
            impact_word_count = sum(1 for word in self.high_impact_words 
                                  if word in script.raw_text.lower())
            if impact_word_count < 3:
                suggestions.append(OptimizationSuggestion(
                    type="script",
                    priority="medium",
                    description="Incluye más palabras de impacto",
                    impact=0.5,
                    implementation="Añade palabras como 'increíble', 'espectacular', 'sorprendente'"
                ))
            
        except Exception as e:
            logger.error(f"Error generando sugerencias de guion: {e}")
        
        return suggestions
    
    def _generate_timing_suggestions(self, project: VideoProject) -> List[OptimizationSuggestion]:
        """Genera sugerencias de timing"""
        suggestions = []
        
        try:
            # Sugerencia de duración total
            if project.duration < 120:
                suggestions.append(OptimizationSuggestion(
                    type="timing",
                    priority="high",
                    description="El video es muy corto",
                    impact=0.8,
                    implementation="Extiende a 2-3 minutos para mejor engagement"
                ))
            elif project.duration > 240:
                suggestions.append(OptimizationSuggestion(
                    type="timing",
                    priority="medium",
                    description="El video es muy largo",
                    impact=0.6,
                    implementation="Acorta a 2-3 minutos para mantener atención"
                ))
            
            # Sugerencia de segmentos
            if len(project.script.segments) < 3:
                suggestions.append(OptimizationSuggestion(
                    type="timing",
                    priority="medium",
                    description="Muy pocos segmentos",
                    impact=0.5,
                    implementation="Divide el contenido en 3-6 segmentos"
                ))
            elif len(project.script.segments) > 8:
                suggestions.append(OptimizationSuggestion(
                    type="timing",
                    priority="low",
                    description="Demasiados segmentos",
                    impact=0.3,
                    implementation="Consolida en 3-6 segmentos principales"
                ))
            
        except Exception as e:
            logger.error(f"Error generando sugerencias de timing: {e}")
        
        return suggestions
    
    def _generate_visual_suggestions(self, project: VideoProject) -> List[OptimizationSuggestion]:
        """Genera sugerencias visuales"""
        suggestions = []
        
        try:
            # Sugerencia de elementos visuales
            if len(project.elements) < 5:
                suggestions.append(OptimizationSuggestion(
                    type="visual",
                    priority="high",
                    description="Faltan elementos visuales",
                    impact=0.7,
                    implementation="Añade más elementos visuales variados"
                ))
            
            # Sugerencia de variedad
            element_types = set(element.type for element in project.elements)
            if len(element_types) < 2:
                suggestions.append(OptimizationSuggestion(
                    type="visual",
                    priority="medium",
                    description="Poca variedad en elementos visuales",
                    impact=0.5,
                    implementation="Incluye texto, imágenes y overlays"
                ))
            
            # Sugerencia de branding
            logo_elements = [elem for elem in project.elements if "logo" in elem.content.lower()]
            if not logo_elements:
                suggestions.append(OptimizationSuggestion(
                    type="visual",
                    priority="high",
                    description="Falta logo de Cine Norte",
                    impact=0.8,
                    implementation="Incluye el logo de Cine Norte en el video"
                ))
            
        except Exception as e:
            logger.error(f"Error generando sugerencias visuales: {e}")
        
        return suggestions
    
    def _create_fallback_analysis(self) -> ImpactAnalysis:
        """Crea análisis de respaldo en caso de error"""
        return ImpactAnalysis(
            engagement_score=0.5,
            viral_potential=0.5,
            seo_score=0.5,
            visual_appeal=0.5,
            overall_score=0.5,
            recommendations=["Revisa el contenido general"],
            strengths=["Análisis en progreso"],
            weaknesses=["Revisar implementación"]
        )
    
    def save_analysis_report(self, analysis: ImpactAnalysis, output_path: str) -> str:
        """Guarda el reporte de análisis en archivo"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "overall_score": analysis.overall_score,
                "scores": {
                    "engagement": analysis.engagement_score,
                    "viral_potential": analysis.viral_potential,
                    "seo": analysis.seo_score,
                    "visual_appeal": analysis.visual_appeal
                },
                "recommendations": analysis.recommendations,
                "strengths": analysis.strengths,
                "weaknesses": analysis.weaknesses
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte de análisis guardado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
            return ""
