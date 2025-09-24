"""
Aplicación principal de Cine Norte
Interfaz de usuario para generar contenido audiovisual automatizado
"""
import streamlit as st
import os
import logging
from typing import Dict, List, Optional
import tempfile
from datetime import datetime
import json

# Importar módulos del sistema
from config import config
from content_analyzer import content_analyzer, ContentInfo
from script_generator import script_generator, GeneratedScript
from voice_synthesizer import voice_synthesizer, SubtitleCue
from video_editor import video_editor
from format_generator import format_generator, GeneratedFormat
from ai_optimizer import ai_optimizer, OptimizationAnalysis
from thumbnail_generator import thumbnail_generator, GeneratedThumbnail

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar página de Streamlit
st.set_page_config(
    page_title="Cine Norte - Generador de Contenido",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para Cine Norte
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #E50914, #C0C0C0);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    .metric-card {
        background: #0A0A0A;
        color: #C0C0C0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #E50914;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background: #1a4d1a;
        color: #90EE90;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4CAF50;
    }
    
    .warning-message {
        background: #4d3a1a;
        color: #FFD700;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #FFA500;
    }
    
    .error-message {
        background: #4d1a1a;
        color: #FFB6C1;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #FF6B6B;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #E50914, #8B0000);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #8B0000, #E50914);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🎬 CINE NORTE</h1>
        <p>Generador Automatizado de Contenido Audiovisual</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Configuración de APIs
        st.subheader("🔑 APIs")
        openai_key = st.text_input("OpenAI API Key", type="password", help="Clave para generación de guiones")
        tmdb_key = st.text_input("TMDB API Key", type="password", help="Clave para análisis de contenido")
        
        # Configuración de video
        st.subheader("🎥 Video")
        target_platform = st.selectbox(
            "Plataforma Principal",
            ["youtube", "tiktok", "instagram", "facebook", "twitter"],
            help="Plataforma objetivo para el video principal"
        )
        
        video_style = st.selectbox(
            "Estilo Visual",
            ["cinematic", "dynamic", "dramatic"],
            help="Estilo visual del video"
        )
        
        # Configuración de voz
        st.subheader("🎤 Voz")
        voice_profile = st.selectbox(
            "Perfil de Voz",
            ["cinenorte_male", "cinenorte_female", "dramatic", "energetic"],
            help="Perfil de voz para la narración"
        )
        
        # Configuración de duración
        st.subheader("⏱️ Duración")
        max_duration = st.slider(
            "Duración Máxima (segundos)",
            min_value=30,
            max_value=300,
            value=120,
            help="Duración máxima del video en segundos"
        )
    
    # Pestañas principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Análisis de Contenido", 
        "📝 Generación de Guion", 
        "🎬 Creación de Video", 
        "📊 Optimización IA", 
        "📁 Descargas"
    ])
    
    with tab1:
        content_analysis_tab()
    
    with tab2:
        script_generation_tab()
    
    with tab3:
        video_creation_tab()
    
    with tab4:
        optimization_tab()
    
    with tab5:
        downloads_tab()

