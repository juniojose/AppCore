"""Módulo de configurações para o AppCore.

Exporta as classes de configuração e a função get_config para seleção de ambiente.
"""

from .development import DevelopmentConfig
from .production import ProductionConfig
from .default import Config
import os

def get_config():
    """Retorna a configuração com base no ambiente."""
    env = os.getenv('FLASK_ENV', 'production').strip().lower()
    return DevelopmentConfig() if env == 'development' else ProductionConfig()