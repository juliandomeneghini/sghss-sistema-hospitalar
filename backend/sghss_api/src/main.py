import os
import sys

# Adiciona o diretório pai ao path para encontrar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.models.user import db
from src.models.paciente import Paciente
from src.models.consulta import Consulta, Prontuario
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.pacientes import pacientes_bp
from src.routes.consultas import consultas_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações de segurança
app.config['SECRET_KEY'] = 'sghss-secret-key-2024-production-change-this'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-sghss-2024-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token não expira (para desenvolvimento)

# Configurar CORS para permitir acesso de qualquer origem
CORS(app, origins="*")

# Configurar JWT
jwt = JWTManager(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(pacientes_bp, url_prefix='/api')
app.register_blueprint(consultas_bp, url_prefix='/api')

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---

# Define o caminho para o diretório do banco de dados
db_dir = os.path.join(os.path.dirname(__file__), 'database')

# Cria o diretório se ele não existir (ESSA É A CORREÇÃO PRINCIPAL)
os.makedirs(db_dir, exist_ok=True)

# Configuração do banco de dados usando o caminho absoluto
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_dir, 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ------------------------------------

# Inicializar banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Endpoint de status da API
@app.route('/api/status', methods=['GET'])
def api_status():
    """Endpoint para verificar o status da API."""
    return {
        'status': 'online',
        'message': 'SGHSS API está funcionando',
        'version': '1.0.0'
    }

# Handlers de erro para JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {'error': 'Token expirado'}, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {'error': 'Token inválido'}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {'error': 'Token de autorização necessário'}, 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