def content_analysis_tab():
    """Pestaña de análisis de contenido"""
    st.header("🔍 Análisis de Contenido")
    
    # Búsqueda de contenido
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input(
            "Buscar Película o Serie",
            placeholder="Ej: Stranger Things, The Crown, La Casa de Papel...",
            help="Busca contenido en las principales plataformas de streaming"
        )
    
    with col2:
        content_type = st.selectbox("Tipo", ["all", "movie", "tv"])
    
    if st.button("🔍 Buscar Contenido", type="primary"):
        if search_query:
            with st.spinner("Buscando contenido..."):
                try:
                    # Buscar contenido
                    content_results = content_analyzer.search_content(search_query, content_type)
                    
                    if content_results:
                        st.success(f"Encontrados {len(content_results)} resultados")
                        
                        # Mostrar resultados
                        for i, content in enumerate(content_results[:5]):  # Mostrar top 5
                            with st.expander(f"🎬 {content.title} ({content.content_type.upper()})"):
                                col1, col2 = st.columns([1, 2])
                                
                                with col1:
                                    if content.poster_url:
                                        st.image(content.poster_url, width=200)
                                
                                with col2:
                                    st.write(f"**Plataforma:** {content.platform}")
                                    st.write(f"**Género:** {', '.join(content.genre)}")
                                    st.write(f"**Rating:** {content.rating}/10")
                                    st.write(f"**Popularidad:** {content.popularity:.1f}")
                                    st.write(f"**Fecha:** {content.release_date}")
                                    st.write(f"**Idioma:** {content.language}")
                                    
                                    if content.overview:
                                        st.write(f"**Sinopsis:** {content.overview[:200]}...")
                                    
                                    # Botón para seleccionar
                                    if st.button(f"Seleccionar {content.title}", key=f"select_{i}"):
                                        st.session_state.selected_content = content
                                        st.success(f"Contenido seleccionado: {content.title}")
                    else:
                        st.warning("No se encontraron resultados. Intenta con otros términos.")
                        
                except Exception as e:
                    st.error(f"Error buscando contenido: {e}")
        else:
            st.warning("Por favor ingresa un término de búsqueda")
    
    # Mostrar contenido trending
    st.subheader("🔥 Contenido Trending")
    
    if st.button("Obtener Contenido Popular"):
        with st.spinner("Obteniendo contenido trending..."):
            try:
                trending_content = content_analyzer.get_content_for_analysis(limit=10)
                
                if trending_content:
                    st.success(f"Obtenidos {len(trending_content)} contenidos trending")
                    
                    # Mostrar en grid
                    cols = st.columns(3)
                    for i, content in enumerate(trending_content):
                        with cols[i % 3]:
                            with st.container():
                                st.markdown(f"**{content.title}**")
                                st.write(f"⭐ {content.rating}/10")
                                st.write(f"📺 {content.platform}")
                                st.write(f"🎭 {', '.join(content.genre[:2])}")
                                
                                if st.button(f"Seleccionar", key=f"trending_{i}"):
                                    st.session_state.selected_content = content
                                    st.success(f"Seleccionado: {content.title}")
                else:
                    st.warning("No se pudo obtener contenido trending")
                    
            except Exception as e:
                st.error(f"Error obteniendo contenido trending: {e}")
    
    # Mostrar contenido seleccionado
    if hasattr(st.session_state, 'selected_content'):
        st.subheader("✅ Contenido Seleccionado")
        content = st.session_state.selected_content
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if content.poster_url:
                st.image(content.poster_url, width=300)
        
        with col2:
            st.markdown(f"### {content.title}")
            st.write(f"**Tipo:** {content.content_type.upper()}")
            st.write(f"**Plataforma:** {content.platform}")
            st.write(f"**Géneros:** {', '.join(content.genre)}")
            st.write(f"**Rating:** {content.rating}/10")
            st.write(f"**Popularidad:** {content.popularity:.1f}")
            st.write(f"**Fecha de estreno:** {content.release_date}")
            st.write(f"**Idioma:** {content.language}")
            st.write(f"**País:** {content.country}")
            
            if content.overview:
                st.write(f"**Sinopsis:** {content.overview}")
            
            if content.cast:
                st.write(f"**Reparto:** {', '.join(content.cast[:3])}")
            
            if content.director:
                st.write(f"**Director:** {', '.join(content.director)}")
            
            # Análisis de viabilidad
            st.subheader("📊 Análisis de Viabilidad")
            viability = content_analyzer.analyze_content_viability(content)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score General", f"{viability['total_score']:.1f}/100")
            with col2:
                st.metric("Viabilidad", viability['viability'])
            with col3:
                st.metric("Factores", len(viability['factors']))
            
            # Mostrar factores
            st.write("**Factores de análisis:**")
            for factor, score in viability['factors'].items():
                st.progress(score / 100, text=f"{factor}: {score:.1f}")
            
            # Mostrar recomendaciones
            if viability['recommendations']:
                st.write("**Recomendaciones:**")
                for rec in viability['recommendations']:
                    st.write(f"• {rec}")

