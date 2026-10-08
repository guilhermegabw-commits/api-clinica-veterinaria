from pydantic import BaseModel, ConfigDict, Field


class PetCreate(BaseModel):
    nome: str
    especie: str
    raca: str | None = None
    idade: int | None = Field(default=None, ge=0)
    tutor_id: int


class PetUpdate(BaseModel):
    nome: str | None = None
    especie: str | None = None
    raca: str | None = None
    idade: int | None = Field(default=None, ge=0)
    tutor_id: int | None = None


class PetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    especie: str
    raca: str | None = None
    idade: int | None = None
    tutor_id: int
