"""
Módulo de análisis de contenido para Cine Norte
Conecta con APIs de streaming y analiza películas/series populares
"""
import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import aiohttp
from config import config

@dataclass
class ContentInfo:
    """Información de contenido multimedia"""
    title: str
    original_title: str
    overview: str
    release_date: str
    genre: List[str]
    rating: float
    popularity: float
    poster_url: str
    backdrop_url: str
    trailer_url: Optional[str]
    platform: str
    content_type: str  # 'movie' o 'tv'
    duration: Optional[int]  # en minutos
    cast: List[str]
    director: List[str]
    keywords: List[str]
    language: str
    country: str

class ContentAnalyzer:
    """Analizador de contenido de streaming"""
    
    def __init__(self):
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        self.omdb_base_url = "http://www.omdbapi.com"
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def get_trending_content(self, time_window: str = "week", content_type: str = "all") -> List[ContentInfo]:
        """
        Obtiene contenido trending de TMDB
        
        Args:
            time_window: 'day' o 'week'
            content_type: 'all', 'movie', 'tv'
        """
        try:
            url = f"{self.tmdb_base_url}/trending/{content_type}/{time_window}"
            params = {
                "api_key": config.TMDB_API_KEY,
                "language": "es-ES",
                "region": "MX"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            content_list = []
            for item in data.get("results", []):
                content_info = self._parse_tmdb_content(item, content_type)
                if content_info:
                    content_list.append(content_info)
            
            return content_list
            
        except Exception as e:
            self.logger.error(f"Error obteniendo contenido trending: {e}")
            return []
    
    def search_content(self, query: str, content_type: str = "all") -> List[ContentInfo]:
        """
        Busca contenido específico
        
        Args:
            query: Término de búsqueda
            content_type: 'all', 'movie', 'tv'
        """
        try:
            if content_type == "all":
                movie_results = self._search_movies(query)
                tv_results = self._search_tv_shows(query)
                return movie_results + tv_results
            elif content_type == "movie":
                return self._search_movies(query)
            elif content_type == "tv":
                return self._search_tv_shows(query)
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error buscando contenido: {e}")
            return []
    
    def _search_movies(self, query: str) -> List[ContentInfo]:
        """Busca películas específicas"""
        url = f"{self.tmdb_base_url}/search/movie"
        params = {
            "api_key": config.TMDB_API_KEY,
            "query": query,
            "language": "es-ES",
            "region": "MX"
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        content_list = []
        for item in data.get("results", []):
            content_info = self._parse_tmdb_content(item, "movie")
            if content_info:
                content_list.append(content_info)
        
        return content_list
    
    def _search_tv_shows(self, query: str) -> List[ContentInfo]:
        """Busca series de TV específicas"""
        url = f"{self.tmdb_base_url}/search/tv"
        params = {
            "api_key": config.TMDB_API_KEY,
            "query": query,
            "language": "es-ES",
            "region": "MX"
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        content_list = []
        for item in data.get("results", []):
            content_info = self._parse_tmdb_content(item, "tv")
            if content_info:
                content_list.append(content_info)
        
        return content_list
    
    def _parse_tmdb_content(self, item: Dict, content_type: str) -> Optional[ContentInfo]:
        """Convierte datos de TMDB a ContentInfo"""
        try:
            # Obtener detalles adicionales
            details = self._get_content_details(item["id"], content_type)
            
            return ContentInfo(
                title=item.get("title") or item.get("name", ""),
                original_title=item.get("original_title") or item.get("original_name", ""),
                overview=item.get("overview", ""),
                release_date=item.get("release_date") or item.get("first_air_date", ""),
                genre=self._get_genre_names(item.get("genre_ids", [])),
                rating=item.get("vote_average", 0.0),
                popularity=item.get("popularity", 0.0),
                poster_url=f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}" if item.get('poster_path') else "",
                backdrop_url=f"https://image.tmdb.org/t/p/w1280{item.get('backdrop_path', '')}" if item.get('backdrop_path') else "",
                trailer_url=self._get_trailer_url(item["id"], content_type),
                platform=self._detect_platform(item),
                content_type=content_type,
                duration=details.get("runtime") if content_type == "movie" else None,
                cast=details.get("cast", [])[:5],  # Top 5 actores
                director=details.get("director", []),
                keywords=details.get("keywords", [])[:10],  # Top 10 keywords
                language=item.get("original_language", "es"),
                country=details.get("production_countries", [""])[0] if details.get("production_countries") else ""
            )
            
        except Exception as e:
            self.logger.error(f"Error parseando contenido TMDB: {e}")
            return None
    
    def _get_content_details(self, content_id: int, content_type: str) -> Dict:
        """Obtiene detalles adicionales del contenido"""
        try:
            url = f"{self.tmdb_base_url}/{content_type}/{content_id}"
            params = {
                "api_key": config.TMDB_API_KEY,
                "language": "es-ES",
                "append_to_response": "credits,keywords,videos"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Procesar cast
            cast = []
            if "credits" in data and "cast" in data["credits"]:
                cast = [actor["name"] for actor in data["credits"]["cast"][:10]]
            
            # Procesar director
            director = []
            if "credits" in data and "crew" in data["credits"]:
                director = [crew["name"] for crew in data["credits"]["crew"] 
                           if crew["job"] == "Director"]
            
            # Procesar keywords
            keywords = []
            if "keywords" in data and "keywords" in data["keywords"]:
                keywords = [kw["name"] for kw in data["keywords"]["keywords"][:10]]
            
            return {
                "runtime": data.get("runtime"),
                "cast": cast,
                "director": director,
                "keywords": keywords,
                "production_countries": [country["name"] for country in data.get("production_countries", [])]
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo detalles del contenido: {e}")
            return {}
    
    def _get_trailer_url(self, content_id: int, content_type: str) -> Optional[str]:
        """Obtiene URL del tráiler"""
        try:
            url = f"{self.tmdb_base_url}/{content_type}/{content_id}/videos"
            params = {
                "api_key": config.TMDB_API_KEY,
                "language": "es-ES"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Buscar tráiler en español o inglés
            for video in data.get("results", []):
                if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                    return f"https://www.youtube.com/watch?v={video['key']}"
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo tráiler: {e}")
            return None
    
    def _get_genre_names(self, genre_ids: List[int]) -> List[str]:
        """Convierte IDs de género a nombres"""
        genre_map = {
            28: "Acción", 12: "Aventura", 16: "Animación", 35: "Comedia",
            80: "Crimen", 99: "Documental", 18: "Drama", 10751: "Familia",
            14: "Fantasía", 36: "Historia", 27: "Terror", 10402: "Música",
            9648: "Misterio", 10749: "Romance", 878: "Ciencia Ficción",
            10770: "Película de TV", 53: "Suspenso", 10752: "Guerra", 37: "Western"
        }
        
        return [genre_map.get(genre_id, "Desconocido") for genre_id in genre_ids]
    
    def _detect_platform(self, item: Dict) -> str:
        """Detecta la plataforma de streaming (simplificado)"""
        # Esta es una implementación básica
        # En producción, se necesitaría una API más específica
        title = (item.get("title") or item.get("name", "")).lower()
        
        if any(word in title for word in ["netflix", "stranger things", "the crown"]):
            return "Netflix"
        elif any(word in title for word in ["amazon", "prime", "the boys"]):
            return "Amazon Prime"
        elif any(word in title for word in ["disney", "marvel", "star wars"]):
            return "Disney+"
        elif any(word in title for word in ["hbo", "max", "game of thrones"]):
            return "HBO Max"
        else:
            return "Múltiples plataformas"
    
    def get_content_for_analysis(self, limit: int = 10) -> List[ContentInfo]:
        """
        Obtiene contenido optimizado para análisis
        
        Args:
            limit: Número máximo de contenidos a retornar
        """
        # Combinar contenido trending de películas y series
        movies = self.get_trending_content("week", "movie")[:limit//2]
        tv_shows = self.get_trending_content("week", "tv")[:limit//2]
        
        all_content = movies + tv_shows
        
        # Ordenar por popularidad y rating
        all_content.sort(key=lambda x: (x.popularity * x.rating), reverse=True)
        
        return all_content[:limit]
    
    def analyze_content_viability(self, content: ContentInfo) -> Dict:
        """
        Analiza la viabilidad del contenido para crear videos
        
        Returns:
            Dict con score de viabilidad y recomendaciones
        """
        score = 0
        factors = {}
        
        # Factor de popularidad (0-30 puntos)
        popularity_score = min(content.popularity / 100, 1) * 30
        score += popularity_score
        factors["popularity"] = popularity_score
        
        # Factor de rating (0-25 puntos)
        rating_score = (content.rating / 10) * 25
        score += rating_score
        factors["rating"] = rating_score
        
        # Factor de disponibilidad de tráiler (0-20 puntos)
        trailer_score = 20 if content.trailer_url else 0
        score += trailer_score
        factors["trailer_available"] = trailer_score
        
        # Factor de calidad de descripción (0-15 puntos)
        overview_score = min(len(content.overview) / 200, 1) * 15
        score += overview_score
        factors["overview_quality"] = overview_score
        
        # Factor de género (0-10 puntos)
        high_impact_genres = ["Acción", "Ciencia Ficción", "Terror", "Suspenso", "Aventura"]
        genre_score = 10 if any(genre in high_impact_genres for genre in content.genre) else 5
        score += genre_score
        factors["genre_impact"] = genre_score
        
        # Clasificación final
        if score >= 80:
            viability = "Excelente"
        elif score >= 60:
            viability = "Buena"
        elif score >= 40:
            viability = "Regular"
        else:
            viability = "Baja"
        
        return {
            "total_score": round(score, 2),
            "viability": viability,
            "factors": factors,
            "recommendations": self._get_recommendations(score, content)
        }
    
    def _get_recommendations(self, score: float, content: ContentInfo) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        if score < 40:
            recommendations.append("Considera buscar contenido más popular o reciente")
        
        if not content.trailer_url:
            recommendations.append("Busca tráileres alternativos o clips oficiales")
        
        if len(content.overview) < 100:
            recommendations.append("Investiga más detalles de la trama")
        
        if not any(genre in ["Acción", "Ciencia Ficción", "Terror", "Suspenso"] for genre in content.genre):
            recommendations.append("Enfócate en aspectos emocionales o dramáticos")
        
        return recommendations

# Instancia global del analizador
content_analyzer = ContentAnalyzer()
