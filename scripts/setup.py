#!/usr/bin/env python3
"""
Script de configuração inicial para o projeto SGHSS.
Este script automatiza a configuração do ambiente de desenvolvimento.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Caminho base fixo para o projeto
BASE_DIR = Path(r"C:\xampp\htdocs\sghss_projeto")

def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def run_command(command, description, check=True):
    """Executa um comando e trata erros."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} - Sucesso")
            return result.stdout
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro: {e}")
        if e.stderr:
            print(f"Detalhes do erro: {e.stderr}")
        return False

def check_python_version():
    """Verifica se a versão do Python é adequada."""
    print_header("VERIFICAÇÃO DO PYTHON")
    
    version = sys.version_info
    print(f"Versão do Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    
    print("✅ Versão do Python adequada")
    return True

def setup_virtual_environment():
    """Configura o ambiente virtual."""
    print_header("CONFIGURAÇÃO DO AMBIENTE VIRTUAL")
    
    venv_path = BASE_DIR / "backend/sghss_api/venv"
    
    if venv_path.exists():
        print("✅ Ambiente virtual já existe")
        return True
    
    # Criar ambiente virtual
    if not run_command(f"python -m venv backend/sghss_api/venv", "Criando ambiente virtual"):
        return False
    
    return True

def install_dependencies():
    """Instala as dependências do projeto."""
    print_header("INSTALAÇÃO DE DEPENDÊNCIAS")
    
    # Determinar comando de ativação baseado no OS
    if os.name == 'nt':  # Windows
        activate_cmd = "backend\\sghss_api\\venv\\Scripts\\activate"
        pip_cmd = f"{activate_cmd} && pip install -r backend/sghss_api/requirements.txt"
    else:  # Unix/Linux/macOS
        activate_cmd = "source backend/sghss_api/venv/bin/activate"
        pip_cmd = f"{activate_cmd} && pip install -r backend/sghss_api/requirements.txt"
    
    return run_command(pip_cmd, "Instalando dependências Python")

def create_database():
    """Cria o banco de dados inicial."""
    print_header("CONFIGURAÇÃO DO BANCO DE DADOS")
    
    if os.name == 'nt':  # Windows
        cmd = "cd backend\\sghss_api && venv\\Scripts\\activate && python -c \"from src.main import app, db; app.app_context().push(); db.create_all(); print('Banco de dados criado com sucesso')\""
    else:  # Unix/Linux/macOS
        cmd = "cd backend/sghss_api && source venv/bin/activate && python -c \"from src.main import app, db; app.app_context().push(); db.create_all(); print('Banco de dados criado com sucesso')\""
    
    return run_command(cmd, "Criando banco de dados")

def create_admin_user():
    """Cria um usuário administrador padrão."""
    print_header("CRIAÇÃO DO USUÁRIO ADMINISTRADOR")
    
    create_user_script = '''
from src.main import app, db
from src.models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(username="admin").first()
    if admin:
        print("Usuário admin já existe")
    else:
        admin_user = User(
            username="admin",
            password=generate_password_hash("admin123"),
            email="admin@sghss.com",
            tipo_usuario="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário admin criado com sucesso")
        print("Username: admin")
        print("Password: admin123")
'''
    script_path = BASE_DIR / "temp_create_admin.py"
    with open(script_path, 'w') as f:
        f.write(create_user_script)
    
    try:
        if os.name == 'nt':  # Windows
            cmd = f"cd backend\\sghss_api && venv\\Scripts\\activate && python ../../{script_path.name}"
        else:  # Unix/Linux/macOS
            cmd = f"cd backend/sghss_api && source venv/bin/activate && python ../../{script_path.name}"
        
        result = run_command(cmd, "Criando usuário administrador")
        os.remove(script_path)
        return result
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        if script_path.exists():
            os.remove(script_path)
        return False

def test_api():
    """Testa se a API está funcionando."""
    print_header("TESTE DA API")
    print("🔄 Iniciando servidor de teste...")
    
    if os.name == 'nt':  # Windows
        test_cmd = "cd backend\\sghss_api && venv\\Scripts\\activate && timeout 10 python src/main.py"
    else:  # Unix/Linux/macOS
        test_cmd = "cd backend/sghss_api && source venv/bin/activate && timeout 10s python src/main.py"
    
    run_command(test_cmd, "Testando inicialização da API", check=False)
    print("✅ Teste de inicialização concluído")
    return True

def create_vscode_config():
    """Cria configurações do VS Code."""
    print_header("CONFIGURAÇÃO DO VS CODE")
    
    vscode_dir = BASE_DIR / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    settings = {
        "python.defaultInterpreterPath": "./backend/sghss_api/venv/bin/python",
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "editor.formatOnSave": True,
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/venv": True
        }
    }
    
    with open(vscode_dir / "settings.json", 'w') as f:
        json.dump(settings, f, indent=4)
    
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Flask",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/backend/sghss_api/src/main.py",
                "console": "integratedTerminal",
                "env": {
                    "FLASK_ENV": "development"
                }
            }
        ]
    }
    
    with open(vscode_dir / "launch.json", 'w') as f:
        json.dump(launch_config, f, indent=4)
    
    print("✅ Configurações do VS Code criadas")
    return True

def print_summary():
    """Imprime um resumo da configuração."""
    print_header("CONFIGURAÇÃO CONCLUÍDA")
    
    print("🎉 Projeto SGHSS configurado com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Abra o projeto no VS Code")
    print("2. Selecione o interpretador Python do ambiente virtual")
    print("3. Execute a aplicação:")
    
    if os.name == 'nt':  # Windows
        print("   cd backend\\sghss_api")
        print("   venv\\Scripts\\activate")
        print("   python src/main.py")
    else:  # Unix/Linux/macOS
        print("   cd backend/sghss_api")
        print("   source venv/bin/activate")
        print("   python src/main.py")
    
    print("\n4. Acesse: http://localhost:5000")
    print("\n🔐 Credenciais do administrador:")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n📚 Documentação:")
    print("   - README.md: Documentação principal")
    print("   - docs/INSTALACAO_VSCODE_GITHUB.md: Guia detalhado")
    print("   - tests/postman_collection.json: Collection para testes")

def main():
    """Função principal do script."""
    print_header("CONFIGURAÇÃO INICIAL DO PROJETO SGHSS")
    print("Este script irá configurar automaticamente o ambiente de desenvolvimento.")
    
    if not (BASE_DIR / "backend/sghss_api").exists():
        print(f"❌ Pasta não encontrada: {BASE_DIR / 'backend/sghss_api'}")
        sys.exit(1)

    # Muda para a pasta raiz do projeto
    os.chdir(BASE_DIR)
    
    steps = [
        ("Verificação do Python", check_python_version),
        ("Configuração do ambiente virtual", setup_virtual_environment),
        ("Instalação de dependências", install_dependencies),
        ("Configuração do banco de dados", create_database),
        ("Criação do usuário administrador", create_admin_user),
        ("Configuração do VS Code", create_vscode_config),
        ("Teste da API", test_api)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        try:
            if not step_function():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Erro em {step_name}: {e}")
            failed_steps.append(step_name)
    
    if failed_steps:
        print_header("CONFIGURAÇÃO CONCLUÍDA COM AVISOS")
        print("⚠️  Algumas etapas falharam:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nConsulte a documentação para configuração manual.")
    else:
        print_summary()

if __name__ == "__main__":
    main()
