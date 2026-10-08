"""criar tabelas tutores e pets

Revision ID: 0001
Revises:
Create Date: 2026-10-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tutores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_tutores_id"), "tutores", ["id"], unique=False)
    op.create_table(
        "pets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("especie", sa.String(length=50), nullable=False),
        sa.Column("raca", sa.String(length=50), nullable=True),
        sa.Column("idade", sa.Integer(), nullable=True),
        sa.Column("tutor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["tutor_id"], ["tutores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pets_id"), "pets", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_pets_id"), table_name="pets")
    op.drop_table("pets")
    op.drop_index(op.f("ix_tutores_id"), table_name="tutores")
    op.drop_table("tutores")
