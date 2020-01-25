"""create_tags_table

Revision ID: cdc7ac137619
Revises: 
Create Date: 2019-12-08 13:01:31.022225

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cdc7ac137619'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    
    op.execute("""
CREATE TABLE tags
(
    tag        TEXT PRIMARY KEY,
    tag__query TEXT NOT NULL
);
""")
    op.execute("""
    CREATE INDEX ft_ix_tag__query_tag ON tags (to_tsquery('simple', tag__query)) WHERE length(tag__query) < 256
    """)


def downgrade():
    op.execute("DROP TABLE tags")
