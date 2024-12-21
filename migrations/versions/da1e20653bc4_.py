"""empty message

Revision ID: da1e20653bc4
Revises: c42bcdfd42ce
Create Date: 2024-12-20 19:24:23.473745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da1e20653bc4'
down_revision = 'c42bcdfd42ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'players', ['user_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'players', ['user_id'], ['id'])

    # ### end Alembic commands ###