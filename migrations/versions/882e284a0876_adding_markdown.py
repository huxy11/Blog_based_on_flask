"""Adding Markdown

Revision ID: 882e284a0876
Revises: bbeeb1bbbc4e
Create Date: 2019-08-30 14:56:39.365080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882e284a0876'
down_revision = 'bbeeb1bbbc4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('postst', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('postst', 'body_html')
    # ### end Alembic commands ###
