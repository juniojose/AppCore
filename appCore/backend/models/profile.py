from appCore.backend import db

# Tabela associativa para relação N:N entre Profile e Permission
profile_permissions = db.Table(
    "profile_permissions",
    db.Column("profile_id", db.Integer, db.ForeignKey("profiles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True)
)

class Profile(db.Model):
    """Modelo para perfis de acesso (papéis) da aplicação."""
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamentos
    users = db.relationship("User", back_populates="profile")
    permissions = db.relationship(
        "Permission",
        secondary=profile_permissions,
        back_populates="profiles"
    )

    def __repr__(self):
        return f"<Profile {self.name}>"