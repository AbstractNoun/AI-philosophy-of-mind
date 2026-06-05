from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from modest_proposal.parser import parse_scored_response
from modest_proposal.prompts import CONDITIONS, QUESTIONS, build_single_question_prompt
from modest_proposal.smoke import SmokeRequest, run_smoke_test


@dataclass(frozen=True)
class PilotModel:
    label: str
    provider: str
    model: str
    reasoning_effort: str | None = None
    reasoning_enabled: bool | None = None
    anthropic_effort: str | None = None
    anthropic_thinking: bool = False
    prompt_style: str = "instruction"
    max_tokens: int | None = None
    timeout_s: float | None = None


DEFAULT_PILOT_MODELS = [
    PilotModel(
        label="ollama_llama31_8b_instruct_q8",
        provider="ollama",
        model="llama3.1:8b-instruct-q8_0",
    ),
    PilotModel(
        label="openai_gpt_5_5_none",
        provider="openai",
        model="gpt-5.5",
        reasoning_effort="none",
    ),
    PilotModel(
        label="anthropic_claude_sonnet_4_6_low",
        provider="anthropic",
        model="claude-sonnet-4-6",
        anthropic_effort="low",
    ),
    PilotModel(
        label="together_llama_3_3_70b_turbo",
        provider="together",
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    ),
]


def run_pilot(
    models: list[PilotModel] | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> list[dict]:
    selected_models = models or DEFAULT_PILOT_MODELS
    rows: list[dict] = []
    run_id = datetime.now(timezone.utc).strftime("pilot_%Y%m%dT%H%M%SZ")

    for pilot_model in selected_models:
        for condition in CONDITIONS:
            for question_id, question_text in QUESTIONS.items():
                prompt = build_single_question_prompt(
                    condition,
                    question_id,
                    style=pilot_model.prompt_style,
                )
                try:
                    reply = run_smoke_test(
                        SmokeRequest(
                            provider=pilot_model.provider,
                            model=pilot_model.model,
                            prompt=prompt,
                            temperature=temperature,
                            max_tokens=pilot_model.max_tokens if pilot_model.max_tokens is not None else max_tokens,
                            reasoning_effort=pilot_model.reasoning_effort,
                            reasoning_enabled=pilot_model.reasoning_enabled,
                            anthropic_effort=pilot_model.anthropic_effort,
                            anthropic_thinking=pilot_model.anthropic_thinking,
                            timeout_s=pilot_model.timeout_s,
                        )
                    )
                    parsed = parse_scored_response(reply)
                    rows.append(
                        {
                            "run_id": run_id,
                            "provider": pilot_model.provider,
                            "model_label": pilot_model.label,
                            "model": pilot_model.model,
                            "reasoning_effort": pilot_model.reasoning_effort,
                            "reasoning_enabled": pilot_model.reasoning_enabled,
                            "anthropic_effort": pilot_model.anthropic_effort,
                            "anthropic_thinking": pilot_model.anthropic_thinking,
                            "prompt_style": pilot_model.prompt_style,
                            "timeout_s": pilot_model.timeout_s,
                            "condition": condition,
                            "question_id": question_id,
                            "question_text": question_text,
                            "temperature": temperature,
                            "max_tokens": pilot_model.max_tokens if pilot_model.max_tokens is not None else max_tokens,
                            "prompt": prompt,
                            "error": None,
                            **asdict(parsed),
                        }
                    )
                except Exception as exc:
                    rows.append(
                        {
                            "run_id": run_id,
                            "provider": pilot_model.provider,
                            "model_label": pilot_model.label,
                            "model": pilot_model.model,
                            "reasoning_effort": pilot_model.reasoning_effort,
                            "reasoning_enabled": pilot_model.reasoning_enabled,
                            "anthropic_effort": pilot_model.anthropic_effort,
                            "anthropic_thinking": pilot_model.anthropic_thinking,
                            "prompt_style": pilot_model.prompt_style,
                            "timeout_s": pilot_model.timeout_s,
                            "condition": condition,
                            "question_id": question_id,
                            "question_text": question_text,
                            "temperature": temperature,
                            "max_tokens": pilot_model.max_tokens if pilot_model.max_tokens is not None else max_tokens,
                            "prompt": prompt,
                            "raw_response": "",
                            "score_value": None,
                            "explanation": "",
                            "format_ok": False,
                            "error": str(exc),
                        }
                    )
    return rows


def save_pilot_rows(rows: list[dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = rows[0]["run_id"] if rows else "pilot_empty"
    output_path = output_dir / f"{run_id}.jsonl"
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")
    return output_path
