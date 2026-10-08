from fastapi import FastAPI

from app.routers import pets, tutores

app = FastAPI(
    title="API da Clínica Veterinária",
    description="Gerencia tutores e seus pets (Trabalho Prática 03).",
    version="1.0.0",
)

app.include_router(tutores.router)
app.include_router(pets.router)


@app.get("/", tags=["Raiz"])
def raiz():
    return {"mensagem": "API da Clínica Veterinária no ar. Veja /docs"}
