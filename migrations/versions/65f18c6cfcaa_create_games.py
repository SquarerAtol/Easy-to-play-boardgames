"""create games

Revision ID: 65f18c6cfcaa
Revises: bb6406a1913d
Create Date: 2024-10-17 03:34:50.087126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65f18c6cfcaa'
down_revision = 'bb6406a1913d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('file', sa.String(length=255), nullable=False),
    sa.Column('title', sa.Text(length=20), nullable=False),
    sa.Column('description', sa.Text(length=100), nullable=False),
    sa.Column('upload_path', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('body',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('body',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    op.drop_table('games')
    # ### end Alembic commands ###