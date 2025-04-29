from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from appCore.backend import db
from appCore.backend.models.profile import Profile
from appCore.backend.models.permission import Permission

profile_bp = Blueprint("profile", __name__)

class ProfileForm(FlaskForm):
    """Formulário para criar/editar perfis de acesso."""
    name = StringField("Nome do Perfil", validators=[DataRequired(), Length(max=50)])
    description = StringField("Descrição", validators=[Length(max=200)])
    permissions = SelectMultipleField("Permissões", coerce=int)
    submit = SubmitField("Salvar")

@profile_bp.route("/list")
@login_required
def list_profiles():
    """Rota para listar perfis de acesso."""
    profiles = Profile.query.all()
    return render_template("miniapps/profile.html", profiles=profiles)

@profile_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Rota para criar um novo perfil de acesso."""
    form = ProfileForm()
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]
    
    if form.validate_on_submit():
        profile = Profile(name=form.name.data, description=form.description.data)
        profile.permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        db.session.add(profile)
        db.session.commit()
        flash("Perfil criado com sucesso!", "success")
        return redirect(url_for("profile.list_profiles"))
    
    return render_template("miniapps/profile.html", form=form, action="create")

@profile_bp.route("/edit/<int:profile_id>", methods=["GET", "POST"])
@login_required
def edit(profile_id):
    """Rota para editar um perfil de acesso."""
    profile = Profile.query.get_or_404(profile_id)
    form = ProfileForm()
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]
    
    if form.validate_on_submit():
        profile.name = form.name.data
        profile.description = form.description.data
        profile.permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("profile.list_profiles"))
    
    form.name.data = profile.name
    form.description.data = profile.description
    form.permissions.data = [p.id for p in profile.permissions]
    return render_template("miniapps/profile.html", form=form, profile=profile, action="edit")