def script_generation_tab():
    """Pestaña de generación de guion"""
    st.header("📝 Generación de Guion")
    
    if not hasattr(st.session_state, 'selected_content'):
        st.warning("⚠️ Primero selecciona un contenido en la pestaña 'Análisis de Contenido'")
        return
    
    content = st.session_state.selected_content
    
    # Configuración del guion
    col1, col2 = st.columns(2)
    
    with col1:
        target_platform = st.selectbox(
            "Plataforma Objetivo",
            ["youtube", "tiktok", "instagram", "facebook", "twitter"],
            key="script_platform"
        )
        
        script_style = st.selectbox(
            "Estilo del Guion",
            ["dynamic", "dramatic", "comedic", "analytical"],
            key="script_style"
        )
    
    with col2:
        duration_target = st.slider(
            "Duración Objetivo (segundos)",
            min_value=30,
            max_value=300,
            value=120,
            key="script_duration"
        )
        
        include_spoilers = st.checkbox(
            "Incluir Spoilers Menores",
            value=False,
            help="Incluye spoilers menores para mayor impacto"
        )
    
    # Generar guion
    if st.button("🎬 Generar Guion", type="primary"):
        with st.spinner("Generando guion con IA..."):
            try:
                # Generar guion
                script = script_generator.generate_script(
                    content=content,
                    target_platform=target_platform,
                    duration_target=duration_target,
                    style=script_style
                )
                
                # Guardar en sesión
                st.session_state.generated_script = script
                
                st.success("✅ Guion generado exitosamente!")
                
                # Mostrar resumen
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Duración", f"{script.total_duration}s")
                with col2:
                    st.metric("Palabras", script.word_count)
                with col3:
                    st.metric("Secciones", len(script.sections))
                with col4:
                    st.metric("Plataforma", script.target_platform.upper())
                
            except Exception as e:
                st.error(f"Error generando guion: {e}")
    
    # Mostrar guion generado
    if hasattr(st.session_state, 'generated_script'):
        script = st.session_state.generated_script
        
        st.subheader("📖 Guion Generado")
        
        # Tabs para diferentes vistas
        tab1, tab2, tab3 = st.tabs(["📝 Texto Completo", "🎭 Por Secciones", "📊 Metadatos"])
        
        with tab1:
            st.text_area("Guion Completo", script.raw_text, height=400)
            
            # Botón para descargar
            if st.button("💾 Descargar Guion (.txt)"):
                filename = script_generator.export_script_to_txt(script)
                st.success(f"Guion guardado como: {filename}")
        
        with tab2:
            for i, section in enumerate(script.sections, 1):
                with st.expander(f"Sección {i}: {section.type.upper()}"):
                    st.write(f"**Duración:** {section.duration_seconds}s")
                    st.write(f"**Emoción:** {section.emotion}")
                    st.write(f"**Contenido:**")
                    st.write(section.content)
                    
                    if section.visual_cues:
                        st.write(f"**Indicaciones visuales:** {', '.join(section.visual_cues)}")
                    
                    if section.emphasis_words:
                        st.write(f"**Palabras de énfasis:** {', '.join(section.emphasis_words)}")
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Títulos Sugeridos:**")
                for title in script.title_suggestions:
                    st.write(f"• {title}")
                
                st.write("**Hashtags:**")
                hashtag_text = " ".join(script.hashtags)
                st.code(hashtag_text)
            
            with col2:
                st.write("**Configuración:**")
                st.write(f"• Estilo Visual: {script.visual_style}")
                st.write(f"• Música Sugerida: {script.music_suggestion}")
                st.write(f"• Plataforma: {script.target_platform}")
                st.write(f"• Duración Total: {script.total_duration}s")

