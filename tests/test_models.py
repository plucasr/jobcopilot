from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from jobcopilot.models import Base, Posting


def test_posting_columns() -> None:
    columns = Base.metadata.tables["postings"].columns
    for name in ("id", "title", "company", "url", "source"):
        assert name in columns


def test_posting_defaults() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Posting(title="Dev", company="Acme", url="https://x/1", source="rss"))
        session.flush()
        posting = session.query(Posting).one()
        assert posting.raw_text == ""
        assert posting.fetched_at is not None
