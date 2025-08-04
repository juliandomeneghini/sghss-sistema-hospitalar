from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Paciente(db.Model):
    """
    Modelo de dados para representar um paciente no sistema SGHSS.
    
    Attributes:
        id (int): Identificador único do paciente
        nome (str): Nome completo do paciente
        cpf (str): CPF do paciente (único)
        data_nascimento (date): Data de nascimento
        endereco (str): Endereço residencial
        telefone (str): Número de telefone
        email (str): Email do paciente (único)
        ativo (bool): Status do paciente (ativo/inativo)
        data_cadastro (datetime): Data e hora do cadastro
        data_atualizacao (datetime): Data e hora da última atualização
    """
    
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False, index=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Paciente {self.nome} - CPF: {self.cpf}>'
    
    def to_dict(self):
        """
        Converte o objeto Paciente para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do paciente
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat()
        }
    
    @staticmethod
    def validar_cpf(cpf):
        """
        Valida se o CPF está no formato correto (apenas números).
        
        Args:
            cpf (str): CPF a ser validado
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not cpf or len(cpf) != 11:
            return False
        return cpf.isdigit()

