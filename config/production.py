from .default import Config
import os

class ProductionConfig(Config):
    """Configurações para produção."""
    DEBUG = False
    db_uri = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///appcore_prod.db')
    if db_uri.startswith('sqlite:///') and not os.path.isabs(db_uri[10:]):
        db_uri = f"sqlite:///{os.path.abspath(db_uri[10:])}"
    SQLALCHEMY_DATABASE_URI = db_uri
    SESSION_COOKIE_SECURE = True  # Forçado em produção