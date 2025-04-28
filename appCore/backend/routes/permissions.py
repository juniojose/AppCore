from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from appCore.backend import db
from appCore.backend.models.permission import Permission  # Assumindo modelo Permission

permissions_bp = Blueprint("permissions", __name__)

class PermissionForm(FlaskForm):
    """Formulário para criar/editar permissões."""
    name = StringField("Nome", validators=[DataRequired(), Length(max=50)])
    description = StringField("Descrição", validators=[Length(max=200)])
    submit = SubmitField("Salvar")

@permissions_bp.route("/list")
@login_required
def list_permissions():
    """Rota para listar permissões."""
    permissions = Permission.query.all()
    return render_template("miniapps/permissions.html", permissions=permissions)

@permissions_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Rota para criar uma nova permissão."""
    form = PermissionForm()
    if form.validate_on_submit():
        permission = Permission(name=form.name.data, description=form.description.data)
        db.session.add(permission)
        db.session.commit()
        flash("Permissão criada com sucesso!", "success")
        return redirect(url_for("permissions.list_permissions"))
    return render_template("miniapps/permissions.html", form=form)