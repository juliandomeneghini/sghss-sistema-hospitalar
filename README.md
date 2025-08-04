# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

## 📋 Sobre o Projeto

O SGHSS (Sistema de Gestão Hospitalar e de Serviços de Saúde) é um sistema desenvolvido como projeto acadêmico para a disciplina de Projetos Multidisciplinares. O sistema foi projetado para atender às necessidades da instituição fictícia VidaPlus, oferecendo uma solução completa para gestão hospitalar.

## 🎯 Objetivos

- Desenvolver um sistema de gestão hospitalar moderno e eficiente
- Implementar funcionalidades essenciais como cadastro de pacientes, agendamento de consultas e prontuários eletrônicos
- Garantir conformidade com a LGPD (Lei Geral de Proteção de Dados)
- Aplicar boas práticas de desenvolvimento de software
- Demonstrar competências em desenvolvimento back-end, modelagem de dados e arquitetura de sistemas

## 🏗️ Arquitetura do Sistema

O projeto foi desenvolvido seguindo uma arquitetura monolítica em camadas, com separação clara de responsabilidades:

- **Camada de Apresentação**: Rotas da API REST (Flask Blueprints)
- **Camada de Negócio**: Lógica de negócio e validações
- **Camada de Acesso a Dados**: Modelos SQLAlchemy e interação com banco de dados

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.11+**: Linguagem de programação principal
- **Flask**: Framework web para desenvolvimento da API REST
- **SQLAlchemy**: ORM para interação com banco de dados
- **Flask-JWT-Extended**: Autenticação e autorização via JWT
- **Flask-CORS**: Configuração de CORS para APIs
- **SQLite**: Banco de dados para desenvolvimento (facilmente substituível por PostgreSQL/MySQL)

### Ferramentas de Desenvolvimento
- **VS Code**: Editor de código recomendado
- **Git**: Controle de versão
- **Postman**: Testes de API
- **Virtual Environment**: Isolamento de dependências Python

## 📁 Estrutura do Projeto

```
sghss_projeto/
├── backend/
│   └── sghss_api/
│       ├── venv/                    # Ambiente virtual Python
│       ├── src/
│       │   ├── models/              # Modelos de dados
│       │   │   ├── user.py          # Modelo de usuário
│       │   │   ├── paciente.py      # Modelo de paciente
│       │   │   └── consulta.py      # Modelos de consulta e prontuário
│       │   ├── routes/              # Rotas da API
│       │   │   ├── user.py          # Rotas de usuário (template)
│       │   │   ├── auth.py          # Rotas de autenticação
│       │   │   ├── pacientes.py     # Rotas de pacientes
│       │   │   └── consultas.py     # Rotas de consultas
│       │   ├── static/              # Arquivos estáticos
│       │   │   └── index.html       # Página inicial
│       │   ├── database/            # Banco de dados
│       │   │   └── app.db           # Arquivo SQLite
│       │   └── main.py              # Arquivo principal da aplicação
│       └── requirements.txt         # Dependências Python
├── docs/                            # Documentação do projeto
├── tests/                           # Testes automatizados
├── scripts/                         # Scripts auxiliares
└── README.md                        # Este arquivo
```

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.8 ou superior
- Git
- VS Code (recomendado)
- Postman (para testes de API)

### Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd sghss_projeto
   ```

2. **Configure o ambiente virtual**
   ```bash
   cd backend/sghss_api
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

5. **Acesse a aplicação**
   - API: http://localhost:5000
   - Página inicial: http://localhost:5000
   - Status da API: http://localhost:5000/api/status

## 📚 Documentação da API

### Autenticação

#### POST /api/register
Registra um novo usuário no sistema.

**Body:**
```json
{
    "username": "string",
    "password": "string",
    "email": "string (opcional)",
    "tipo_usuario": "medico|admin|recepcionista"
}
```

#### POST /api/login
Autentica um usuário e retorna um token JWT.

**Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "access_token": "jwt_token",
    "user": {
        "id": 1,
        "username": "usuario",
        "tipo_usuario": "medico"
    }
}
```

### Gestão de Pacientes

#### GET /api/pacientes
Lista todos os pacientes ativos (requer autenticação).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `page`: Número da página (padrão: 1)
- `per_page`: Itens por página (padrão: 10, máximo: 100)
- `search`: Buscar por nome ou CPF

#### POST /api/pacientes
Cadastra um novo paciente (requer autenticação).

**Body:**
```json
{
    "nome": "string",
    "cpf": "string",
    "data_nascimento": "YYYY-MM-DD (opcional)",
    "endereco": "string (opcional)",
    "telefone": "string (opcional)",
    "email": "string (opcional)"
}
```

#### GET /api/pacientes/{id}
Obtém dados de um paciente específico.

#### PUT /api/pacientes/{id}
Atualiza dados de um paciente.

#### DELETE /api/pacientes/{id}
Desativa um paciente (exclusão lógica).

### Gestão de Consultas

#### POST /api/consultas
Agenda uma nova consulta.

**Body:**
```json
{
    "paciente_id": 1,
    "medico_id": 1,
    "data_consulta": "YYYY-MM-DD HH:MM",
    "tipo_consulta": "presencial|telemedicina",
    "observacoes": "string (opcional)"
}
```

#### GET /api/consultas
Lista consultas com filtros opcionais.

**Query Parameters:**
- `paciente_id`: Filtrar por paciente
- `medico_id`: Filtrar por médico
- `status`: Filtrar por status
- `data_inicio`: Data de início (YYYY-MM-DD)
- `data_fim`: Data de fim (YYYY-MM-DD)

## 🧪 Testes

### Testes Manuais com Postman

1. **Importe a collection** (arquivo em `tests/postman_collection.json`)
2. **Configure as variáveis de ambiente**:
   - `base_url`: http://localhost:5000
   - `token`: (será preenchido automaticamente após login)

### Casos de Teste Principais

1. **Autenticação**
   - Registro de usuário com dados válidos
   - Login com credenciais corretas
   - Tentativa de acesso sem token

2. **Gestão de Pacientes**
   - Cadastro de paciente com dados válidos
   - Tentativa de cadastro com CPF duplicado
   - Busca de pacientes
   - Atualização de dados
   - Desativação de paciente

3. **Gestão de Consultas**
   - Agendamento de consulta
   - Listagem de consultas
   - Criação de prontuário

## 🔒 Segurança e LGPD

O sistema implementa diversas medidas de segurança e conformidade:

### Autenticação e Autorização
- Autenticação via JWT (JSON Web Tokens)
- Senhas criptografadas com hash seguro
- Controle de acesso baseado em perfis de usuário
- Validação rigorosa de dados de entrada

### Proteção de Dados (LGPD)
- Exclusão lógica de registros (soft delete)
- Criptografia de senhas
- Validação de CPF e email
- Logs de auditoria para rastreabilidade
- Minimização de dados coletados

### Validações Implementadas
- Validação de CPF (formato e unicidade)
- Validação de email (formato e unicidade)
- Validação de senhas (critérios mínimos)
- Sanitização de dados de entrada
- Prevenção contra SQL Injection (via ORM)

## 🚀 Deploy e Produção

### Configurações para Produção

1. **Altere as chaves secretas** em `src/main.py`:
   ```python
   app.config['SECRET_KEY'] = 'sua-chave-secreta-forte'
   app.config['JWT_SECRET_KEY'] = 'sua-jwt-secret-key-forte'
   ```

2. **Configure banco de dados de produção**:
   ```python
   # PostgreSQL
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/sghss'
   
   # MySQL
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/sghss'
   ```

3. **Configure variáveis de ambiente**:
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://...
   export SECRET_KEY=...
   ```

### Deploy com Docker (Opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

## 🤝 Contribuição

Este é um projeto acadêmico, mas contribuições são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é desenvolvido para fins acadêmicos. Consulte o arquivo LICENSE para mais detalhes.

## 👥 Autor

Desenvolvido como projeto acadêmico para a disciplina de Projetos Multidisciplinares.

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Consulte a documentação técnica em `/docs`
- Verifique os logs da aplicação para debugging

---

**Versão:** 1.0.0  
**Data:** 2025  
**Status:** Em desenvolvimento

