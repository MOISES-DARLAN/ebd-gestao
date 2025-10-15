# Sistema de Gestão para EBD - El Shaday

## Sobre o Projeto

Este projeto é uma aplicação web desenvolvida em Django, destinada ao gerenciamento de classes da Escola Bíblica Dominical (EBD) da igreja Assembleia de Deus El Shaday. O sistema foi criado para substituir processos manuais, oferecendo uma plataforma centralizada para que professores e administradores possam acompanhar a frequência, o desempenho e a participação dos alunos de forma eficiente e moderna.

A aplicação conta com um design responsivo, adaptando-se a desktops, tablets e dispositivos móveis, e utiliza um banco de dados PostgreSQL para garantir a persistência e segurança dos dados.

## Funcionalidades Principais

- **Autenticação e Níveis de Acesso:**
    - Área restrita para professores com login e senha.
    - Painel de controle exclusivo para administradores (`is_staff`).

- **Painel do Administrador:**
    - Visão geral com estatísticas do sistema (total de turmas, alunos, professores).
    - Resumo da atividade do dia (total de presentes, ofertas, visitantes).
    - Ranking diário e semestral de turmas, baseado na média de pontos por aluno.
    - Acesso rápido aos relatórios detalhados de cada turma.

- **Fluxo do Professor:**
    - Dashboard com a visualização de todas as turmas cadastradas.
    - Acesso seguro a cada turma através de um código de acesso único.
    - Painel de controle por turma, com acesso rápido às principais funcionalidades.

- **Sistema de Chamada e Pontuação:**
    - Interface para realização da chamada diária.
    - Registro de múltiplos critérios de pontuação por aluno:
        - Presença (15 pts)
        - Contribuição (10 pts)
        - Participação (0, 5 ou 10 pts)
        - Bíblia (5 pts)
        - Revista (5 pts)
        - Levar Visitante (20 pts)
    - Cálculo e exibição da pontuação total do aluno no semestre.
    - Registro de dados gerais da aula (oferta total e número de visitantes).

- **Gerenciamento de Alunos (CRUD):**
    - Professores autorizados podem adicionar, editar e excluir alunos de suas respectivas turmas.
    - Validações no formulário para garantir a integridade dos dados (idade, formato do nome, etc.).

- **Relatórios Avançados:**
    - Histórico de todas as chamadas realizadas por uma turma.
    - Relatório detalhado por dia, com a pontuação e os status de cada aluno.
    - Página de análise visual com gráficos de desempenho (ranking de alunos e frequência da turma).

## Tecnologias Utilizadas

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3 (Flexbox, Grid Layout)
- **Banco de Dados:** PostgreSQL (conectado via Supabase)
- **Servidor de Produção:** Gunicorn, WhiteNoise
- **Bibliotecas Principais:**
    - `psycopg`: Driver de conexão com o PostgreSQL.
    - `dj-database-url`: Para configuração segura da URL do banco de dados.
    - `python-dotenv`: Para gerenciamento de variáveis de ambiente.
    - `Chart.js`: Para a renderização dos gráficos no frontend.

## Começando (Ambiente Local)

Para configurar e executar o projeto localmente, siga os passos abaixo.

### Pré-requisitos

- Python (versão 3.10 ou superior) - RECOMENDO PYTHON 3.12
- `pip` (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MOISES-DARLAN/ebd-gestao.git
    cd nome-da-pasta-do-projeto
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    - Crie um arquivo chamado `.env` na pasta raiz do projeto.
    - Copie o conteúdo do exemplo abaixo para o seu `.env` e preencha com suas credenciais.

    **`.env.example`:**
    ```
    DATABASE_URL=
    SECRET_KEY=
    DJANGO_DEBUG=True
    ```

5.  **Execute as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

6.  **Crie um superusuário (administrador):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

O site estará disponível em `http://127.0.0.1:8000/`.

## Deploy

O projeto está configurado para deploy na plataforma Render. As principais configurações são:

- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- **Start Command:** `gunicorn config.wsgi`
- **Variáveis de Ambiente:** As mesmas do arquivo `.env` (`DATABASE_URL`, `SECRET_KEY`, `DJANGO_DEBUG=False`) devem ser configuradas na interface do Render.

## Licença

Distribuído sob a licença MIT. Veja `LICENSE.txt` para mais informações.
