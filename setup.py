"""
Script de configuración para Cine Norte
Configura el entorno y verifica dependencias
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cine-norte",
    version="1.0.0",
    author="Cine Norte Team",
    author_email="soporte@cinenorte.com",
    description="Generador Automatizado de Contenido Audiovisual para Redes Sociales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/cine-norte",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "gpu": [
            "torch[cuda]>=1.9.0",
            "torchvision[cuda]>=0.10.0",
            "torchaudio[cuda]>=0.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cine-norte=run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords=[
        "video", "audio", "ai", "machine-learning", "streaming", 
        "content-creation", "social-media", "automation", "cinema"
    ],
    project_urls={
        "Bug Reports": "https://github.com/tu-usuario/cine-norte/issues",
        "Source": "https://github.com/tu-usuario/cine-norte",
        "Documentation": "https://github.com/tu-usuario/cine-norte/wiki",
    },
)
