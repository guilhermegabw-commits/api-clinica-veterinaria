from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    especie: Mapped[str] = mapped_column(String(50), nullable=False)
    raca: Mapped[str | None] = mapped_column(String(50), nullable=True)
    idade: Mapped[int | None] = mapped_column(nullable=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutores.id"), nullable=False)

    tutor: Mapped["Tutor"] = relationship(back_populates="pets")
