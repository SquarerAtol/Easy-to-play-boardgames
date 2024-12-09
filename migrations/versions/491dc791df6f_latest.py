"""latest

Revision ID: 491dc791df6f
Revises: 858d2d9f9a0a
Create Date: 2024-12-12 01:40:51.127274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '491dc791df6f'
down_revision = '858d2d9f9a0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Text(length=20),
               existing_nullable=False)
        batch_op.drop_index('ix_posts_parent_id')
        batch_op.drop_index('ix_posts_user_id')
        batch_op.drop_constraint('ix_posts_parent_id', type_='foreignkey')
        batch_op.drop_column('parent_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('ix_posts_parent_id', 'posts', ['parent_id'], ['id'], ondelete='CASCADE')
        batch_op.create_index('ix_posts_user_id', ['user_id'], unique=False)
        batch_op.create_index('ix_posts_parent_id', ['parent_id'], unique=False)
        batch_op.alter_column('title',
               existing_type=sa.Text(length=20),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
