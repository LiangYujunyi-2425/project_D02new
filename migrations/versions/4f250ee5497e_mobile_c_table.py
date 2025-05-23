"""Mobile_c table

Revision ID: 4f250ee5497e
Revises: 6092228cc420
Create Date: 2025-04-11 07:34:46.896839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f250ee5497e'
down_revision = '6092228cc420'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('health_care',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mobile_c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('voice_c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('voice_c')
    op.drop_table('mobile_c')
    op.drop_table('health_care')
    # ### end Alembic commands ###
