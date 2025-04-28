from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from appCore.backend import db
from appCore.backend.models.profile import Profile  # Assumindo modelo Profile

profile_bp = Blueprint("profile", __name__)

class ProfileForm(FlaskForm):
    """Formulário para atualizar perfil."""
    bio = StringField("Bio", validators=[Length(max=200)])
    submit = SubmitField("Atualizar")

@profile_bp.route("/view")
@login_required
def view():
    """Rota para visualizar o perfil do usuário."""
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    return render_template("miniapps/profile.html", profile=profile)

@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Rota para editar o perfil do usuário."""
    form = ProfileForm()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    
    if form.validate_on_submit():
        if not profile:
            profile = Profile(user_id=current_user.id)
        profile.bio = form.bio.data
        db.session.add(profile)
        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("profile.view"))
    
    if profile:
        form.bio.data = profile.bio
    return render_template("miniapps/profile.html", form=form)