def video_creation_tab():
    """Pestaña de creación de video"""
    st.header("🎬 Creación de Video")
    
    if not hasattr(st.session_state, 'generated_script'):
        st.warning("⚠️ Primero genera un guion en la pestaña 'Generación de Guion'")
        return
    
    script = st.session_state.generated_script
    
    # Configuración del video
    col1, col2 = st.columns(2)
    
    with col1:
        video_style = st.selectbox(
            "Estilo Visual",
            ["cinematic", "dynamic", "dramatic"],
            key="video_style"
        )
        
        voice_profile = st.selectbox(
            "Perfil de Voz",
            ["cinenorte_male", "cinenorte_female", "dramatic", "energetic"],
            key="voice_profile"
        )
    
    with col2:
        include_subtitles = st.checkbox("Incluir Subtítulos", value=True)
        include_music = st.checkbox("Incluir Música de Fondo", value=True)
        
        quality = st.selectbox(
            "Calidad de Video",
            ["720p", "1080p", "4K"],
            index=1
        )
    
    # Generar audio y video
    if st.button("🎥 Generar Video", type="primary"):
        with st.spinner("Generando audio y video..."):
            try:
                # Generar audio
                st.write("🎤 Generando audio...")
                audio_path, subtitles = voice_synthesizer.synthesize_script(
                    script=script,
                    voice_profile=voice_profile,
                    output_format="mp3"
                )
                
                if audio_path:
                    st.success("✅ Audio generado exitosamente!")
                    
                    # Generar video
                    st.write("🎬 Generando video...")
                    video_path = video_editor.create_video(
                        script=script,
                        audio_path=audio_path,
                        subtitles=subtitles,
                        format_type=script.target_platform,
                        style=video_style
                    )
                    
                    if video_path:
                        st.success("✅ Video generado exitosamente!")
                        
                        # Guardar en sesión
                        st.session_state.generated_video = video_path
                        st.session_state.generated_audio = audio_path
                        st.session_state.generated_subtitles = subtitles
                        
                        # Mostrar video
                        st.video(video_path)
                        
                        # Mostrar información
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Duración", f"{script.total_duration}s")
                        with col2:
                            st.metric("Formato", script.target_platform.upper())
                        with col3:
                            st.metric("Calidad", quality)
                    else:
                        st.error("Error generando video")
                else:
                    st.error("Error generando audio")
                    
            except Exception as e:
                st.error(f"Error en la generación: {e}")
    
    # Generar formatos múltiples
    if hasattr(st.session_state, 'generated_video'):
        st.subheader("📱 Formatos Múltiples")
        
        if st.button("🔄 Generar Todos los Formatos"):
            with st.spinner("Generando formatos para todas las plataformas..."):
                try:
                    content_info = {
                        "title": script.title,
                        "platform": script.content.platform,
                        "content_type": script.content.content_type
                    }
                    
                    generated_formats = format_generator.generate_all_formats(
                        source_video_path=st.session_state.generated_video,
                        script_title=script.title,
                        content_info=content_info
                    )
                    
                    if generated_formats:
                        st.success(f"✅ Generados {len(generated_formats)} formatos!")
                        st.session_state.generated_formats = generated_formats
                        
                        # Mostrar formatos generados
                        for fmt in generated_formats:
                            with st.expander(f"📱 {fmt.format_type.upper()}"):
                                col1, col2 = st.columns([1, 2])
                                
                                with col1:
                                    if fmt.thumbnail_path:
                                        st.image(fmt.thumbnail_path, width=200)
                                
                                with col2:
                                    st.write(f"**Plataforma:** {fmt.metadata['platform']}")
                                    st.write(f"**Dimensiones:** {fmt.metadata['dimensions']}")
                                    st.write(f"**Aspecto:** {fmt.metadata['aspect_ratio']}")
                                    st.write(f"**Score:** {fmt.optimization_score:.1f}/100")
                                    
                                    if st.button(f"Ver Video", key=f"view_{fmt.format_type}"):
                                        st.video(fmt.video_path)
                    else:
                        st.warning("No se pudieron generar formatos")
                        
                except Exception as e:
                    st.error(f"Error generando formatos: {e}")

