# from flask_app import app
from flask_login import UserMixin
from flask_app.db.db import database as db

class Administrator(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def __repr__(self):
        return f'User: {self.nome}'
    
# # criação do banco de dados
# try:
#     with app.app_context():
#         Administrator.query.first()
# except Exception as e:
#     print(e)
#     with app.app_context():
#        db.create_all()