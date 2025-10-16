from jobcopilot.models import Base, Posting


def test_posting_columns() -> None:
    columns = Base.metadata.tables["postings"].columns
    for name in ("id", "title", "company", "url", "source"):
        assert name in columns


def test_posting_defaults() -> None:
    posting = Posting(title="Dev", company="Acme", url="https://x/1", source="rss")
    assert posting.raw_text == ""
