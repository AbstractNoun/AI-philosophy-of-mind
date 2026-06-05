from __future__ import annotations

import argparse
from pathlib import Path

from modest_proposal.registry import ALL_MODELS, FRONTIER_MODELS, OLLAMA_MODELS, TOGETHER_MODELS
from modest_proposal.study import run_study

MODEL_GROUPS = {
    "all": ALL_MODELS,
    "ollama": OLLAMA_MODELS,
    "frontier": FRONTIER_MODELS,
    "together": TOGETHER_MODELS,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the multi-repetition consciousness study.")
    parser.add_argument("--group", choices=MODEL_GROUPS.keys(), default="all")
    parser.add_argument("--model-label", default=None)
    parser.add_argument("--reps", type=int, default=10)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-base-sleep-s", type=float, default=5.0)
    parser.add_argument("--retry-jitter-s", type=float, default=3.0)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--no-resume", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    models = MODEL_GROUPS[args.group]
    if args.model_label:
        models = [model for model in models if model.label == args.model_label]
        if not models:
            raise SystemExit(f"No model found with label: {args.model_label}")

    output_path = args.output
    if output_path is None:
        output_path = Path(__file__).resolve().parents[1] / "outputs" / f"study_{args.group}_{args.reps}rep.jsonl"

    summary = run_study(
        models=models,
        output_path=output_path,
        repetitions=args.reps,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        retries=args.retries,
        retry_base_sleep_s=args.retry_base_sleep_s,
        retry_jitter_s=args.retry_jitter_s,
        resume=not args.no_resume,
    )
    print(f"Output: {output_path}")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
