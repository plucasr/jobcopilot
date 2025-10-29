import json
from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from jobcopilot.llm import LlmClient, LlmError, extract_json
from jobcopilot.models import AgentTrace, Score

SYSTEM_PROMPT = """You are a job-matching analyst. Score how well a job posting
matches the candidate profile. Reply with a JSON object only:
{"score": <0-100 integer>, "reasons": ["...", "..."]}"""


@dataclass
class ScoreResult:
    posting_id: int
    score: float
    reasons: list[str] = field(default_factory=list)


class ScoringAgent:
    def __init__(self, llm: LlmClient, max_attempts: int = 3) -> None:
        self.llm = llm
        self.max_attempts = max_attempts

    def run(self, session: Session, posting_id: int, title: str, company: str, raw_text: str, profile: dict) -> ScoreResult:
        prompt = self._build_prompt(title, company, raw_text, profile)
        self._trace(session, posting_id, "prompt_built", prompt)

        last_error = ""
        for attempt in range(1, self.max_attempts + 1):
            response = self._call(session, posting_id, attempt, prompt)
            if response is None:
                continue
            parsed = self._parse(session, posting_id, attempt, response.content)
            if parsed is None:
                continue
            score, reasons = parsed
            self._persist(session, posting_id, response, score, reasons)
            return ScoreResult(posting_id=posting_id, score=score, reasons=reasons)

        raise LlmError(f"Scoring failed after {self.max_attempts} attempts: {last_error}")

    def _build_prompt(self, title: str, company: str, raw_text: str, profile: dict) -> str:
        return (
            f"Candidate profile:\n{json.dumps(profile, indent=2)}\n\n"
            f"Job posting ({title} at {company}):\n{raw_text[:4000]}"
        )

    def _call(self, session: Session, posting_id: int, attempt: int, prompt: str):
        try:
            response = self.llm.complete(SYSTEM_PROMPT, prompt)
        except LlmError as error:
            self._trace(session, posting_id, f"llm_error_attempt_{attempt}", str(error))
            return None
        self._trace(
            session,
            posting_id,
            f"llm_response_attempt_{attempt}",
            f"tokens in={response.input_tokens} out={response.output_tokens}",
        )
        return response

    def _parse(self, session: Session, posting_id: int, attempt: int, content: str):
        try:
            data = extract_json(content)
            score = float(data["score"])
            reasons = [str(reason) for reason in data.get("reasons", [])]
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            self._trace(session, posting_id, f"parse_error_attempt_{attempt}", str(error))
            return None
        self._trace(session, posting_id, f"parsed_attempt_{attempt}", f"score={score}")
        return score, reasons

    def _persist(self, session: Session, posting_id: int, response, score: float, reasons: list[str]) -> None:
        session.add(
            Score(
                posting_id=posting_id,
                score=score,
                reasons=json.dumps(reasons),
                model=response.model,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
            )
        )
        self._trace(session, posting_id, "persisted", f"score={score}")
        session.commit()

    def _trace(self, session: Session, posting_id: int, step: str, detail: str) -> None:
        session.add(AgentTrace(posting_id=posting_id, step=step, detail=detail[:2000]))
        session.commit()
