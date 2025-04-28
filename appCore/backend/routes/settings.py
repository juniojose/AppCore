from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from appCore.backend import db
from appCore.backend.models.settings import Settings  # Assumindo modelo Settings

settings_bp = Blueprint("settings", __name__)

class SettingsForm(FlaskForm):
    """Formulário para atualizar configurações."""
    app_name = StringField("Nome da Aplicação", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Salvar")

@settings_bp.route("/view")
@login_required
def view():
    """Rota para visualizar configurações."""
    settings = Settings.query.first()
    return render_template("miniapps/settings.html", settings=settings)

@settings_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Rota para editar configurações."""
    form = SettingsForm()
    settings = Settings.query.first()
    
    if form.validate_on_submit():
        if not settings:
            settings = Settings()
        settings.app_name = form.app_name.data
        db.session.add(settings)
        db.session.commit()
        flash("Configurações atualizadas com sucesso!", "success")
        return redirect(url_for("settings.view"))
    
    if settings:
        form.app_name.data = settings.app_name
    return render_template("miniapps/settings.html", form=form)