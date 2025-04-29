from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from appCore.backend import db, bcrypt
from appCore.backend.models.user import User
from appCore.backend.models.profile import Profile

users_bp = Blueprint("users", __name__)

class LoginForm(FlaskForm):
    """Formulário de login."""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Formulário de registro."""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    profile_id = SelectField("Perfil", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Register")

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    """Rota para login de usuários."""
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("core.index"))
        else:
            flash("Email ou senha inválidos.", "danger")
    return render_template("miniapps/users.html", form=form, action="login")

@users_bp.route("/logout")
@login_required
def logout():
    """Rota para logout de usuários."""
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("core.index"))

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    """Rota para registro de novos usuários."""
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))
    
    form = RegisterForm()
    form.profile_id.choices = [(p.id, p.name) for p in Profile.query.all()]
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            profile_id=form.profile_id.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("users.login"))
    
    return render_template("miniapps/users.html", form=form, action="register")

@users_bp.route("/list")
@login_required
def list_users():
    """Rota para listar todos os usuários."""
    users = User.query.all()
    return render_template("miniapps/users.html", users=users, action="list")