def optimization_tab():
    """Pestaña de optimización con IA"""
    st.header("📊 Optimización con IA")
    
    if not hasattr(st.session_state, 'generated_script'):
        st.warning("⚠️ Primero genera un guion en la pestaña 'Generación de Guion'")
        return
    
    script = st.session_state.generated_script
    
    # Análisis de optimización
    if st.button("🔍 Analizar con IA", type="primary"):
        with st.spinner("Analizando contenido con IA..."):
            try:
                video_path = st.session_state.get('generated_video')
                
                analysis = ai_optimizer.optimize_content(
                    script=script,
                    content_info=script.content,
                    video_path=video_path
                )
                
                st.session_state.optimization_analysis = analysis
                st.success("✅ Análisis completado!")
                
            except Exception as e:
                st.error(f"Error en el análisis: {e}")
    
    # Mostrar análisis
    if hasattr(st.session_state, 'optimization_analysis'):
        analysis = st.session_state.optimization_analysis
        
        st.subheader("📈 Resultados del Análisis")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Score General",
                f"{analysis.overall_score:.1f}/100",
                delta=f"{analysis.overall_score - 50:.1f}"
            )
        
        with col2:
            st.metric(
                "Engagement",
                f"{analysis.engagement_potential:.1f}/100"
            )
        
        with col3:
            st.metric(
                "Viralidad",
                f"{analysis.viral_probability:.1f}/100"
            )
        
        with col4:
            st.metric(
                "SEO",
                f"{analysis.seo_score:.1f}/100"
            )
        
        # Gráficos de análisis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Análisis Detallado")
            
            metrics = {
                "Calidad de Contenido": analysis.content_score,
                "Potencial de Engagement": analysis.engagement_potential,
                "Probabilidad Viral": analysis.viral_probability,
                "Optimización SEO": analysis.seo_score,
                "Impacto Visual": analysis.visual_impact,
                "Calidad de Audio": analysis.audio_quality
            }
            
            for metric, score in metrics.items():
                st.progress(score / 100, text=f"{metric}: {score:.1f}/100")
        
        with col2:
            st.subheader("🎯 Recomendaciones")
            
            if analysis.recommendations:
                for i, rec in enumerate(analysis.recommendations, 1):
                    st.write(f"{i}. {rec}")
            else:
                st.write("No hay recomendaciones específicas")
        
        # Mejoras sugeridas
        if analysis.improvements:
            st.subheader("🔧 Mejoras Sugeridas")
            for i, improvement in enumerate(analysis.improvements, 1):
                st.write(f"{i}. {improvement}")
        
        # Análisis de tendencias
        st.subheader("📈 Análisis de Tendencias")
        
        # Simular análisis de tendencias
        trending_keywords = ["netflix", "streaming", "película", "serie", "estreno"]
        st.write("**Keywords Trending:**")
        for keyword in trending_keywords:
            st.write(f"• #{keyword}")
        
        # Análisis de competencia
        st.write("**Análisis de Competencia:**")
        st.write("• Contenido similar: 15 videos")
        st.write("• Engagement promedio: 75%")
        st.write("• Oportunidad: Alta")

