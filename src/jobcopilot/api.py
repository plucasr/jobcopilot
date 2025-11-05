import json
import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from jobcopilot.agents.scoring import ScoringAgent
from jobcopilot.llm import LlmClient
from jobcopilot.models import AgentTrace, Base, Letter, Posting, Score

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///jobcopilot.db")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="Jobcopilot API", version="0.1.0")


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class PostingOut(BaseModel):
    id: int
    title: str
    company: str
    url: str
    source: str

    model_config = {"from_attributes": True}


class ScoreOut(BaseModel):
    posting_id: int
    score: float
    reasons: list[str]
    model: str

    model_config = {"from_attributes": True}


class LetterOut(BaseModel):
    id: int
    posting_id: int
    content: str

    model_config = {"from_attributes": True}


class TraceOut(BaseModel):
    step: str
    detail: str
    created_at: str


def load_profile() -> dict:
    path = Path(os.environ.get("PROFILE_PATH", "profile.json"))
    return json.loads(path.read_text()) if path.exists() else {}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/postings", response_model=list[PostingOut])
def list_postings(db: Session = Depends(get_db)):
    return db.query(Posting).order_by(Posting.fetched_at.desc()).all()


@app.get("/postings/{posting_id}", response_model=PostingOut)
def get_posting(posting_id: int, db: Session = Depends(get_db)):
    posting = db.get(Posting, posting_id)
    if posting is None:
        raise HTTPException(status_code=404, detail="Posting not found")
    return posting


@app.get("/scores", response_model=list[ScoreOut])
def list_scores(db: Session = Depends(get_db)):
    scores = db.query(Score).order_by(Score.score.desc()).all()
    return [
        ScoreOut(
            posting_id=s.posting_id,
            score=s.score,
            reasons=json.loads(s.reasons),
            model=s.model,
        )
        for s in scores
    ]


@app.get("/postings/{posting_id}/traces", response_model=list[TraceOut])
def list_traces(posting_id: int, db: Session = Depends(get_db)):
    traces = (
        db.query(AgentTrace)
        .filter(AgentTrace.posting_id == posting_id)
        .order_by(AgentTrace.created_at)
        .all()
    )
    return [TraceOut(step=t.step, detail=t.detail, created_at=t.created_at.isoformat()) for t in traces]


@app.get("/postings/{posting_id}/letters", response_model=list[LetterOut])
def list_letters(posting_id: int, db: Session = Depends(get_db)):
    return db.query(Letter).filter(Letter.posting_id == posting_id).order_by(Letter.created_at.desc()).all()


@app.post("/postings/{posting_id}/score", response_model=ScoreOut)
def score_posting(posting_id: int, db: Session = Depends(get_db)):
    posting = db.get(Posting, posting_id)
    if posting is None:
        raise HTTPException(status_code=404, detail="Posting not found")

    agent = ScoringAgent(LlmClient(api_key=os.environ.get("LLM_API_KEY")))
    result = agent.run(db, posting.id, posting.title, posting.company, posting.raw_text, load_profile())
    return ScoreOut(posting_id=result.posting_id, score=result.score, reasons=result.reasons, model="unknown")
