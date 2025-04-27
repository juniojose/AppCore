import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configuração base para a aplicação."""
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    FORCE_HTTPS = True
    SESSION_TYPE = "filesystem"

class DevelopmentConfig(Config):
    """Configuração para o ambiente de desenvolvimento."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///dev.db")
    FORCE_HTTPS = False

class ProductionConfig(Config):
    """Configuração para o ambiente de produção."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///prod.db")