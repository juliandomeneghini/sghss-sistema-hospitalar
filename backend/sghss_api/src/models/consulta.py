from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Consulta(db.Model):
    """
    Modelo de dados para representar uma consulta médica no sistema SGHSS.
    
    Attributes:
        id (int): Identificador único da consulta
        paciente_id (int): ID do paciente (chave estrangeira)
        medico_id (int): ID do médico (chave estrangeira)
        data_consulta (datetime): Data e hora da consulta
        tipo_consulta (str): Tipo da consulta (presencial, telemedicina)
        status (str): Status da consulta (agendada, realizada, cancelada)
        observacoes (str): Observações sobre a consulta
        data_cadastro (datetime): Data e hora do cadastro
        data_atualizacao (datetime): Data e hora da última atualização
    """
    
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)
    tipo_consulta = db.Column(db.String(20), nullable=False, default='presencial')  # presencial, telemedicina
    status = db.Column(db.String(20), nullable=False, default='agendada')  # agendada, realizada, cancelada
    observacoes = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy=True))
    medico = db.relationship('User', backref=db.backref('consultas_medico', lazy=True))
    
    def __repr__(self):
        return f'<Consulta {self.id} - Paciente: {self.paciente_id} - Data: {self.data_consulta}>'
    
    def to_dict(self):
        """
        Converte o objeto Consulta para um dicionário.
        
        Returns:
            dict: Dicionário com os dados da consulta
        """
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'data_consulta': self.data_consulta.isoformat(),
            'tipo_consulta': self.tipo_consulta,
            'status': self.status,
            'observacoes': self.observacoes,
            'data_cadastro': self.data_cadastro.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat()
        }

class Prontuario(db.Model):
    """
    Modelo de dados para representar um prontuário médico no sistema SGHSS.
    
    Attributes:
        id (int): Identificador único do prontuário
        consulta_id (int): ID da consulta (chave estrangeira)
        diagnostico (str): Diagnóstico médico
        prescricao (str): Prescrição médica
        exames_solicitados (str): Exames solicitados
        observacoes_medicas (str): Observações do médico
        data_cadastro (datetime): Data e hora do cadastro
    """
    
    __tablename__ = 'prontuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    diagnostico = db.Column(db.Text, nullable=True)
    prescricao = db.Column(db.Text, nullable=True)
    exames_solicitados = db.Column(db.Text, nullable=True)
    observacoes_medicas = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamento
    consulta = db.relationship('Consulta', backref=db.backref('prontuario', uselist=False))
    
    def __repr__(self):
        return f'<Prontuario {self.id} - Consulta: {self.consulta_id}>'
    
    def to_dict(self):
        """
        Converte o objeto Prontuario para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do prontuário
        """
        return {
            'id': self.id,
            'consulta_id': self.consulta_id,
            'diagnostico': self.diagnostico,
            'prescricao': self.prescricao,
            'exames_solicitados': self.exames_solicitados,
            'observacoes_medicas': self.observacoes_medicas,
            'data_cadastro': self.data_cadastro.isoformat()
        }

