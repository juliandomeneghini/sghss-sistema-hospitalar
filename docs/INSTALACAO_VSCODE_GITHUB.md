# Guia Completo: Configurando SGHSS no VS Code e Publicando no GitHub

Este guia detalhado irá te ajudar a configurar o projeto SGHSS no Visual Studio Code e publicá-lo no GitHub, desde a configuração inicial até o primeiro commit.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Visual Studio Code**: [Download VS Code](https://code.visualstudio.com/)
- **Conta no GitHub**: [Criar conta](https://github.com/join)

## 🔧 Parte 1: Configuração do VS Code

### 1.1 Instalação de Extensões Essenciais

Abra o VS Code e instale as seguintes extensões:

1. **Python (Microsoft)**
   - Pressione `Ctrl+Shift+X` para abrir a aba de extensões
   - Pesquise por "Python" e instale a extensão oficial da Microsoft
   - Esta extensão fornece IntelliSense, debugging, formatação e muito mais

2. **Pylance (Microsoft)**
   - Pesquise por "Pylance" e instale
   - Melhora significativamente o IntelliSense para Python

3. **GitLens — Git supercharged**
   - Pesquise por "GitLens" e instale
   - Adiciona recursos avançados do Git ao VS Code

4. **REST Client (Huachao Mao)**
   - Pesquise por "REST Client" e instale
   - Permite testar APIs diretamente no VS Code

### 1.2 Configuração do Workspace

1. **Abra a pasta do projeto**:
   - `Arquivo > Abrir Pasta...` (ou `Ctrl+K Ctrl+O`)
   - Navegue até a pasta `sghss_projeto` e selecione

2. **Configure o interpretador Python**:
   - Pressione `Ctrl+Shift+P` para abrir a paleta de comandos
   - Digite "Python: Select Interpreter"
   - Selecione o interpretador dentro da pasta `venv` do projeto

3. **Configure o workspace**:
   - Crie um arquivo `.vscode/settings.json` na raiz do projeto:
   ```json
   {
       "python.defaultInterpreterPath": "./backend/sghss_api/venv/bin/python",
       "python.terminal.activateEnvironment": true,
       "python.linting.enabled": true,
       "python.linting.pylintEnabled": true,
       "python.formatting.provider": "black",
       "editor.formatOnSave": true,
       "files.exclude": {
           "**/__pycache__": true,
           "**/*.pyc": true,
           "**/venv": true
       }
   }
   ```

## 🐍 Parte 2: Configuração do Ambiente Python

### 2.1 Verificação do Python

Abra o terminal integrado do VS Code (`Ctrl+Shift+` `` ` ``) e execute:

```bash
python --version
# ou
python3 --version
```

Você deve ver uma versão 3.8 ou superior.

### 2.2 Configuração do Ambiente Virtual

1. **Navegue até a pasta do backend**:
   ```bash
   cd backend/sghss_api
   ```

2. **Ative o ambiente virtual**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Verifique as dependências**:
   ```bash
   pip list
   ```

4. **Se necessário, instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

### 2.3 Teste da Aplicação

1. **Execute a aplicação**:
   ```bash
   python src/main.py
   ```

2. **Teste no navegador**:
   - Acesse: http://localhost:5000
   - Você deve ver a página inicial do SGHSS

3. **Teste a API**:
   - Acesse: http://localhost:5000/api/status
   - Deve retornar um JSON com o status da API

## 🐙 Parte 3: Configuração do Git e GitHub

### 3.1 Configuração Inicial do Git

Se é a primeira vez usando Git, configure suas informações:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 3.2 Inicialização do Repositório Local

1. **Na raiz do projeto** (`sghss_projeto`), execute:
   ```bash
   git init
   ```

2. **Crie um arquivo .gitignore**:
   ```bash
   # Arquivo .gitignore
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   *.egg-info/
   .installed.cfg
   *.egg
   
   # Virtual Environment
   venv/
   env/
   ENV/
   
   # Database
   *.db
   *.sqlite3
   
   # IDE
   .vscode/
   .idea/
   
   # OS
   .DS_Store
   Thumbs.db
   
   # Logs
   *.log
   
   # Environment variables
   .env
   ```

3. **Adicione os arquivos ao staging**:
   ```bash
   git add .
   ```

4. **Faça o primeiro commit**:
   ```bash
   git commit -m "Initial commit: SGHSS project setup"
   ```

### 3.3 Criação do Repositório no GitHub

1. **Acesse o GitHub** e faça login
2. **Clique em "New repository"** (botão verde)
3. **Configure o repositório**:
   - **Repository name**: `sghss-sistema-hospitalar`
   - **Description**: "Sistema de Gestão Hospitalar e de Serviços de Saúde - Projeto Acadêmico"
   - **Visibility**: Public ou Private (sua escolha)
   - **NÃO** marque "Initialize this repository with a README"
4. **Clique em "Create repository"**

### 3.4 Conectando o Repositório Local ao GitHub

1. **Adicione o remote origin**:
   ```bash
   git remote add origin https://github.com/SEU_USUARIO/sghss-sistema-hospitalar.git
   ```

2. **Verifique a conexão**:
   ```bash
   git remote -v
   ```

3. **Envie o código para o GitHub**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

## 📝 Parte 4: Workflow de Desenvolvimento

### 4.1 Estrutura de Branches

Para um desenvolvimento organizado, use a seguinte estrutura:

```bash
# Branch principal
main

# Branches de desenvolvimento
develop

# Branches de features
feature/nome-da-funcionalidade

# Branches de correção
hotfix/nome-da-correcao
```

### 4.2 Comandos Git Essenciais

```bash
# Verificar status
git status

# Adicionar arquivos modificados
git add .
git add arquivo_especifico.py

# Fazer commit
git commit -m "Descrição clara da mudança"

# Enviar para o GitHub
git push origin main

# Baixar mudanças do GitHub
git pull origin main

# Criar nova branch
git checkout -b feature/nova-funcionalidade

# Trocar de branch
git checkout main

# Listar branches
git branch

# Merge de branch
git checkout main
git merge feature/nova-funcionalidade
```

### 4.3 Boas Práticas para Commits

1. **Use mensagens descritivas**:
   ```bash
   # ✅ Bom
   git commit -m "Add patient registration validation"
   git commit -m "Fix JWT token expiration issue"
   git commit -m "Update API documentation"
   
   # ❌ Ruim
   git commit -m "fix"
   git commit -m "update"
   git commit -m "changes"
   ```

2. **Faça commits pequenos e frequentes**
3. **Teste antes de fazer commit**
4. **Use o padrão de commit semântico** (opcional):
   ```bash
   feat: add new feature
   fix: bug fix
   docs: documentation changes
   style: formatting changes
   refactor: code refactoring
   test: adding tests
   ```

## 🔄 Parte 5: Sincronização Contínua

### 5.1 Workflow Diário

1. **Antes de começar a trabalhar**:
   ```bash
   git pull origin main
   ```

2. **Durante o desenvolvimento**:
   ```bash
   # Salve frequentemente
   git add .
   git commit -m "Descrição da mudança"
   ```

3. **Ao final do dia**:
   ```bash
   git push origin main
   ```

### 5.2 Trabalhando com Issues

1. **Crie issues no GitHub** para organizar tarefas
2. **Referencie issues nos commits**:
   ```bash
   git commit -m "Fix patient validation bug - closes #5"
   ```

### 5.3 Usando Pull Requests

Para projetos em equipe:

1. **Crie uma branch para sua feature**:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. **Desenvolva e faça commits**
3. **Envie a branch**:
   ```bash
   git push origin feature/nova-funcionalidade
   ```

4. **Crie um Pull Request no GitHub**
5. **Aguarde review e merge**

## 🛠️ Parte 6: Ferramentas Auxiliares

### 6.1 Testando a API no VS Code

Crie um arquivo `tests/api_tests.http`:

```http
### Status da API
GET http://localhost:5000/api/status

### Registro de usuário
POST http://localhost:5000/api/register
Content-Type: application/json

{
    "username": "admin",
    "password": "123456",
    "email": "admin@sghss.com",
    "tipo_usuario": "admin"
}

### Login
POST http://localhost:5000/api/login
Content-Type: application/json

{
    "username": "admin",
    "password": "123456"
}

### Listar pacientes (substitua o token)
GET http://localhost:5000/api/pacientes
Authorization: Bearer SEU_TOKEN_AQUI
```

### 6.2 Debugging no VS Code

1. **Crie um arquivo `.vscode/launch.json`**:
   ```json
   {
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
   ```

2. **Use breakpoints** clicando na margem esquerda do código
3. **Execute em modo debug** pressionando `F5`

## 🚨 Solução de Problemas Comuns

### Problema: "Python não encontrado"
**Solução**: Verifique se o Python está no PATH do sistema

### Problema: "Módulo não encontrado"
**Solução**: 
```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstale as dependências
pip install -r requirements.txt
```

### Problema: "Permission denied" no Git
**Solução**: Configure as credenciais do Git ou use SSH

### Problema: "Port already in use"
**Solução**: 
```bash
# Encontre o processo usando a porta 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Mate o processo ou use outra porta
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Git Documentation](https://git-scm.com/doc)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

### Tutoriais Recomendados
- [Git e GitHub para Iniciantes](https://www.youtube.com/watch?v=UBAX-13g8OM)
- [Flask Tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/)
- [VS Code Python Setup](https://code.visualstudio.com/docs/python/environments)

## ✅ Checklist Final

Antes de considerar a configuração completa, verifique:

- [ ] VS Code instalado com extensões Python
- [ ] Projeto aberto no VS Code
- [ ] Ambiente virtual ativado
- [ ] Aplicação executando sem erros
- [ ] Git configurado com suas credenciais
- [ ] Repositório criado no GitHub
- [ ] Código enviado para o GitHub
- [ ] README.md atualizado
- [ ] .gitignore configurado
- [ ] Testes básicos da API funcionando

Parabéns! Seu ambiente de desenvolvimento está configurado e seu projeto está no GitHub. Agora você pode desenvolver com confiança e manter seu código versionado e seguro.

---

**Dica Final**: Mantenha sempre backups do seu trabalho e faça commits frequentes. O Git é seu melhor amigo para não perder código!

