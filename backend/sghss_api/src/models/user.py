from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    Modelo de dados para representar um usuário do sistema SGHSS.
    
    Attributes:
        id (int): Identificador único do usuário
        username (str): Nome de usuário (único)
        password (str): Senha criptografada
        email (str): Email do usuário (único)
        tipo_usuario (str): Tipo do usuário (medico, admin, recepcionista)
        ativo (bool): Status do usuário (ativo/inativo)
        data_cadastro (datetime): Data e hora do cadastro
        data_atualizacao (datetime): Data e hora da última atualização
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    tipo_usuario = db.Column(db.String(20), nullable=False, default='recepcionista')  # medico, admin, recepcionista
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username} - {self.tipo_usuario}>'
    
    def to_dict(self):
        """
        Converte o objeto User para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do usuário (sem a senha)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat()
        }

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
