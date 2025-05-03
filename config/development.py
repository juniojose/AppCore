from .default import Config
import os

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento."""
    DEBUG = True
    db_uri = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///appcore_dev.db')
    if db_uri.startswith('sqlite:///') and not os.path.isabs(db_uri[10:]):
        db_uri = f"sqlite:///{os.path.abspath(db_uri[10:])}"
    SQLALCHEMY_DATABASE_URI = db_uri