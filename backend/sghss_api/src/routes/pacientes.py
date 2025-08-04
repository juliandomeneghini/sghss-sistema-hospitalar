from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models.paciente import Paciente, db
import re

pacientes_bp = Blueprint("pacientes_bp", __name__)

def validar_cpf(cpf):
    """Valida se o CPF está no formato correto."""
    if not cpf:
        return False
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()

def validar_email(email):
    """Valida se o email está no formato correto."""
    if not email:
        return True  # Email é opcional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_telefone(telefone):
    """Valida se o telefone está no formato correto."""
    if not telefone:
        return True  # Telefone é opcional
    # Remove caracteres não numéricos
    telefone_limpo = re.sub(r'\D', '', telefone)
    return len(telefone_limpo) >= 10 and len(telefone_limpo) <= 11

@pacientes_bp.route("/pacientes", methods=["POST"])
@jwt_required()
def create_paciente():
    """
    Endpoint para cadastrar um novo paciente.
    
    Headers:
        Authorization: Bearer <token>
    
    Body (JSON):
        nome (str): Nome completo do paciente
        cpf (str): CPF do paciente
        data_nascimento (str, opcional): Data de nascimento (YYYY-MM-DD)
        endereco (str, opcional): Endereço do paciente
        telefone (str, opcional): Telefone do paciente
        email (str, opcional): Email do paciente
    
    Returns:
        JSON: Dados do paciente criado ou mensagem de erro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        nome = data.get("nome", "").strip()
        cpf = data.get("cpf", "").strip()
        data_nascimento = data.get("data_nascimento", "").strip()
        endereco = data.get("endereco", "").strip()
        telefone = data.get("telefone", "").strip()
        email = data.get("email", "").strip()
        
        # Validações obrigatórias
        if not nome or not cpf:
            return jsonify({"error": "Nome e CPF são obrigatórios"}), 400
        
        if len(nome) < 2:
            return jsonify({"error": "Nome deve ter pelo menos 2 caracteres"}), 400
        
        # Validar CPF
        if not validar_cpf(cpf):
            return jsonify({"error": "CPF inválido"}), 400
        
        # Limpar CPF (apenas números)
        cpf = re.sub(r'\D', '', cpf)
        
        # Verificar se CPF já existe
        if Paciente.query.filter_by(cpf=cpf).first():
            return jsonify({"error": "Paciente com este CPF já existe"}), 409
        
        # Validar email se fornecido
        if email and not validar_email(email):
            return jsonify({"error": "Email inválido"}), 400
        
        # Verificar se email já existe
        if email and Paciente.query.filter_by(email=email).first():
            return jsonify({"error": "Email já está em uso"}), 409
        
        # Validar telefone se fornecido
        if telefone and not validar_telefone(telefone):
            return jsonify({"error": "Telefone inválido"}), 400
        
        # Validar data de nascimento se fornecida
        data_nasc_obj = None
        if data_nascimento:
            try:
                data_nasc_obj = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Data de nascimento inválida. Use o formato YYYY-MM-DD"}), 400
        
        # Criar novo paciente
        new_paciente = Paciente(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nasc_obj,
            endereco=endereco if endereco else None,
            telefone=telefone if telefone else None,
            email=email if email else None
        )
        
        db.session.add(new_paciente)
        db.session.commit()
        
        return jsonify({
            "message": "Paciente cadastrado com sucesso",
            "paciente": new_paciente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@pacientes_bp.route("/pacientes", methods=["GET"])
@jwt_required()
def get_pacientes():
    """
    Endpoint para listar todos os pacientes ativos.
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        page (int, opcional): Número da página (padrão: 1)
        per_page (int, opcional): Itens por página (padrão: 10, máximo: 100)
        search (str, opcional): Buscar por nome ou CPF
    
    Returns:
        JSON: Lista de pacientes
    """
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        search = request.args.get('search', '').strip()
        
        # Query base
        query = Paciente.query.filter_by(ativo=True)
        
        # Aplicar filtro de busca se fornecido
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                db.or_(
                    Paciente.nome.ilike(search_filter),
                    Paciente.cpf.like(search_filter)
                )
            )
        
        # Aplicar paginação
        pacientes_paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        pacientes_list = [paciente.to_dict() for paciente in pacientes_paginated.items]
        
        return jsonify({
            "pacientes": pacientes_list,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pacientes_paginated.total,
                "pages": pacientes_paginated.pages,
                "has_next": pacientes_paginated.has_next,
                "has_prev": pacientes_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@pacientes_bp.route("/pacientes/<int:paciente_id>", methods=["GET"])
@jwt_required()
def get_paciente(paciente_id):
    """
    Endpoint para obter dados de um paciente específico.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        paciente_id (int): ID do paciente
    
    Returns:
        JSON: Dados do paciente
    """
    try:
        paciente = Paciente.query.get(paciente_id)
        
        if not paciente or not paciente.ativo:
            return jsonify({"error": "Paciente não encontrado"}), 404
        
        return jsonify({
            "paciente": paciente.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@pacientes_bp.route("/pacientes/<int:paciente_id>", methods=["PUT"])
@jwt_required()
def update_paciente(paciente_id):
    """
    Endpoint para atualizar dados de um paciente.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        paciente_id (int): ID do paciente
    
    Body (JSON):
        nome (str, opcional): Nome completo do paciente
        data_nascimento (str, opcional): Data de nascimento (YYYY-MM-DD)
        endereco (str, opcional): Endereço do paciente
        telefone (str, opcional): Telefone do paciente
        email (str, opcional): Email do paciente
    
    Returns:
        JSON: Dados do paciente atualizado ou mensagem de erro
    """
    try:
        paciente = Paciente.query.get(paciente_id)
        
        if not paciente or not paciente.ativo:
            return jsonify({"error": "Paciente não encontrado"}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Atualizar campos se fornecidos
        if "nome" in data:
            nome = data["nome"].strip()
            if len(nome) < 2:
                return jsonify({"error": "Nome deve ter pelo menos 2 caracteres"}), 400
            paciente.nome = nome
        
        if "data_nascimento" in data:
            data_nascimento = data["data_nascimento"].strip()
            if data_nascimento:
                try:
                    paciente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({"error": "Data de nascimento inválida. Use o formato YYYY-MM-DD"}), 400
            else:
                paciente.data_nascimento = None
        
        if "endereco" in data:
            paciente.endereco = data["endereco"].strip() if data["endereco"] else None
        
        if "telefone" in data:
            telefone = data["telefone"].strip()
            if telefone and not validar_telefone(telefone):
                return jsonify({"error": "Telefone inválido"}), 400
            paciente.telefone = telefone if telefone else None
        
        if "email" in data:
            email = data["email"].strip()
            if email:
                if not validar_email(email):
                    return jsonify({"error": "Email inválido"}), 400
                # Verificar se email já existe em outro paciente
                existing_paciente = Paciente.query.filter_by(email=email).first()
                if existing_paciente and existing_paciente.id != paciente_id:
                    return jsonify({"error": "Email já está em uso"}), 409
            paciente.email = email if email else None
        
        db.session.commit()
        
        return jsonify({
            "message": "Paciente atualizado com sucesso",
            "paciente": paciente.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@pacientes_bp.route("/pacientes/<int:paciente_id>", methods=["DELETE"])
@jwt_required()
def delete_paciente(paciente_id):
    """
    Endpoint para desativar um paciente (exclusão lógica).
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        paciente_id (int): ID do paciente
    
    Returns:
        JSON: Mensagem de sucesso ou erro
    """
    try:
        paciente = Paciente.query.get(paciente_id)
        
        if not paciente or not paciente.ativo:
            return jsonify({"error": "Paciente não encontrado"}), 404
        
        # Exclusão lógica
        paciente.ativo = False
        db.session.commit()
        
        return jsonify({
            "message": "Paciente desativado com sucesso"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@pacientes_bp.route("/pacientes/<int:paciente_id>/reativar", methods=["PUT"])
@jwt_required()
def reativar_paciente(paciente_id):
    """
    Endpoint para reativar um paciente.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        paciente_id (int): ID do paciente
    
    Returns:
        JSON: Mensagem de sucesso ou erro
    """
    try:
        paciente = Paciente.query.get(paciente_id)
        
        if not paciente:
            return jsonify({"error": "Paciente não encontrado"}), 404
        
        if paciente.ativo:
            return jsonify({"error": "Paciente já está ativo"}), 400
        
        # Reativar paciente
        paciente.ativo = True
        db.session.commit()
        
        return jsonify({
            "message": "Paciente reativado com sucesso",
            "paciente": paciente.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

