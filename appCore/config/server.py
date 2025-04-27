import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

# Configuração de constantes
DEFAULT_HOST_DEV = "127.0.0.1"
DEFAULT_HOST_PROD = "0.0.0.0"
DEFAULT_PORT = 5000
VALID_ENVIRONMENTS = {"development", "production"}
LOG_FILE = "appcore.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

def setup_logging(environment: str) -> logging.Logger:
    """Configura o logging para a aplicação.

    Args:
        environment: O ambiente da aplicação ('development' ou 'production').

    Returns:
        Logger configurado para a aplicação.

    Raises:
        ValueError: Se o ambiente for inválido.
    """
    # Valida o ambiente
    environment = validate_environment(environment)

    logger = logging.getLogger(__name__)
    
    # Define o nível de logging baseado no ambiente
    log_level = logging.DEBUG if environment == "development" else logging.INFO
    logger.setLevel(log_level)

    # Evita múltiplos handlers
    if not logger.handlers:
        # Formato do log
        log_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        # Handler para arquivo com rotação
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger

def validate_environment(env: str) -> str:
    """Valida o ambiente da aplicação.

    Args:
        env: Nome do ambiente a ser validado.

    Returns:
        O ambiente validado em letras minúsculas.

    Raises:
        ValueError: Se o ambiente for inválido.
    """
    env = env.strip().lower()
    if env not in VALID_ENVIRONMENTS:
        raise ValueError(f"Ambiente inválido: {env}. Use: {', '.join(VALID_ENVIRONMENTS)}")
    return env

def run_server(app: Flask, environment: str) -> None:
    """Executa o servidor da aplicação no ambiente especificado.

    Args:
        app: Instância da aplicação Flask.
        environment: O ambiente da aplicação ('development' ou 'production').

    Raises:
        Exception: Se houver erro ao executar o servidor.
    """
    logger = logging.getLogger(__name__)

    # Valida o ambiente
    environment = validate_environment(environment)

    # Configurações baseadas no ambiente
    debug_mode = environment == "development"
    host = DEFAULT_HOST_DEV if debug_mode else DEFAULT_HOST_PROD
    port = int(os.getenv("PORT", DEFAULT_PORT))

    # Log de inicialização
    logger.info(f"Executando servidor em {host}:{port} (Debug: {debug_mode})")

    if debug_mode:
        # Modo desenvolvimento: usa servidor Flask
        try:
            app.run(host=host, port=port, debug=True, use_reloader=True)
        except Exception as e:
            logger.exception("Erro ao executar a aplicação em modo desenvolvimento:")
            raise
    else:
        # Modo produção: usa gunicorn
        from gunicorn.app.base import Application

        class FlaskApplication(Application):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        gunicorn_options = {
            "bind": f"{host}:{port}",
            "workers": (os.cpu_count() or 1) * 2 + 1,  # Fórmula: 2*CPU + 1
            "timeout": 30,
            "loglevel": "info",
            "accesslog": "-",
            "errorlog": "-",
        }

        try:
            FlaskApplication(app, gunicorn_options).run()
        except Exception as e:
            logger.exception("Erro ao executar a aplicação em modo produção:")
            raise