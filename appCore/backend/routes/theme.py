from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from appCore.backend import db
from appCore.backend.models.theme import Theme  # Assumindo modelo Theme

theme_bp = Blueprint("theme", __name__)

class ThemeForm(FlaskForm):
    """Formulário para selecionar tema."""
    theme = SelectField("Tema", choices=[("light", "Claro"), ("dark", "Escuro")], validators=[DataRequired()])
    submit = SubmitField("Aplicar")

@theme_bp.route("/select", methods=["GET", "POST"])
@login_required
def select():
    """Rota para selecionar um tema."""
    form = ThemeForm()
    theme = Theme.query.filter_by(user_id=current_user.id).first()
    
    if form.validate_on_submit():
        if not theme:
            theme = Theme(user_id=current_user.id)
        theme.theme = form.theme.data
        db.session.add(theme)
        db.session.commit()
        flash("Tema atualizado com sucesso!", "success")
        return redirect(url_for("theme.select"))
    
    if theme:
        form.theme.data = theme.theme
    return render_template("miniapps/theme.html", form=form)