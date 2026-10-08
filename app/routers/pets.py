from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Pet, Tutor
from app.schemas import PetCreate, PetResponse, PetUpdate

router = APIRouter(prefix="/pets", tags=["Pets"])


def _get_pet_or_404(db: Session, pet_id: int) -> Pet:
    pet = db.get(Pet, pet_id)
    if pet is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pet não encontrado")
    return pet


def _verificar_tutor(db: Session, tutor_id: int) -> None:
    if db.get(Tutor, tutor_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Tutor {tutor_id} não existe"
        )


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def criar_pet(dados: PetCreate, db: Session = Depends(get_db)):
    _verificar_tutor(db, dados.tutor_id)  # validação de integridade
    pet = Pet(**dados.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/", response_model=list[PetResponse])
def listar_pets(especie: str | None = None, db: Session = Depends(get_db)):
    consulta = select(Pet)
    if especie:
        consulta = consulta.where(Pet.especie == especie)
    return db.scalars(consulta).all()


@router.get("/{pet_id}", response_model=PetResponse)
def obter_pet(pet_id: int, db: Session = Depends(get_db)):
    return _get_pet_or_404(db, pet_id)


@router.put("/{pet_id}", response_model=PetResponse)
def atualizar_pet(pet_id: int, dados: PetUpdate, db: Session = Depends(get_db)):
    pet = _get_pet_or_404(db, pet_id)
    campos = dados.model_dump(exclude_unset=True)
    if "tutor_id" in campos and campos["tutor_id"] is not None:
        _verificar_tutor(db, campos["tutor_id"])
    for campo, valor in campos.items():
        setattr(pet, campo, valor)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = _get_pet_or_404(db, pet_id)
    db.delete(pet)
    db.commit()
