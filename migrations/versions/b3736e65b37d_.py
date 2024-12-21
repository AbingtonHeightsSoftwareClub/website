"""empty message

Revision ID: b3736e65b37d
Revises: 9ba6583ba3e8
Create Date: 2024-12-20 19:27:51.364202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3736e65b37d'
down_revision = '9ba6583ba3e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_properties_players', 'players', ['user_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_constraint('fk_properties_players', type_='foreignkey')
        batch_op.create_foreign_key(None, 'players', ['user_id'], ['id'])

    # ### end Alembic commands ###