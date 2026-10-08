from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Tutor
from app.schemas import PetResponse, TutorCreate, TutorResponse, TutorUpdate

router = APIRouter(prefix="/tutores", tags=["Tutores"])


def _get_tutor_or_404(db: Session, tutor_id: int) -> Tutor:
    tutor = db.get(Tutor, tutor_id)
    if tutor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tutor não encontrado")
    return tutor


@router.post("/", response_model=TutorResponse, status_code=status.HTTP_201_CREATED)
def criar_tutor(dados: TutorCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Tutor).where(Tutor.email == dados.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")
    tutor = Tutor(**dados.model_dump())
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor


@router.get("/", response_model=list[TutorResponse])
def listar_tutores(db: Session = Depends(get_db)):
    return db.scalars(select(Tutor)).all()


@router.get("/{tutor_id}", response_model=TutorResponse)
def obter_tutor(tutor_id: int, db: Session = Depends(get_db)):
    return _get_tutor_or_404(db, tutor_id)


@router.get("/{tutor_id}/pets", response_model=list[PetResponse])
def listar_pets_do_tutor(tutor_id: int, db: Session = Depends(get_db)):
    return _get_tutor_or_404(db, tutor_id).pets


@router.patch("/{tutor_id}", response_model=TutorResponse)
def atualizar_tutor(tutor_id: int, dados: TutorUpdate, db: Session = Depends(get_db)):
    tutor = _get_tutor_or_404(db, tutor_id)
    campos = dados.model_dump(exclude_unset=True)
    novo_email = campos.get("email")
    if novo_email and novo_email != tutor.email:
        if db.scalar(select(Tutor).where(Tutor.email == novo_email)):
            raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")
    for campo, valor in campos.items():
        setattr(tutor, campo, valor)
    db.commit()
    db.refresh(tutor)
    return tutor


@router.delete("/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = _get_tutor_or_404(db, tutor_id)
    db.delete(tutor)
    db.commit()
