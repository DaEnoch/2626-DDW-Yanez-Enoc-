# models.py
from flask_login import UserMixin


class Usuario(UserMixin):
    # clase compatible con flask-login, envuelve los datos del usuario
    def __init__(self, id, usuario, password):
        self.id = id
        self.usuario = usuario
        self.password = password
