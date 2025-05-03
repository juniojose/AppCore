import os

def validate_config():
    """Valida configurações críticas."""
    secret_key = os.getenv('SECRET_KEY', 'alterar_essa_chave')
    if secret_key == 'alterar_essa_chave' or len(secret_key) < 32:
        raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres e ser configurada no .env.")
    session_timeout = os.getenv('SESSION_TIMEOUT_MINUTES', '30')
    if not session_timeout.isdigit() or int(session_timeout) <= 0:
        raise ValueError("SESSION_TIMEOUT_MINUTES deve ser um número positivo.")

class Config:
    """Configurações padrão para todos os ambientes."""
    validate_config()
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') in ('True', 'true', '1')
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_TIMEOUT_SECONDS = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30')) * 60