"""empty message

Revision ID: 1f91df8d3d76
Revises: b3736e65b37d
Create Date: 2024-12-26 12:30:04.400817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f91df8d3d76'
down_revision = 'b3736e65b37d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=256), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=30),
               nullable=False)
        batch_op.alter_column('piece',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('position',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('money',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_no_set',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_color_set',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_1_house',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_2_house',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_3_house',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_4_house',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rent_hotel',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('building_cost',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('mortgage',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('unmortgage',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('color',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=20),
               nullable=False)
        batch_op.drop_constraint('fk_properties_players', type_='foreignkey')
        batch_op.create_foreign_key(None, 'players', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'players', ['user_id'], ['id'], ondelete='SET NULL')
        batch_op.alter_column('color',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('unmortgage',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('mortgage',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('building_cost',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_hotel',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_4_house',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_3_house',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_2_house',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_1_house',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_color_set',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('rent_no_set',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('price',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.alter_column('money',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('position',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('piece',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###