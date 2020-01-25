from sqlalchemy import create_engine

from .tags import TagsModel

PG_MIGRATIONS_SQL = {
    'user': "mykolashved",
    'password': "password",
    'host': "localhost",
    'port': 5432,
    'db': "tags-finder"
}

PG_ENGINE = create_engine(
    'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**PG_MIGRATIONS_SQL)
)

TAGS_MODEL = TagsModel(PG_ENGINE)
