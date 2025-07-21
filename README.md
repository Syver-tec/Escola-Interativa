# 🎓 Escola Interativa - Sistema de Feedback Educacional

Um sistema completo de gerenciamento de feedback e tickets para instituições educacionais, desenvolvido em Django com interface moderna e funcionalidades avançadas de controle de acesso.

## ✨ Funcionalidades Principais

### 🏫 Gestão Multi-Instituição
- **Múltiplas instituições** com códigos únicos
- **Controle de acesso** por usuário autorizado
- **Superusuários** podem acessar todas as instituições
- **Usuários normais** só veem instituições autorizadas

### 📝 Sistema de Feedback
- **Formulário público** para envio de feedback
- **Tipos de feedback**: Sugestão, Suporte Técnico, Reclamação, Elogio, Dúvida
- **Categorias educacionais**: Administrativo, Acadêmico, Técnico, Infraestrutura, Outro
- **Prioridades**: Baixa, Média, Alta, Urgente
- **Status**: Pendente, Em Andamento, Resolvido, Fechado

### 🎯 Campos Educacionais Específicos
- **Matrícula do estudante**
- **Curso e semestre**
- **Professor e disciplina**
- **Avaliação de satisfação**
- **Notas administrativas**

### 📊 Dashboard Administrativo
- **Estatísticas em tempo real**
- **Filtros avançados** por tipo, categoria, status, prioridade
- **Seleção de instituição** via dropdown
- **Métricas de satisfação**
- **Gestão de responsáveis**

### 🔐 Segurança
- **Autenticação de usuários**
- **Controle de acesso por instituição**
- **Proteção contra acesso não autorizado**
- **Logs de atividades**

## 🚀 Deploy e Produção

### 1. Variáveis Sensíveis e Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=seu_dominio.com,localhost,127.0.0.1
```

No `settings.py`, certifique-se de que as variáveis são lidas do ambiente:

```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-insegura-para-dev')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Coleta de Arquivos Estáticos

Antes de rodar em produção, execute:

```
python manage.py collectstatic
```

### 3. Backup e Migração do Banco de Dados

**Backup do SQLite:**
```
cp db.sqlite3 db_backup.sqlite3
```
**Restauração:**
```
cp db_backup.sqlite3 db.sqlite3
```

