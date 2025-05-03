"""Blueprint principal para rotas básicas do AppCore."""
import logging
from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')

@main_bp.route('/favicon.ico')
def favicon():
    """Redireciona favicon.ico para o arquivo estático."""
    return redirect(url_for('static', filename='favicon.ico'))

@main_bp.route('/search')
def search():
    """Placeholder para a rota de pesquisa."""
    return render_template('index.html')

@main_bp.route('/profile')
def profile():
    """Placeholder para a rota de perfil."""
    return render_template('index.html')

@main_bp.route('/menu/dashboard')
def dashboard():
    """Placeholder para a rota de dashboard."""
    return render_template('index.html')

@main_bp.route('/menu/settings')
def settings():
    """Placeholder para a rota de configurações."""
    return render_template('index.html')

@main_bp.route('/extend_session', methods=['POST'])
def extend_session():
    """Estende a sessão do usuário (simulação)."""
    logging.info('Sessão estendida via /extend_session')
    return '', 204