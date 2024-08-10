"""Initial migration

Revision ID: 838ae6d7d879
Revises: 1e4d057c44b0
Create Date: 2024-08-09 21:46:32.851396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '838ae6d7d879'
down_revision = '1e4d057c44b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sighting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_time', sa.DateTime(timezone=True), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sighting', schema=None) as batch_op:
        batch_op.drop_column('creation_time')

    # ### end Alembic commands ###