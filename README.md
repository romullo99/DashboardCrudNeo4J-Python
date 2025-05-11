# 📊 Neo4j CRUD Dashboard

Um dashboard interativo para gerenciamento de dados em Neo4j, construído com Streamlit e Python.

## 🚀 Funcionalidades

- Visualização de dados com filtros e gráficos
- Operações CRUD completas para pessoas
- Gerenciamento de relacionamentos
- Interface amigável e responsiva
- Visualizações gráficas com Plotly

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Streamlit 1.27.0
- Neo4j 5.17.0
- Pandas 2.0.3
- Plotly 5.15.0

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Acesso a um banco Neo4j (Sandbox ou local)
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd crud-neo4j-fastapi
```

2. Crie e ative um ambiente virtual:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a conexão com o Neo4j:
Crie um arquivo `config.py` com suas credenciais:
```python
SANDBOX_URI = "bolt+s://SEU-SUBDOMINIO.databases.neo4j.io"
SANDBOX_USER = "neo4j"
SANDBOX_PASSWORD = "SUA-SENHA-AQUI"
```

## 🚀 Executando a Aplicação

Execute o comando:
```bash
streamlit run app.py
```

A aplicação estará disponível em: http://localhost:8501

## 📊 Funcionalidades Principais

### Visualização de Dados
- Lista completa de pessoas
- Filtros por idade e profissão
- Gráficos de distribuição por profissão

### Gerenciamento de Pessoas
- Adicionar novas pessoas
- Editar informações existentes
- Remover pessoas do banco

### Relacionamentos
- Criar relacionamentos entre pessoas
- Visualizar conexões existentes
- Tipos de relacionamentos: KNOWS, WORKS_WITH, FRIENDS_WITH

## 🐛 Solução de Problemas

### Problemas de Conexão SSL
Se encontrar problemas de SSL no Windows, adicione ao `config.py`:
```python
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'c:/caminho/para/seu/certificado.pem'
```

### Atualização de Dependências
Para atualizar as dependências:
```bash
pip freeze > requirements.txt
```

## 👥 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📝 Licença

Este projeto está sob a licença MIT.

## 📞 Contato

- GitHub: @romullo99

---