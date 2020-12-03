"""empty message

Revision ID: 700ed16f7030
Revises: 9f90ab232821
Create Date: 2020-12-02 23:41:28.167986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '700ed16f7030'
down_revision = '9f90ab232821'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('register', 'password',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=202),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('register', 'password',
               existing_type=sa.String(length=202),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
    # ### end Alembic commands ###
