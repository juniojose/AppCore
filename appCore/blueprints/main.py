"""Blueprint principal para rotas básicas do AppCore."""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')