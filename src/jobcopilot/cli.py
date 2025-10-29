import json
import os
from pathlib import Path

import typer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = typer.Typer(help="Jobcopilot CLI")


@app.command()
def version() -> None:
    """Show version."""
    from jobcopilot import __version__

    typer.echo(__version__)


@app.command()
def score(
    database_url: str = typer.Option("sqlite:///jobcopilot.db", "--db", help="SQLAlchemy database URL"),
    profile: Path = typer.Option(None, "--profile", help="Candidate profile JSON file"),
    limit: int = typer.Option(10, "--limit", help="Max postings to score"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Score a sample posting without the LLM"),
) -> None:
    """Score un-scored postings against the candidate profile."""
    from jobcopilot.agents.scoring import ScoringAgent
    from jobcopilot.llm import LlmClient
    from jobcopilot.models import Base, Posting, Score

    profile_path = profile or Path("profile.json")
    profile_data = json.loads(profile_path.read_text())
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    if dry_run:
        typer.echo(json.dumps({"posting_id": 0, "score": 87.0, "reasons": ["dry run"]}, indent=2))
        raise typer.Exit()

    llm = LlmClient(api_key=os.environ.get("LLM_API_KEY"))
    agent = ScoringAgent(llm)

    with Session(engine) as session:
        scored_ids = {row.posting_id for row in session.query(Score).all()}
        postings = [p for p in session.query(Posting).all() if p.id not in scored_ids][:limit]
        for posting in postings:
            result = agent.run(session, posting.id, posting.title, posting.company, posting.raw_text, profile_data)
            typer.echo(f"[{result.score:.0f}] {posting.title} @ {posting.company}")
            for reason in result.reasons:
                typer.echo(f"  - {reason}")


if __name__ == "__main__":
    app()
