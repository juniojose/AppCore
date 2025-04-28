from flask import Blueprint, render_template

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
def index():
    """Renderiza a página inicial da aplicação."""
    return render_template("miniapps/core.html")