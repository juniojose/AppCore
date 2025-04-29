from appCore.backend import db

class Permission(db.Model):
    """Modelo para permissões de acesso."""
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamento
    profiles = db.relationship(
        "Profile",
        secondary="profile_permissions",
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission {self.name}>"