from flask_login import UserMixin
from appCore.backend import db

class User(UserMixin, db.Model):
    """Modelo para usuários da aplicação."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamentos
    profile = db.relationship("Profile", back_populates="users")
    theme = db.relationship("Theme", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"

    # Propriedades exigidas pelo Flask-Login
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def has_permission(self, permission_name: str) -> bool:
        """Verifica se o usuário tem uma permissão específica via perfil."""
        if not self.profile:
            return False
        return any(permission.name == permission_name for permission in self.profile.permissions)