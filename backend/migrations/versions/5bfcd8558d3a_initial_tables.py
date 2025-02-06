"""initial tables

Revision ID: 5bfcd8558d3a
Revises: 
Create Date: 2024-02-06 19:58:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bfcd8558d3a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # departments テーブル
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('department_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('department_code', 'valid_from')
    )

    # employees テーブル
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('employee_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code'),
        sa.UniqueConstraint('email')
    )

    # assignments テーブル
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('is_main', sa.Boolean(), nullable=False),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # インデックス作成
    op.create_index(
        'ix_departments_parent_id',
        'departments',
        ['parent_id'],
    )
    op.create_index(
        'ix_assignments_employee_id',
        'assignments',
        ['employee_id'],
    )
    op.create_index(
        'ix_assignments_department_id',
        'assignments',
        ['department_id'],
    )


def downgrade() -> None:
    op.drop_index('ix_assignments_department_id', 'assignments')
    op.drop_index('ix_assignments_employee_id', 'assignments')
    op.drop_index('ix_departments_parent_id', 'departments')
    op.drop_table('assignments')
    op.drop_table('employees')
    op.drop_table('departments')
