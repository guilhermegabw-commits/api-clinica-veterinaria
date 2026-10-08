from pydantic import BaseModel, ConfigDict


class TutorCreate(BaseModel):
    nome: str
    email: str
    telefone: str | None = None


class TutorUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None


class TutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    telefone: str | None = None
