"""nevers

Revision ID: 1178bf18c925
Revises: 06db11cd8556
Create Date: 2023-03-31 12:35:42.786163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1178bf18c925'
down_revision = '06db11cd8556'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('owner', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'chats', 'user', ['owner'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.drop_column('chats', 'owner')
    # ### end Alembic commands ###
