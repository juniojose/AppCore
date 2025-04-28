from appCore.backend import db

# Tabela associativa para relação N:N entre User e Permission
user_permissions = db.Table(
    "user_permissions",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True)
)

class Permission(db.Model):
    """Modelo para permissões de acesso."""
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamento
    users = db.relationship(
        "User",
        secondary=user_permissions,
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission {self.name}>"