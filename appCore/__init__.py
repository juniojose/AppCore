"""Módulo principal do AppCore.

Inicializa a aplicação Flask com extensões e configurações baseadas no ambiente.
"""

import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

# Inicializa extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def setup_logging():
    """Configura o sistema de logging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def create_app(env_name=None):
    """Cria e configura a aplicação Flask.

    Args:
        env_name (str, optional): Nome do ambiente ('development' ou 'production').
            Se None, usa FLASK_ENV ou 'development' como padrão.

    Returns:
        Flask: Instância configurada da aplicação Flask.

    Raises:
        ValueError: Se o ambiente não for suportado ou configuração for inválida.
    """
    logger = setup_logging()
    app = Flask(__name__)

    # Carrega configuração com base no ambiente
    env_name = env_name or os.getenv('FLASK_ENV', 'development').lower()
    config_module = f"config.{env_name.capitalize()}Config"
    try:
        app.config.from_object(config_module)
    except ImportError as e:
        logger.error(f"Falha ao carregar configuração para o ambiente '{env_name}': {str(e)}")
        raise ValueError(f"Ambiente '{env_name}' não suportado ou configuração inválida.")

    # Verifica SESSION_COOKIE_SECURE em produção
    if env_name == 'production' and not app.config.get('SESSION_COOKIE_SECURE'):
        logger.warning("SESSION_COOKIE_SECURE deve ser True em produção.")

    # Configura tempo de sessão
    app.permanent_session_lifetime = timedelta(seconds=app.config.get('SESSION_TIMEOUT_SECONDS', 600))

    # Inicializa extensões
    initialize_extensions(app)

    # Configura manipulador de erro 403
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html', message="Acesso negado."), 403

    logger.info(f"Aplicação inicializada no ambiente: {env_name}")
    return app

def initialize_extensions(app):
    """Inicializa extensões Flask com a aplicação."""
    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"

    # Configura carregador de usuário (assumindo modelo Usuario futuro)
    try:
        from app.models import Usuario
        @login_manager.user_loader
        def load_user(user_id):
            return Usuario.query.get(int(user_id))
    except ImportError:
        logging.getLogger(__name__).warning("Modelo Usuario não encontrado. Carregador de usuário não configurado.")