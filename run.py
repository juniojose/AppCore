"""Script de inicialização da aplicação Flask AppCore.

Configura o ambiente, logging e validação de hosts com base em variáveis de ambiente.
Suporta ambientes de desenvolvimento e produção.
"""

import os
import logging
from flask import Flask, abort, request, redirect
from app import create_app
from config import DevelopmentConfig, ProductionConfig, get_config
from dotenv import load_dotenv
from datetime import timedelta

# Constantes
FLASK_ENV_DEVELOPMENT = 'development'
FLASK_ENV_PRODUCTION = 'production'

def setup_logging():
    """Configura o sistema de logging."""
    log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def validate_environment():
    """Valida variáveis de ambiente críticas."""
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key or len(secret_key) < 32:
        raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres.")

def main():
    """Inicializa a aplicação Flask."""
    load_dotenv()
    logger = setup_logging()
    validate_environment()

    # Seleciona configuração
    config = get_config()
    app = create_app()
    app.config.from_object(config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=int(os.getenv('SESSION_TIMEOUT', 30)))

    # Garante debug=False em produção
    flask_env = os.getenv('FLASK_ENV', FLASK_ENV_PRODUCTION).strip().lower()
    if flask_env == FLASK_ENV_PRODUCTION and config.DEBUG:
        logger.warning("Modo debug desativado em produção por segurança.")
        config.DEBUG = False

    # Middleware para validar hosts
    allowed_hosts = set(config.ALLOWED_HOSTS) if config.ALLOWED_HOSTS else set()
    @app.before_request
    def validate_host():
        if allowed_hosts and request.host not in allowed_hosts:
            logger.warning(f"Host não permitido: {request.host}")
            abort(403, description="Host não permitido")

    # Força HTTPS em produção
    @app.before_request
    def enforce_https():
        if flask_env == FLASK_ENV_PRODUCTION and not request.is_secure:
            return redirect(request.url.replace('http://', 'https://'), code=301)

    try:
        logger.info(f"Iniciando a aplicação em {config.HOST}:{config.PORT} (Debug: {config.DEBUG})")
        app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
    except OSError as e:
        logger.exception(f"Erro ao iniciar o servidor (possível problema de porta): {str(e)}")
        raise SystemExit("A aplicação encontrou um erro crítico e será encerrada.")

if __name__ == "__main__":
    main()