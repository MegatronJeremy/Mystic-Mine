"""Custom message.

Revision ID: 51e4e5b700a8
Revises: 
Create Date: 2024-06-15 20:27:16.658161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51e4e5b700a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('couriers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('password', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('couriers', schema=None) as batch_op:
        batch_op.drop_column('password')
        batch_op.drop_column('type')

    # ### end Alembic commands ###
