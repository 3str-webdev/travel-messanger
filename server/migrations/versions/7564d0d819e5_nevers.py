"""nevers

Revision ID: 7564d0d819e5
Revises: 1178bf18c925
Create Date: 2023-04-04 15:32:26.989285

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7564d0d819e5'
down_revision = '1178bf18c925'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('communities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_community',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('community_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['community_id'], ['communities.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_post',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('photos')
    op.add_column('posts', sa.Column('title', sa.String(length=255), nullable=True))
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=True))
    op.add_column('posts', sa.Column('owner', sa.UUID(), nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'posts', 'user', ['owner'], ['id'])
    op.create_foreign_key(None, 'posts', 'content', ['id'], ['id'])
    op.drop_column('posts', 'permissions')
    op.drop_column('posts', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('posts', sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'owner')
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'title')
    op.create_table('photos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='photos_pkey')
    )
    op.drop_table('user_post')
    op.drop_table('user_community')
    op.drop_table('communities')
    # ### end Alembic commands ###