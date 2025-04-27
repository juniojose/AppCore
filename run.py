import os
from dotenv import load_dotenv
from appCore.backend import create_app
from appCore.config.server import setup_logging, run_server

# Carrega variáveis de ambiente
load_dotenv()

def main():
    """Inicializa e executa a aplicação AppCore."""
    # Obtém o ambiente
    environment = os.getenv("FLASK_ENV", "production").strip().lower()

    # Configura o logging
    logger = setup_logging(environment)

    # Cria a aplicação
    app = create_app(environment)
    logger.info(f"Iniciando AppCore no ambiente: {environment}")

    # Executa o servidor
    run_server(app, environment)

if __name__ == "__main__":
    main()