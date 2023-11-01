"""added exercise and category models, updated user model

Revision ID: 07a93b012c20
Revises: b9c47cd8c41e
Create Date: 2023-11-01 18:05:47.515751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '07a93b012c20'
down_revision: Union[str, None] = 'b9c47cd8c41e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_id'), 'exercise', ['id'], unique=False)
    op.create_index(op.f('ix_exercise_name'), 'exercise', ['name'], unique=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'create_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('user', 'create_date',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_exercise_name'), table_name='exercise')
    op.drop_index(op.f('ix_exercise_id'), table_name='exercise')
    op.drop_table('exercise')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
