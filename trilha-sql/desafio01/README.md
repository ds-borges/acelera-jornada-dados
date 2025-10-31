# Ambiente PostgreSQL com pgAdmin usando Docker

Este projeto simplifica a configuração de um ambiente de banco de dados PostgreSQL, provisionando o PostgreSQL e a interface de gerenciamento pgAdmin 4 utilizando Docker Compose. A carga inicial do banco é feita automaticamente a partir do arquivo `google_mail.sql`.

---

## Requisitos

- Docker e Docker Compose instalados
- O arquivo `google_mail.sql` deve estar na raiz do projeto, junto do `docker-compose.yml`
- Diretório local chamado `files` mapeado nos volumes de ambos os serviços Docker

---

## Configuração dos Serviços Docker

O arquivo `docker-compose.yml` define:

| Serviço    | Nome do Container | Imagem           | Variáveis de Ambiente                | Volumes                                                      | Porta(s)         | Rede       |
|------------|-------------------|------------------|------------------------------------|--------------------------------------------------------------|------------------|------------|
| db         | gmaildb           | postgres:latest  | POSTGRES_DB=googlegmail<br>POSTGRES_USER=postgres<br>POSTGRES_PASSWORD=postgres | - `./google_mail.sql:/docker-entrypoint-initdb.d/google_mail.sql`<br>- Outros volumes para dados | 5432, mapeado para 5559 | gmailnet   |
| pgadmin    | gmailpgadmin      | dpage/pgadmin4   | PGADMIN_DEFAULT_EMAIL=pgadmin4@pgadmin.org<br>PGADMIN_DEFAULT_PASSWORD=postgres<br>PGADMIN_LISTEN_PORT=5050<br>PGADMIN_CONFIG_SERVER_MODE=False | Volumes para configuração e dados do pgAdmin                  | 5050             | gmailnet   |

---

## Banco de Dados: Estrutura e Conteúdo Inicial

O banco inicial `googlegmail` é criado e populado a partir do script `google_mail.sql`, que contém a tabela:

| Nome da Tabela           | Descrição                                  | Campo Principal |
|-------------------------|--------------------------------------------|-----------------|
| googlegmailemailsextended | Emails fictícios com remetente, destinatário e dia de envio | `id_user`        |

Os dados inseridos representam envios de e-mail entre usuários com os campos: `id_user`, `from_user`, `to_user`, `day_send`.

---

## Inicialização do Ambiente

Para subir o ambiente, execute:

```bash
docker compose up -d
```

- Acesse o pgAdmin no navegador em `http://localhost:5050`
- Login:
  - Senha: `postgres`

---

## Registrando o Servidor PostgreSQL no pgAdmin

Após o login, adicione um novo servidor com as seguintes configurações:

| Aba       | Configuração                  | Valor                |
|-----------|-------------------------------|----------------------|
| Geral     | Nome do Servidor              | Google_gmail ou outro nome de sua preferência |
| Conexão   | Host name/address             | `db`                 |
| Conexão   | Porta                         | 5432                 |
| Conexão   | Database Maintenance          | postgres             |
| Conexão   | Nome do usuário               | postgres             |
| Conexão   | Senha                         | postgres             |

Salve para visualizar e trabalhar com a base de dados já carregada.

---

Este README atualizado adequa-se ao novo contexto dos arquivos Docker e SQL utilizados no projeto.
