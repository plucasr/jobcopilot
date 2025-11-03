import hashlib

from sqlalchemy.orm import Session

from jobcopilot.models import Posting


def posting_key(title: str, company: str) -> str:
    normalized = f"{title.strip().lower()}|{company.strip().lower()}"
    return hashlib.sha256(normalized.encode()).hexdigest()


def is_duplicate(session: Session, title: str, company: str) -> bool:
    digest = posting_key(title, company)
    return any(posting_key(p.title, p.company) == digest for p in session.query(Posting).all())


def insert_unique(session: Session, title: str, company: str, url: str, source: str, raw_text: str = "") -> Posting | None:
    if is_duplicate(session, title, company):
        return None
    posting = Posting(title=title, company=company, url=url, source=source, raw_text=raw_text)
    session.add(posting)
    session.commit()
    return posting
