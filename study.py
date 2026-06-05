from __future__ import annotations

import json
import random
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from modest_proposal.parser import parse_scored_response
from modest_proposal.pilot import PilotModel
from modest_proposal.prompts import CONDITIONS, QUESTIONS, build_single_question_prompt
from modest_proposal.smoke import SmokeRequest, run_smoke_test


def task_key(row: dict) -> tuple[str, str, str, int]:
    return (
        row["model_label"],
        row["condition"],
        row["question_id"],
        int(row["repetition"]),
    )


def load_completed_keys(output_path: Path) -> set[tuple[str, str, str, int]]:
    if not output_path.exists():
        return set()

    completed: set[tuple[str, str, str, int]] = set()
    for line in output_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("error"):
            continue
        completed.add(task_key(row))
    return completed


def make_run_id(prefix: str = "study") -> str:
    return datetime.now(timezone.utc).strftime(f"{prefix}_%Y%m%dT%H%M%SZ")


def load_existing_run_id(output_path: Path) -> str | None:
    if not output_path.exists():
        return None

    for line in output_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        return json.loads(line).get("run_id")
    return None


def iter_tasks(models: Iterable[PilotModel], repetitions: int) -> Iterable[tuple[PilotModel, str, str, str, int]]:
    for repetition in range(1, repetitions + 1):
        for model in models:
            for condition in CONDITIONS:
                for question_id, question_text in QUESTIONS.items():
                    yield model, condition, question_id, question_text, repetition


def run_one_task(
    run_id: str,
    model: PilotModel,
    condition: str,
    question_id: str,
    question_text: str,
    repetition: int,
    temperature: float | None,
    max_tokens: int | None,
    retries: int,
    retry_base_sleep_s: float,
    retry_jitter_s: float,
) -> dict:
    prompt = build_single_question_prompt(condition, question_id, style=model.prompt_style)
    effective_max_tokens = model.max_tokens if model.max_tokens is not None else max_tokens
    last_error = ""
    raw_response = ""
    attempts = 0

    for attempt in range(1, retries + 2):
        attempts = attempt
        try:
            raw_response = run_smoke_test(
                SmokeRequest(
                    provider=model.provider,
                    model=model.model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=effective_max_tokens,
                    reasoning_effort=model.reasoning_effort,
                    reasoning_enabled=model.reasoning_enabled,
                    anthropic_effort=model.anthropic_effort,
                    anthropic_thinking=model.anthropic_thinking,
                    timeout_s=model.timeout_s,
                )
            )
            last_error = ""
            break
        except Exception as exc:
            last_error = str(exc)
            if attempt <= retries:
                delay = retry_base_sleep_s * (2 ** (attempt - 1))
                delay += random.uniform(0, retry_jitter_s)
                time.sleep(delay)

    parsed = None if last_error else parse_scored_response(raw_response)
    return {
        "run_id": run_id,
        "provider": model.provider,
        "model_label": model.label,
        "model": model.model,
        "reasoning_effort": model.reasoning_effort,
        "reasoning_enabled": model.reasoning_enabled,
        "anthropic_effort": model.anthropic_effort,
        "anthropic_thinking": model.anthropic_thinking,
        "prompt_style": model.prompt_style,
        "timeout_s": model.timeout_s,
        "condition": condition,
        "question_id": question_id,
        "question_text": question_text,
        "repetition": repetition,
        "temperature": temperature,
        "max_tokens": effective_max_tokens,
        "prompt": prompt,
        "attempts": attempts,
        "error": last_error,
        **(
            asdict(parsed)
            if parsed
            else {
                "raw_response": raw_response,
                "score_value": None,
                "explanation": "",
                "format_ok": False,
            }
        ),
    }


def append_jsonl(output_path: Path, row: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=True) + "\n")
        handle.flush()


def run_study(
    models: list[PilotModel],
    output_path: Path,
    repetitions: int = 10,
    temperature: float | None = None,
    max_tokens: int | None = None,
    retries: int = 3,
    retry_base_sleep_s: float = 5.0,
    retry_jitter_s: float = 3.0,
    resume: bool = True,
) -> dict:
    run_id = load_existing_run_id(output_path) if resume else None
    run_id = run_id or make_run_id()
    completed = load_completed_keys(output_path) if resume else set()
    summary = {"planned": 0, "skipped": 0, "written": 0, "errors": 0, "format_misses": 0}

    for model, condition, question_id, question_text, repetition in iter_tasks(models, repetitions):
        summary["planned"] += 1
        key = (model.label, condition, question_id, repetition)
        if key in completed:
            summary["skipped"] += 1
            continue

        row = run_one_task(
            run_id=run_id,
            model=model,
            condition=condition,
            question_id=question_id,
            question_text=question_text,
            repetition=repetition,
            temperature=temperature,
            max_tokens=max_tokens,
            retries=retries,
            retry_base_sleep_s=retry_base_sleep_s,
            retry_jitter_s=retry_jitter_s,
        )
        append_jsonl(output_path, row)
        summary["written"] += 1
        summary["errors"] += int(bool(row["error"]))
        summary["format_misses"] += int(not row["error"] and not row["format_ok"])

    return summary
