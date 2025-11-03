from sqlalchemy.orm import Session

from jobcopilot.llm import LlmClient, LlmError
from jobcopilot.models import AgentTrace, Letter

SYSTEM_PROMPT = """You write short, specific cover letters. Rules:
- Three paragraphs max: hook, relevant evidence, close.
- Reference the actual company and role.
- No flattery, no buzzwords, no placeholders.
- Output the letter text only, no JSON."""


class LetterAgent:
    def __init__(self, llm: LlmClient, max_attempts: int = 3) -> None:
        self.llm = llm
        self.max_attempts = max_attempts

    def run(self, session: Session, posting_id: int, title: str, company: str, raw_text: str, profile: dict) -> str:
        prompt = self._build_prompt(title, company, raw_text, profile)
        self._trace(session, posting_id, "letter_prompt_built")

        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self.llm.complete(SYSTEM_PROMPT, prompt)
            except LlmError as error:
                self._trace(session, posting_id, f"letter_llm_error_attempt_{attempt}", str(error))
                continue
            self._persist(session, posting_id, response.content, response.model)
            self._trace(session, posting_id, "letter_persisted", f"tokens in={response.input_tokens}")
            return response.content

        raise LlmError(f"Letter drafting failed after {self.max_attempts} attempts")

    def _build_prompt(self, title: str, company: str, raw_text: str, profile: dict) -> str:
        import json

        return (
            f"Candidate profile:\n{json.dumps(profile, indent=2)}\n\n"
            f"Write a cover letter for: {title} at {company}.\n\nJob posting:\n{raw_text[:4000]}"
        )

    def _persist(self, session: Session, posting_id: int, content: str, model: str) -> None:
        session.add(Letter(posting_id=posting_id, content=content, model=model))
        session.commit()

    def _trace(self, session: Session, posting_id: int, step: str, detail: str = "") -> None:
        session.add(AgentTrace(posting_id=posting_id, step=step, detail=detail[:2000]))
        session.commit()
