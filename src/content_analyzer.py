"""
Módulo para análisis y selección de contenido de películas y series
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

from config import API_KEYS, STREAMING_PLATFORMS

logger = logging.getLogger(__name__)

@dataclass
class ContentItem:
    """Estructura para representar una película o serie"""
    title: str
    original_title: str
    release_date: str
    overview: str
    genres: List[str]
    platforms: List[str]
    rating: float
    popularity: float
    poster_url: str
    backdrop_url: str
    content_type: str  # 'movie' o 'tv'
    tmdb_id: int
    duration: Optional[int] = None
    seasons: Optional[int] = None
    episodes: Optional[int] = None

class ContentAnalyzer:
    """Analizador de contenido para seleccionar películas y series populares"""
    
    def __init__(self):
        self.tmdb_api_key = API_KEYS.get("tmdb")
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        
    def get_trending_content(self, content_type: str = "all", time_window: str = "week") -> List[ContentItem]:
        """
        Obtiene contenido trending de TMDB
        
        Args:
            content_type: 'movie', 'tv', o 'all'
            time_window: 'day' o 'week'
        """
        try:
            url = f"{self.base_url}/trending/{content_type}/{time_window}"
            params = {"api_key": self.tmdb_api_key, "language": "es-ES"}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            content_items = []
            
            for item in data.get("results", []):
                content_item = self._parse_tmdb_item(item)
                if content_item:
                    content_items.append(content_item)
                    
            return content_items
            
        except Exception as e:
            logger.error(f"Error obteniendo contenido trending: {e}")
            return []
    
    def get_popular_content(self, content_type: str = "movie", page: int = 1) -> List[ContentItem]:
        """
        Obtiene contenido popular de TMDB
        
        Args:
            content_type: 'movie' o 'tv'
            page: Número de página
        """
        try:
            url = f"{self.base_url}/{content_type}/popular"
            params = {
                "api_key": self.tmdb_api_key,
                "language": "es-ES",
                "page": page,
                "region": "ES"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            content_items = []
            
            for item in data.get("results", []):
                content_item = self._parse_tmdb_item(item)
                if content_item:
                    content_items.append(content_item)
                    
            return content_items
            
        except Exception as e:
            logger.error(f"Error obteniendo contenido popular: {e}")
            return []
    
    def get_recent_releases(self, content_type: str = "movie", days_back: int = 30) -> List[ContentItem]:
        """
        Obtiene estrenos recientes
        
        Args:
            content_type: 'movie' o 'tv'
            days_back: Días hacia atrás para buscar
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            url = f"{self.base_url}/discover/{content_type}"
            params = {
                "api_key": self.tmdb_api_key,
                "language": "es-ES",
                "sort_by": "popularity.desc",
                "primary_release_date.gte": start_date.strftime("%Y-%m-%d"),
                "primary_release_date.lte": end_date.strftime("%Y-%m-%d"),
                "region": "ES"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            content_items = []
            
            for item in data.get("results", []):
                content_item = self._parse_tmdb_item(item)
                if content_item:
                    content_items.append(content_item)
                    
            return content_items
            
        except Exception as e:
            logger.error(f"Error obteniendo estrenos recientes: {e}")
            return []
    
    def search_content(self, query: str, content_type: str = "movie") -> List[ContentItem]:
        """
        Busca contenido específico
        
        Args:
            query: Término de búsqueda
            content_type: 'movie' o 'tv'
        """
        try:
            url = f"{self.base_url}/search/{content_type}"
            params = {
                "api_key": self.tmdb_api_key,
                "language": "es-ES",
                "query": query,
                "region": "ES"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            content_items = []
            
            for item in data.get("results", []):
                content_item = self._parse_tmdb_item(item)
                if content_item:
                    content_items.append(content_item)
                    
            return content_items
            
        except Exception as e:
            logger.error(f"Error buscando contenido: {e}")
            return []
    
    def get_content_details(self, content_id: int, content_type: str = "movie") -> Optional[ContentItem]:
        """
        Obtiene detalles completos de un contenido específico
        
        Args:
            content_id: ID del contenido en TMDB
            content_type: 'movie' o 'tv'
        """
        try:
            url = f"{self.base_url}/{content_type}/{content_id}"
            params = {
                "api_key": self.tmdb_api_key,
                "language": "es-ES",
                "append_to_response": "videos,images,credits"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_tmdb_item(data, detailed=True)
            
        except Exception as e:
            logger.error(f"Error obteniendo detalles del contenido: {e}")
            return None
    
    def _parse_tmdb_item(self, item: Dict, detailed: bool = False) -> Optional[ContentItem]:
        """Parsea un item de TMDB a ContentItem"""
        try:
            # Determinar tipo de contenido
            content_type = "movie" if "title" in item else "tv"
            
            # Título
            title = item.get("title") or item.get("name", "")
            original_title = item.get("original_title") or item.get("original_name", "")
            
            # Fecha de lanzamiento
            if content_type == "movie":
                release_date = item.get("release_date", "")
            else:
                release_date = item.get("first_air_date", "")
            
            # Géneros
            genres = []
            if "genres" in item:
                genres = [genre["name"] for genre in item["genres"]]
            elif "genre_ids" in item:
                # Mapeo básico de IDs a nombres (simplificado)
                genre_map = {
                    28: "Acción", 12: "Aventura", 16: "Animación", 35: "Comedia",
                    80: "Crimen", 99: "Documental", 18: "Drama", 10751: "Familiar",
                    14: "Fantasía", 36: "Historia", 27: "Terror", 10402: "Música",
                    9648: "Misterio", 10749: "Romance", 878: "Ciencia ficción",
                    10770: "Película de TV", 53: "Suspense", 10752: "Guerra", 37: "Western"
                }
                genres = [genre_map.get(genre_id, "Otro") for genre_id in item["genre_ids"]]
            
            # URLs de imágenes
            poster_url = f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}" if item.get('poster_path') else ""
            backdrop_url = f"https://image.tmdb.org/t/p/w1280{item.get('backdrop_path', '')}" if item.get('backdrop_path') else ""
            
            # Duración (solo para películas)
            duration = None
            if content_type == "movie" and "runtime" in item:
                duration = item["runtime"]
            elif content_type == "tv" and detailed:
                duration = item.get("episode_run_time", [0])[0] if item.get("episode_run_time") else None
            
            # Temporadas y episodios (solo para series)
            seasons = None
            episodes = None
            if content_type == "tv":
                seasons = item.get("number_of_seasons")
                episodes = item.get("number_of_episodes")
            
            return ContentItem(
                title=title,
                original_title=original_title,
                release_date=release_date,
                overview=item.get("overview", ""),
                genres=genres,
                platforms=[],  # Se llenaría con datos de JustWatch o similar
                rating=item.get("vote_average", 0.0),
                popularity=item.get("popularity", 0.0),
                poster_url=poster_url,
                backdrop_url=backdrop_url,
                content_type=content_type,
                tmdb_id=item.get("id", 0),
                duration=duration,
                seasons=seasons,
                episodes=episodes
            )
            
        except Exception as e:
            logger.error(f"Error parseando item de TMDB: {e}")
            return None
    
    def filter_by_criteria(self, content_list: List[ContentItem], 
                          min_rating: float = 6.0,
                          min_popularity: float = 10.0,
                          genres: List[str] = None) -> List[ContentItem]:
        """
        Filtra contenido según criterios específicos
        
        Args:
            content_list: Lista de contenido a filtrar
            min_rating: Rating mínimo
            min_popularity: Popularidad mínima
            genres: Géneros deseados (opcional)
        """
        filtered = []
        
        for item in content_list:
            # Filtros básicos
            if item.rating < min_rating or item.popularity < min_popularity:
                continue
            
            # Filtro de géneros
            if genres and not any(genre in item.genres for genre in genres):
                continue
            
            filtered.append(item)
        
        return filtered
    
    def get_recommended_content(self, limit: int = 10) -> List[ContentItem]:
        """
        Obtiene contenido recomendado combinando diferentes fuentes
        
        Args:
            limit: Número máximo de elementos a retornar
        """
        all_content = []
        
        # Obtener contenido trending
        trending = self.get_trending_content("all", "week")
        all_content.extend(trending[:5])
        
        # Obtener estrenos recientes
        recent_movies = self.get_recent_releases("movie", 30)
        all_content.extend(recent_movies[:3])
        
        recent_series = self.get_recent_releases("tv", 30)
        all_content.extend(recent_series[:2])
        
        # Filtrar y ordenar
        filtered = self.filter_by_criteria(all_content)
        filtered.sort(key=lambda x: x.popularity, reverse=True)
        
        return filtered[:limit]
