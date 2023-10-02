"""normalized the data to 3FN

Revision ID: f2e61173deeb
Revises: 5dee79da5cde
Create Date: 2023-09-17 12:30:12.637527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2e61173deeb'
down_revision = '5dee79da5cde'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('authors',
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('author_id')
    )
    op.create_table('analysis_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('analyze_date', sa.DateTime(), nullable=True),
    sa.Column('average_commits', sa.Float(), nullable=True),
    sa.Column('repository_url', sa.String(length=50), nullable=True),
    sa.Column('repository_name', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.author_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('git_analysis_results')


def downgrade() -> None:
    op.create_table('git_analysis_results',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('author', sa.VARCHAR(), nullable=True),
    sa.Column('analyze_date', sa.DATETIME(), nullable=True),
    sa.Column('average_commits', sa.FLOAT(), nullable=True),
    sa.Column('repository_url', sa.VARCHAR(), nullable=True),
    sa.Column('repository_name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('analysis_results')
    op.drop_table('authors')
