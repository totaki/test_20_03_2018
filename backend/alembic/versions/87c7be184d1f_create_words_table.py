"""Create words table

Revision ID: 87c7be184d1f
Revises: 
Create Date: 2018-03-20 09:46:32.042455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c7be184d1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'words',
        sa.Column('hash', sa.CHAR(64), primary_key=True),
        sa.Column('word', sa.Text(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
    )


def downgrade():
    op.drop_table('words')
