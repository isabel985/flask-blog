"""added fk to post table

Revision ID: 55bb3e121391
Revises: 60b6aec27b1f
Create Date: 2020-06-30 11:50:48.364045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55bb3e121391'
down_revision = '60b6aec27b1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###