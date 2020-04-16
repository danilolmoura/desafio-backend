"""Create first database version

Revision ID: f4a10324c4c5
Revises: 
Create Date: 2020-04-16 11:20:21.324961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4a10324c4c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    op.create_table('trip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_inicio', sa.DateTime(timezone=True), nullable=False),
    sa.Column('data_fim', sa.DateTime(timezone=True), nullable=False),
    sa.Column('classificacao', sa.Enum('TRABALHO', 'ATIVIADADE_FISICA', 'LAZER', 'DESLOCAMENTO', name='enum_bike_trip_type'), nullable=True),
    sa.Column('nota', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trip_data_fim'), 'trip', ['data_fim'], unique=False)
    op.create_index(op.f('ix_trip_data_inicio'), 'trip', ['data_inicio'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trip_data_inicio'), table_name='trip')
    op.drop_index(op.f('ix_trip_data_fim'), table_name='trip')
    op.drop_table('trip')
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###