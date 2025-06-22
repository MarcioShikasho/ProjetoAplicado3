# Sistema de Gestão de Treinamentos e Colaboradores

Sistema web Django para gerenciar treinamentos e colaboradores em uma empresa.

## Tecnologias
- Python
- Django
- HTML
- CSS
- Bootstrap (via template base)
- JavaScript (JQuery, AJAX, Select2)
- SQLite (banco padrão)

## Como executar o projeto

### 1. Clone o repositório:
```bash
git clone https://github.com/MarcioShikasho/ProjetoAplicado3.git
cd seu-repositorio
```

### 2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Aplique as migrações:
```bash
python manage.py migrate
```

### 5. (Opcional) Crie um superusuário:
```bash
python manage.py createsuperuser
```

### 6. Rode o servidor de desenvolvimento:
```bash
python manage.py runserver
```

Acesse: [http://localhost:8000](http://localhost:8000)

## 👤 Acesso ao sistema

Você pode usar o superusuário criado ou cadastrar um novo colaborador com permissão de acesso via painel administrativo.

---

**Observação:** O banco de dados não é incluído por padrão. O Django criará as tabelas automaticamente com `migrate`.