def downloads_tab():
    """Pestaña de descargas"""
    st.header("📁 Descargas")
    
    if not hasattr(st.session_state, 'generated_script'):
        st.warning("⚠️ No hay contenido generado para descargar")
        return
    
    script = st.session_state.generated_script
    
    # Archivos disponibles
    st.subheader("📄 Archivos Generados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📝 Guion**")
        if st.button("💾 Descargar Guion (.txt)"):
            filename = script_generator.export_script_to_txt(script)
            st.success(f"Guion guardado: {filename}")
        
        st.write("**🎤 Audio**")
        if hasattr(st.session_state, 'generated_audio'):
            audio_path = st.session_state.generated_audio
            if os.path.exists(audio_path):
                with open(audio_path, "rb") as file:
                    st.download_button(
                        label="💾 Descargar Audio (.mp3)",
                        data=file.read(),
                        file_name=f"audio_{script.title.replace(' ', '_')}.mp3",
                        mime="audio/mpeg"
                    )
        
        st.write("**📝 Subtítulos**")
        if hasattr(st.session_state, 'generated_subtitles'):
            subtitles = st.session_state.generated_subtitles
            if subtitles:
                # Exportar subtítulos
                vtt_filename = voice_synthesizer.export_subtitles(subtitles)
                srt_filename = voice_synthesizer.export_subtitles_srt(subtitles)
                
                with open(vtt_filename, "rb") as file:
                    st.download_button(
                        label="💾 Descargar Subtítulos (.vtt)",
                        data=file.read(),
                        file_name=f"subtitulos_{script.title.replace(' ', '_')}.vtt",
                        mime="text/vtt"
                    )
                
                with open(srt_filename, "rb") as file:
                    st.download_button(
                        label="💾 Descargar Subtítulos (.srt)",
                        data=file.read(),
                        file_name=f"subtitulos_{script.title.replace(' ', '_')}.srt",
                        mime="text/plain"
                    )
    
    with col2:
        st.write("**🎬 Videos**")
        if hasattr(st.session_state, 'generated_video'):
            video_path = st.session_state.generated_video
            if os.path.exists(video_path):
                with open(video_path, "rb") as file:
                    st.download_button(
                        label="💾 Descargar Video Principal",
                        data=file.read(),
                        file_name=f"video_{script.title.replace(' ', '_')}.mp4",
                        mime="video/mp4"
                    )
        
        # Formatos múltiples
        if hasattr(st.session_state, 'generated_formats'):
            st.write("**📱 Formatos Múltiples**")
            for fmt in st.session_state.generated_formats:
                if os.path.exists(fmt.video_path):
                    with open(fmt.video_path, "rb") as file:
                        st.download_button(
                            label=f"💾 {fmt.format_type.upper()}",
                            data=file.read(),
                            file_name=f"{script.title.replace(' ', '_')}_{fmt.format_type}.mp4",
                            mime="video/mp4"
                        )
        
        # Miniaturas
        if hasattr(st.session_state, 'generated_formats'):
            st.write("**🖼️ Miniaturas**")
            for fmt in st.session_state.generated_formats:
                if fmt.thumbnail_path and os.path.exists(fmt.thumbnail_path):
                    with open(fmt.thumbnail_path, "rb") as file:
                        st.download_button(
                            label=f"🖼️ {fmt.format_type.upper()}",
                            data=file.read(),
                            file_name=f"thumbnail_{script.title.replace(' ', '_')}_{fmt.format_type}.jpg",
                            mime="image/jpeg"
                        )
    
    # Resumen de generación
    st.subheader("📊 Resumen de Generación")
    
    if hasattr(st.session_state, 'generated_script'):
        script = st.session_state.generated_script
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Duración Total", f"{script.total_duration}s")
            st.metric("Palabras", script.word_count)
            st.metric("Secciones", len(script.sections))
        
        with col2:
            st.metric("Plataforma", script.target_platform.upper())
            st.metric("Estilo", script.visual_style)
            st.metric("Música", script.music_suggestion)
        
        with col3:
            if hasattr(st.session_state, 'optimization_analysis'):
                analysis = st.session_state.optimization_analysis
                st.metric("Score General", f"{analysis.overall_score:.1f}/100")
                st.metric("Engagement", f"{analysis.engagement_potential:.1f}/100")
                st.metric("Viralidad", f"{analysis.viral_probability:.1f}/100")
    
    # Limpiar archivos temporales
    if st.button("🗑️ Limpiar Archivos Temporales"):
        try:
            # Limpiar archivos de cada módulo
            voice_synthesizer.cleanup_temp_files()
            video_editor.cleanup_temp_files()
            format_generator.cleanup_temp_files()
            thumbnail_generator.cleanup_temp_files()
            
            st.success("✅ Archivos temporales limpiados")
        except Exception as e:
            st.error(f"Error limpiando archivos: {e}")

if __name__ == "__main__":
    main()
