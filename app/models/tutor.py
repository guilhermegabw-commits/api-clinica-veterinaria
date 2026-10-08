from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Tutor(Base):
    __tablename__ = "tutores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    pets: Mapped[list["Pet"]] = relationship(
        back_populates="tutor", cascade="all, delete-orphan"
    )
