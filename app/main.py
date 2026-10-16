from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import pets, tutores

app = FastAPI(
    title="API da Clínica Veterinária",
    description="Gerencia tutores e seus pets (Trabalho Prática 03).",
    version="1.0.0",
)

app.include_router(tutores.router)
app.include_router(pets.router)

PAGINA_INICIAL = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>API da Clínica Veterinária</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: linear-gradient(135deg, #0f766e, #14b8a6);
      color: #0f172a;
    }
    .card {
      background: #ffffff;
      padding: 48px 40px;
      border-radius: 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
      text-align: center;
      max-width: 420px;
      width: 90%;
    }
    .emoji { font-size: 56px; margin-bottom: 12px; }
    h1 { font-size: 26px; margin-bottom: 8px; }
    p { color: #475569; margin-bottom: 28px; }
    a.botao {
      display: inline-block;
      padding: 14px 32px;
      background: #0f766e;
      color: #ffffff;
      text-decoration: none;
      font-weight: 600;
      border-radius: 999px;
      transition: transform 0.15s, background 0.15s;
    }
    a.botao:hover { background: #115e59; transform: translateY(-2px); }
  </style>
</head>
<body>
  <div class="card">
    <div class="emoji">🐾</div>
    <h1>API da Clínica Veterinária</h1>
    <p>Gerenciamento de tutores e pets.</p>
    <a class="botao" href="/docs">Abrir documentação (Swagger)</a>
  </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def raiz():
    return PAGINA_INICIAL