# API da Clínica Veterinária

Trabalho Prática 03 — Arquitetura de Software (ADS, Bloco IV 2026.2)

**Integrantes:** _(preencher com os nomes do grupo)_

## Modelo de negócio

Uma clínica veterinária que precisa cadastrar os **tutores** (donos) e os **pets**
de cada um. A API permite gerenciar esses cadastros, consultar os pets de um tutor
e filtrar pets por espécie.

## Entidades e relacionamento

| Tutor (`tutores`) | Pet (`pets`) |
|---|---|
| id (PK) | id (PK) |
| nome | nome |
| email (único) | especie |
| telefone (opcional) | raca (opcional) |
| | idade (opcional, >= 0) |
| | tutor_id (FK → tutores.id) |

```
Tutor 1 ────────< N Pet
```

Um tutor possui vários pets; cada pet pertence a um único tutor.
No SQLAlchemy: `Tutor.pets` e `Pet.tutor` via `relationship()`.
Ao excluir um tutor, seus pets também são excluídos (cascade).

## Estrutura do projeto

```
app/
├── main.py          # instancia o FastAPI e registra os routers
├── core/            # configuração e conexão com o banco
├── models/          # modelos SQLAlchemy
├── schemas/         # schemas Pydantic (Create / Update / Response)
└── routers/         # endpoints
alembic/             # migrações (versions/ contém as migrations)
```

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

alembic upgrade head             # cria o banco (vet.db) via migrações
uvicorn app.main:app --reload
```

Acesse o Swagger em http://127.0.0.1:8000/docs

Para gerar novas migrações após alterar os modelos:

```bash
alembic revision --autogenerate -m "descricao"
alembic upgrade head
```

## Endpoints

| Método | Rota | Descrição | Status |
|---|---|---|---|
| POST | `/tutores/` | Cria tutor | 201 (409 se e-mail repetido) |
| GET | `/tutores/` | Lista tutores | 200 |
| GET | `/tutores/{id}` | Busca tutor | 200 / 404 |
| GET | `/tutores/{id}/pets` | Lista pets do tutor | 200 / 404 |
| PATCH | `/tutores/{id}` | Atualiza tutor | 200 / 404 |
| DELETE | `/tutores/{id}` | Remove tutor (e seus pets) | 204 / 404 |
| POST | `/pets/` | Cria pet (valida se o tutor existe) | 201 / 404 |
| GET | `/pets/` | Lista pets (`?especie=Cachorro`) | 200 |
| GET | `/pets/{id}` | Busca pet | 200 / 404 |
| PUT | `/pets/{id}` | Atualiza pet (valida tutor se alterado) | 200 / 404 |
| DELETE | `/pets/{id}` | Remove pet | 204 / 404 |

Dados inválidos retornam **422** automaticamente (validação do Pydantic).
