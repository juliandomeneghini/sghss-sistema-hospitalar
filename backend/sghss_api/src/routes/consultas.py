from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from src.models.consulta import Consulta, Prontuario, db
from src.models.paciente import Paciente
from src.models.user import User

consultas_bp = Blueprint("consultas_bp", __name__)

@consultas_bp.route("/consultas", methods=["POST"])
@jwt_required()
def create_consulta():
    """
    Endpoint para agendar uma nova consulta.
    
    Headers:
        Authorization: Bearer <token>
    
    Body (JSON):
        paciente_id (int): ID do paciente
        medico_id (int): ID do médico
        data_consulta (str): Data e hora da consulta (YYYY-MM-DD HH:MM)
        tipo_consulta (str, opcional): Tipo da consulta (presencial, telemedicina)
        observacoes (str, opcional): Observações sobre a consulta
    
    Returns:
        JSON: Dados da consulta criada ou mensagem de erro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        paciente_id = data.get("paciente_id")
        medico_id = data.get("medico_id")
        data_consulta_str = data.get("data_consulta", "").strip()
        tipo_consulta = data.get("tipo_consulta", "presencial").strip()
        observacoes = data.get("observacoes", "").strip()
        
        # Validações obrigatórias
        if not paciente_id or not medico_id or not data_consulta_str:
            return jsonify({"error": "Paciente, médico e data da consulta são obrigatórios"}), 400
        
        # Validar se paciente existe e está ativo
        paciente = Paciente.query.get(paciente_id)
        if not paciente or not paciente.ativo:
            return jsonify({"error": "Paciente não encontrado"}), 404
        
        # Validar se médico existe
        medico = User.query.get(medico_id)
        if not medico:
            return jsonify({"error": "Médico não encontrado"}), 404
        
        # Validar tipo de consulta
        if tipo_consulta not in ['presencial', 'telemedicina']:
            return jsonify({"error": "Tipo de consulta deve ser 'presencial' ou 'telemedicina'"}), 400
        
        # Validar e converter data da consulta
        try:
            data_consulta = datetime.strptime(data_consulta_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Data da consulta inválida. Use o formato YYYY-MM-DD HH:MM"}), 400
        
        # Validar se a data não é no passado
        if data_consulta < datetime.now():
            return jsonify({"error": "Não é possível agendar consulta no passado"}), 400
        
        # Verificar se já existe consulta no mesmo horário para o médico
        consulta_existente = Consulta.query.filter_by(
            medico_id=medico_id,
            data_consulta=data_consulta,
            status='agendada'
        ).first()
        
        if consulta_existente:
            return jsonify({"error": "Médico já possui consulta agendada neste horário"}), 409
        
        # Criar nova consulta
        new_consulta = Consulta(
            paciente_id=paciente_id,
            medico_id=medico_id,
            data_consulta=data_consulta,
            tipo_consulta=tipo_consulta,
            observacoes=observacoes if observacoes else None
        )
        
        db.session.add(new_consulta)
        db.session.commit()
        
        return jsonify({
            "message": "Consulta agendada com sucesso",
            "consulta": new_consulta.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@consultas_bp.route("/consultas", methods=["GET"])
@jwt_required()
def get_consultas():
    """
    Endpoint para listar consultas.
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        page (int, opcional): Número da página (padrão: 1)
        per_page (int, opcional): Itens por página (padrão: 10, máximo: 100)
        paciente_id (int, opcional): Filtrar por paciente
        medico_id (int, opcional): Filtrar por médico
        status (str, opcional): Filtrar por status (agendada, realizada, cancelada)
        data_inicio (str, opcional): Data de início do filtro (YYYY-MM-DD)
        data_fim (str, opcional): Data de fim do filtro (YYYY-MM-DD)
    
    Returns:
        JSON: Lista de consultas
    """
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Filtros
        paciente_id = request.args.get('paciente_id', type=int)
        medico_id = request.args.get('medico_id', type=int)
        status = request.args.get('status', '').strip()
        data_inicio = request.args.get('data_inicio', '').strip()
        data_fim = request.args.get('data_fim', '').strip()
        
        # Query base
        query = Consulta.query
        
        # Aplicar filtros
        if paciente_id:
            query = query.filter_by(paciente_id=paciente_id)
        
        if medico_id:
            query = query.filter_by(medico_id=medico_id)
        
        if status and status in ['agendada', 'realizada', 'cancelada']:
            query = query.filter_by(status=status)
        
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d")
                query = query.filter(Consulta.data_consulta >= data_inicio_obj)
            except ValueError:
                return jsonify({"error": "Data de início inválida. Use o formato YYYY-MM-DD"}), 400
        
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d") + timedelta(days=1)
                query = query.filter(Consulta.data_consulta < data_fim_obj)
            except ValueError:
                return jsonify({"error": "Data de fim inválida. Use o formato YYYY-MM-DD"}), 400
        
        # Ordenar por data da consulta
        query = query.order_by(Consulta.data_consulta.desc())
        
        # Aplicar paginação
        consultas_paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        consultas_list = []
        for consulta in consultas_paginated.items:
            consulta_dict = consulta.to_dict()
            # Adicionar informações do paciente e médico
            consulta_dict['paciente_nome'] = consulta.paciente.nome
            consulta_dict['medico_nome'] = consulta.medico.username
            consultas_list.append(consulta_dict)
        
        return jsonify({
            "consultas": consultas_list,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": consultas_paginated.total,
                "pages": consultas_paginated.pages,
                "has_next": consultas_paginated.has_next,
                "has_prev": consultas_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@consultas_bp.route("/consultas/<int:consulta_id>", methods=["GET"])
@jwt_required()
def get_consulta(consulta_id):
    """
    Endpoint para obter dados de uma consulta específica.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        consulta_id (int): ID da consulta
    
    Returns:
        JSON: Dados da consulta
    """
    try:
        consulta = Consulta.query.get(consulta_id)
        
        if not consulta:
            return jsonify({"error": "Consulta não encontrada"}), 404
        
        consulta_dict = consulta.to_dict()
        consulta_dict['paciente'] = consulta.paciente.to_dict()
        consulta_dict['medico'] = {
            'id': consulta.medico.id,
            'username': consulta.medico.username,
            'email': consulta.medico.email
        }
        
        # Incluir prontuário se existir
        if consulta.prontuario:
            consulta_dict['prontuario'] = consulta.prontuario.to_dict()
        
        return jsonify({
            "consulta": consulta_dict
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@consultas_bp.route("/consultas/<int:consulta_id>/status", methods=["PUT"])
@jwt_required()
def update_consulta_status(consulta_id):
    """
    Endpoint para atualizar o status de uma consulta.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        consulta_id (int): ID da consulta
    
    Body (JSON):
        status (str): Novo status (agendada, realizada, cancelada)
    
    Returns:
        JSON: Dados da consulta atualizada ou mensagem de erro
    """
    try:
        consulta = Consulta.query.get(consulta_id)
        
        if not consulta:
            return jsonify({"error": "Consulta não encontrada"}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        novo_status = data.get("status", "").strip()
        
        if novo_status not in ['agendada', 'realizada', 'cancelada']:
            return jsonify({"error": "Status deve ser 'agendada', 'realizada' ou 'cancelada'"}), 400
        
        consulta.status = novo_status
        db.session.commit()
        
        return jsonify({
            "message": "Status da consulta atualizado com sucesso",
            "consulta": consulta.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@consultas_bp.route("/consultas/<int:consulta_id>/prontuario", methods=["POST"])
@jwt_required()
def create_prontuario(consulta_id):
    """
    Endpoint para criar um prontuário para uma consulta.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        consulta_id (int): ID da consulta
    
    Body (JSON):
        diagnostico (str, opcional): Diagnóstico médico
        prescricao (str, opcional): Prescrição médica
        exames_solicitados (str, opcional): Exames solicitados
        observacoes_medicas (str, opcional): Observações do médico
    
    Returns:
        JSON: Dados do prontuário criado ou mensagem de erro
    """
    try:
        consulta = Consulta.query.get(consulta_id)
        
        if not consulta:
            return jsonify({"error": "Consulta não encontrada"}), 404
        
        # Verificar se já existe prontuário
        if consulta.prontuario:
            return jsonify({"error": "Consulta já possui prontuário"}), 409
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        diagnostico = data.get("diagnostico", "").strip()
        prescricao = data.get("prescricao", "").strip()
        exames_solicitados = data.get("exames_solicitados", "").strip()
        observacoes_medicas = data.get("observacoes_medicas", "").strip()
        
        # Criar prontuário
        new_prontuario = Prontuario(
            consulta_id=consulta_id,
            diagnostico=diagnostico if diagnostico else None,
            prescricao=prescricao if prescricao else None,
            exames_solicitados=exames_solicitados if exames_solicitados else None,
            observacoes_medicas=observacoes_medicas if observacoes_medicas else None
        )
        
        db.session.add(new_prontuario)
        
        # Atualizar status da consulta para realizada
        consulta.status = 'realizada'
        
        db.session.commit()
        
        return jsonify({
            "message": "Prontuário criado com sucesso",
            "prontuario": new_prontuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@consultas_bp.route("/prontuarios/<int:prontuario_id>", methods=["PUT"])
@jwt_required()
def update_prontuario(prontuario_id):
    """
    Endpoint para atualizar um prontuário.
    
    Headers:
        Authorization: Bearer <token>
    
    Path Parameters:
        prontuario_id (int): ID do prontuário
    
    Body (JSON):
        diagnostico (str, opcional): Diagnóstico médico
        prescricao (str, opcional): Prescrição médica
        exames_solicitados (str, opcional): Exames solicitados
        observacoes_medicas (str, opcional): Observações do médico
    
    Returns:
        JSON: Dados do prontuário atualizado ou mensagem de erro
    """
    try:
        prontuario = Prontuario.query.get(prontuario_id)
        
        if not prontuario:
            return jsonify({"error": "Prontuário não encontrado"}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Atualizar campos se fornecidos
        if "diagnostico" in data:
            prontuario.diagnostico = data["diagnostico"].strip() if data["diagnostico"] else None
        
        if "prescricao" in data:
            prontuario.prescricao = data["prescricao"].strip() if data["prescricao"] else None
        
        if "exames_solicitados" in data:
            prontuario.exames_solicitados = data["exames_solicitados"].strip() if data["exames_solicitados"] else None
        
        if "observacoes_medicas" in data:
            prontuario.observacoes_medicas = data["observacoes_medicas"].strip() if data["observacoes_medicas"] else None
        
        db.session.commit()
        
        return jsonify({
            "message": "Prontuário atualizado com sucesso",
            "prontuario": prontuario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

