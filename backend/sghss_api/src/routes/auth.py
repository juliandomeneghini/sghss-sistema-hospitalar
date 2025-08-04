from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db
import re

auth_bp = Blueprint("auth_bp", __name__)

def validar_email(email):
    """Valida se o email está no formato correto."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_senha(senha):
    """Valida se a senha atende aos critérios mínimos de segurança."""
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    return True, "Senha válida"

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Endpoint para registro de novos usuários.
    
    Body (JSON):
        username (str): Nome de usuário
        password (str): Senha do usuário
        email (str, opcional): Email do usuário
        tipo_usuario (str, opcional): Tipo do usuário (medico, admin, recepcionista)
    
    Returns:
        JSON: Mensagem de sucesso ou erro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        username = data.get("username", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()
        tipo_usuario = data.get("tipo_usuario", "recepcionista").strip()
        
        # Validações
        if not username or not password:
            return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400
        
        if len(username) < 3:
            return jsonify({"error": "Nome de usuário deve ter pelo menos 3 caracteres"}), 400
        
        # Validar senha
        senha_valida, mensagem_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({"error": mensagem_senha}), 400
        
        # Validar email se fornecido
        if email and not validar_email(email):
            return jsonify({"error": "Email inválido"}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Nome de usuário já existe"}), 409
        
        if email and User.query.filter_by(email=email).first():
            return jsonify({"error": "Email já está em uso"}), 409
        
        # Criar novo usuário
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username, 
            password=hashed_password,
            email=email if email else None,
            tipo_usuario=tipo_usuario
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "user_id": new_user.id,
            "username": new_user.username
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Endpoint para autenticação de usuários.
    
    Body (JSON):
        username (str): Nome de usuário
        password (str): Senha do usuário
    
    Returns:
        JSON: Token de acesso JWT ou mensagem de erro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        username = data.get("username", "").strip()
        password = data.get("password", "")
        
        if not username or not password:
            return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400
        
        # Buscar usuário
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        # Criar token JWT
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "username": user.username,
                "tipo_usuario": user.tipo_usuario
            }
        )
        
        return jsonify({
            "message": "Login realizado com sucesso",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "tipo_usuario": user.tipo_usuario
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    Endpoint para obter o perfil do usuário autenticado.
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        JSON: Dados do perfil do usuário
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "tipo_usuario": user.tipo_usuario,
                "data_cadastro": user.data_cadastro.isoformat() if hasattr(user, 'data_cadastro') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    """
    Endpoint para alterar a senha do usuário autenticado.
    
    Headers:
        Authorization: Bearer <token>
    
    Body (JSON):
        current_password (str): Senha atual
        new_password (str): Nova senha
    
    Returns:
        JSON: Mensagem de sucesso ou erro
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        current_password = data.get("current_password", "")
        new_password = data.get("new_password", "")
        
        if not current_password or not new_password:
            return jsonify({"error": "Senha atual e nova senha são obrigatórias"}), 400
        
        # Verificar senha atual
        if not check_password_hash(user.password, current_password):
            return jsonify({"error": "Senha atual incorreta"}), 401
        
        # Validar nova senha
        senha_valida, mensagem_senha = validar_senha(new_password)
        if not senha_valida:
            return jsonify({"error": mensagem_senha}), 400
        
        # Atualizar senha
        user.password = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({"message": "Senha alterada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

