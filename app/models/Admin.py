from app.models import db, UserMixin

class Adm(db.Model, UserMixin):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def __repr__(self):
        return f'User: {self.nome}'
