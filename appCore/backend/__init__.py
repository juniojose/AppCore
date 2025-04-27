import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from appCore.config.settings import DevelopmentConfig, ProductionConfig

# Inicializa extensões
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address)

logger = logging.getLogger(__name__)

def create_app(environment: str = "production") -> Flask:
    """Cria e configura a aplicação Flask para o AppCore.

    Args:
        environment: O ambiente da aplicação ('development' ou 'production').

    Returns:
        Instância configurada da aplicação Flask.

    Raises:
        ValueError: Se o ambiente for inválido.
    """
    # Valida o ambiente
    environment = environment.strip().lower()
    if environment not in {"development", "production"}:
        logger.error(f"Ambiente inválido: {environment}")
        raise ValueError("Ambiente deve ser 'development' ou 'production'")

    # Cria a instância da aplicação
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Carrega configurações
    config_class = DevelopmentConfig if environment == "development" else ProductionConfig
    app.config.from_object(config_class)

    # Inicializa extensões
    initialize_extensions(app)

    # Registra blueprints
    register_blueprints(app)

    # Configurações adicionais
    configure_app(app, environment)

    logger.info(f"Aplicação Flask inicializada no ambiente: {environment}")
    return app

def initialize_extensions(app: Flask) -> None:
    """Inicializa as extensões da aplicação.

    Args:
        app: Instância da aplicação Flask.
    """
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    talisman.init_app(app, force_https=app.config["FORCE_HTTPS"], strict_transport_security=True)
    limiter.init_app(app)

    # Configura o login manager
    login_manager.login_view = "users.login"
    login_manager.login_message_category = "info"

def register_blueprints(app: Flask) -> None:
    """Registra os blueprints dos miniApps na aplicação.

    Args:
        app: Instância da aplicação Flask.
    """
    from .routes.core import core_bp
    from .routes.users import users_bp
    from .routes.profile import profile_bp
    from .routes.permissions import permissions_bp
    from .routes.settings import settings_bp
    from .routes.theme import theme_bp

    # Registra blueprints padrão
    app.register_blueprint(core_bp)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(permissions_bp, url_prefix="/permissions")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(theme_bp, url_prefix="/theme")

    # Registra blueprints de miniApps personalizados
    try:
        from app.miniapps.novo_miniapp.blueprints.routes import novo_miniapp_bp
        app.register_blueprint(novo_miniapp_bp, url_prefix="/novo_miniapp")
        logger.info("Blueprint novo_miniapp registrado")
    except ImportError as e:
        logger.warning(f"Falha ao registrar novo_miniapp: {e}")

def configure_app(app: Flask, environment: str) -> None:
    """Aplica configurações adicionais à aplicação.

    Args:
        app: Instância da aplicação Flask.
        environment: O ambiente da aplicação.
    """
    # Configurações de segurança
    app.config["SESSION_COOKIE_SECURE"] = environment == "production"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Limiter para endpoints sensíveis
    limiter.limit("5 per minute")(app.view_functions.get("users.login", lambda: None))