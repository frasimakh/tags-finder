import re
import unicodedata
from itertools import product
from logging import getLogger

import sqlalchemy as sa
from sqlalchemy import Integer, TEXT
import shlex

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert

from .pg_meta import PG_META_DATA

_bad_chars_re = re.compile(r"[<>^&'()*!|]")


class TagsModel:
    _columns = [
        (("tag", TEXT), dict(nullable=False)),
        (("tag__query", TEXT), dict(nullable=False))
    ]
    _table = sa.Table("tags", PG_META_DATA,
                      *[sa.Column(*args, **kwargs) for args, kwargs in _columns])

    _insert_tag = insert(_table).on_conflict_do_nothing()

    _POSITIONS_DIFFERENCE = [1, 2, 3]

    def __init__(self, pg_engine):
        """
        :param pg_engine: SQLAlchemy engine to run commands to db
        :type pg_engine: sqlalchemy.engine.base.Engine
        """
        self._pg_engine = pg_engine

    def insert_tag(self, tag):
        serialized = {
            'tag': tag,
            'tag__query': self._make_query_from_tag(tag)
        }
        self._pg_engine.execute(self._insert_tag, serialized)

    def _make_query_from_tag(self, tag):
        tag = re.sub(_bad_chars_re, "", tag)
        words = tag.split()
        predicate_pattern = " <{}> ".join(words)
        combinations = list(product(self._POSITIONS_DIFFERENCE, repeat=len(words) - 1))
        predicates = [predicate_pattern.format(*c) for c in combinations]
        return " | ".join(predicates)

    def search_tags_in_text(self, text):
        print(text)
        # tsquery = to_tsquery(self._table.c.tag__query)
        # tsvector = to_tsvector(text)
        tsquery = sa.func.to_tsquery(self._table.c.tag__query)
        tsvector = sa.func.to_tsvector(text)
        _select_founded_tags = sa.select([self._table.c.tag]).where(tsvector.op("@@")(tsquery))

        data = _select_founded_tags.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
        # log.info("[SearchTags]", data=data)
        print(data)
        return list(self._pg_engine.execute(_select_founded_tags))
