"""empty message

Revision ID: 3c2809cf1af0
Revises: 
Create Date: 2017-02-15 15:10:39.200653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c2809cf1af0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('progress', sa.Float(), nullable=True))
    op.add_column('tasks', sa.Column('status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'status')
    op.drop_column('tasks', 'progress')
    op.drop_column('tasks', 'due_date')
    # ### end Alembic commands ###