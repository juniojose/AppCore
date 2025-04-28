from appCore.backend import db

class Settings(db.Model):
    """Modelo para configurações globais da aplicação."""
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(100), nullable=False, default="AppCore")
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<Settings app_name={self.app_name}>"