**Migração para PostgreSQL:**
No `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Testes de Fluxos e Permissões

- Teste todos os fluxos: envio de feedback, login, dashboard, filtros, relatórios, notas administrativas, priorização, etc.
- Teste com diferentes tipos de usuários (superusuário e usuário comum autorizado).
- Teste o acesso negado para usuários não autorizados em instituições diferentes.
- Teste mensagens de sucesso/erro e responsividade em dispositivos móveis.

### 5. Remover Dependências Não Utilizadas

- Se não for usar mais `django-bootstrap4`, remova de `INSTALLED_APPS` no `settings.py` e do `requirements.txt`.
- Rode `pip freeze > requirements.txt` para atualizar as dependências.

### 6. Deploy Futuro (Netlify ou outro)

> **Nota:** O Netlify não executa Python nativamente. Para deploy Django, recomenda-se usar Render, Railway, Heroku ou outro serviço de backend. O Netlify pode ser usado para frontend estático, caso o projeto seja separado em frontend/backend.

## 🛠️ Desenvolvimento Local

### Instalação

1. **Clonar o repositório**
```bash
git clone https://github.com/seu-usuario/escola-interativa.git
cd escola-interativa
```

2. **Criar ambiente virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Configurar banco de dados**
```bash
python manage.py migrate
```

5. **Criar superusuário**
```bash
python manage.py createsuperuser
```

6. **Executar servidor**
```bash
python manage.py runserver
```

### Comandos de Gestão

#### Criar Instituição
```bash
python manage.py create_institution "Universidade Federal" "ufmg"
```

#### Atribuir Usuário à Instituição
```bash
python manage.py assign_user_to_institution admin ufmg
```

## 🏗️ Estrutura do Projeto

```
EscolaInterativa/
├── api/
│   └── index.py                 # Ponto de entrada para Vercel
├── escola_interativa/
│   ├── settings.py              # Configurações de desenvolvimento
│   ├── production.py            # Configurações de produção
│   ├── urls.py                  # URLs principais
│   └── wsgi.py                  # Configuração WSGI
├── feedback/
│   ├── models.py                # Modelos de dados
│   ├── views.py                 # Lógica de negócio
│   ├── forms.py                 # Formulários
│   ├── urls.py                  # URLs do app
│   ├── admin.py                 # Configuração admin
│   └── management/commands/     # Comandos personalizados
│       ├── create_institution.py
│       └── assign_user_to_institution.py
├── templates/                   # Templates HTML
├── static/                      # Arquivos estáticos
├── requirements.txt             # Dependências Python
├── vercel.json                 # Configuração Vercel
├── runtime.txt                 # Versão Python
└── README.md                   # Este arquivo
```

## 📋 Modelos de Dados

### Institution
- **name**: Nome da instituição
- **code**: Código único
- **domain**: Domínio (opcional)
- **address**: Endereço
- **phone**: Telefone
- **email**: Email de contato
- **logo**: Logo da instituição
- **is_active**: Status ativo
- **authorized_users**: Usuários autorizados (ManyToMany)

### Feedback
- **institution**: Instituição relacionada
- **name**: Nome do remetente
- **email**: Email do remetente
- **type**: Tipo de feedback
- **category**: Categoria educacional
- **message**: Mensagem
- **status**: Status atual
- **priority**: Prioridade
- **student_id**: Matrícula (opcional)
- **course**: Curso (opcional)
- **semester**: Semestre (opcional)
- **teacher**: Professor (opcional)
- **subject**: Disciplina (opcional)
- **admin_note**: Nota administrativa
- **assigned_to**: Responsável
- **satisfaction_rating**: Avaliação de satisfação

## 🎨 Interface

### Página Pública
- **Formulário de feedback** responsivo
- **Campos educacionais** específicos
- **Validação em tempo real**
- **Mensagens de sucesso**

### Dashboard Administrativo
- **Interface moderna** com Bootstrap 5
- **Filtros dinâmicos**
- **Estatísticas visuais**
- **Ações em lote**
- **Seleção de instituição**

## 🔧 Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Deploy**: Vercel
- **Servidor**: WSGI
- **Arquivos Estáticos**: WhiteNoise

## 📊 Funcionalidades Avançadas

### Relatórios
- **Estatísticas por categoria**
- **Métricas de satisfação**
- **Análise temporal**
- **Exportação de dados**

### Gestão de Responsáveis
- **Atribuição de feedback**
- **Controle de responsabilidades**
- **Acompanhamento de tarefas**

### Notificações
- **Alertas de prioridade alta**
- **Lembretes de pendências**
- **Confirmações de ações**

## 🛡️ Segurança

### Controle de Acesso
- **Autenticação obrigatória** para área administrativa
- **Verificação de autorização** por instituição
- **Proteção contra acesso não autorizado**
- **Logs de atividades**

### Validação de Dados
- **Validação de formulários**
- **Sanitização de entrada**
- **Proteção contra CSRF**
- **Validação de tipos**

## 📱 Responsividade

- **Design mobile-first**
- **Interface adaptativa**
- **Componentes responsivos**
- **Navegação otimizada**

## 🚀 Performance

- **Otimização de consultas**
- **Cache de templates**
- **Compressão de arquivos**
- **CDN para arquivos estáticos**

## 📞 Suporte

Para dúvidas, problemas ou sugestões:

1. **Issues do GitHub**: Abra uma issue no repositório
2. **Documentação**: Consulte a documentação do Django
3. **Comunidade**: Participe da comunidade Django

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

---

**Desenvolvido com ❤️ para a comunidade educacional brasileira** 

### Como resolver

1. **Abra o arquivo `.env`** na raiz do seu projeto.
2. **Garanta que a linha de ALLOWED_HOSTS esteja assim:**
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
   (Se já estiver, confira se não há espaços ou erros de digitação.)

3. **Salve o arquivo**.

4. **Pare o servidor (Ctrl+C) e inicie novamente:**
   ```bash
   python manage.py runserver
   ```

---

#### Observação

- Se você acessar por `localhost:8000`, o valor `localhost` precisa estar em `ALLOWED_HOSTS`.
- Se acessar por `127.0.0.1:8000`, o valor `127.0.0.1` precisa estar em `ALLOWED_HOSTS`.
- Para acessar de outro computador na rede, adicione o IP da sua máquina também.

---

Se mesmo assim continuar o erro, me envie o conteúdo do seu `.env` (pode ocultar a SECRET_KEY) para eu conferir! 