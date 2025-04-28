from appCore.backend import db

class Theme(db.Model):
    """Modelo para preferências de tema por usuário."""
    __tablename__ = "themes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    theme = db.Column(db.String(20), nullable=False, default="light")  # Ex.: 'light', 'dark'
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamento
    user = db.relationship("User", back_populates="theme")

    def __repr__(self):
        return f"<Theme user_id={self.user_id} theme={self.theme}>"