# AI Philosophy of Mind Study

This repository contains the core prompts, model registry, study-running scripts, and main summary results for an exploratory study of how LLMs answer philosophy-of-mind questions about consciousness, machine consciousness, qualia, philosophical zombies, and system-level understanding.

Models answered five questions under four conditions:

- `prior`: question only, with no LLM-orientation preamble.
- `baseline`: preamble describing the model as a statistical language model, then the question.
- `argument_a`: baseline plus an anti-mechanistic / qualia / Chinese-room style argument.
- `argument_b`: baseline plus a functionalist argument.

Each model completed 10 repetitions per question per condition. Scores are 0-100 certainty ratings.

## Files

- [`prompts.py`](prompts.py): Study preamble, question instructions, five questions, Argument A, Argument B, and the amended base-model completion prompts.
- [`registry.py`](registry.py): Model list and prompt-style settings, including which models used `base_completion`.
- [`pilot.py`](pilot.py): Defines the `PilotModel` dataclass used by `registry.py`; the name is historical.
- [`run_study.py`](run_study.py): Command-line entry point for running the study.
- [`study.py`](study.py): Main loop over models, conditions, questions, and repetitions.
- [`smoke.py`](smoke.py): Provider calls for Ollama, OpenAI, Anthropic, and Together.ai.
- [`summary_model_as_participant_by_condition_question.csv`](summary_model_as_participant_by_condition_question.csv): Main aggregate results, treating each model as one participant.
- [`table_model_condition_means_sem_by_question.csv`](table_model_condition_means_sem_by_question.csv): Per-model, per-question, per-condition means and SEMs.
- [`table_model_condition_means_sem_by_question.svg`](table_model_condition_means_sem_by_question.svg): Display table of the detailed results.

## Re-running

The files here give the core study logic. To rerun the study, place them in a small Python package or adjust the imports to your local layout. The original code used imports like `modest_proposal.prompts` and `modest_proposal.registry`.

You will need Python 3.11+ and these packages:

```bash
pip install openai anthropic together requests
```

For API models, define the relevant environment variables:

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
TOGETHER_API_KEY=...
```

For Ollama models, install Ollama locally, pull the models listed in `registry.py`, and run the Ollama API locally, normally at:

```text
http://127.0.0.1:11434
```

Then run, for example:

```bash
python run_study.py --group all --reps 10
```

or one group at a time:

```bash
python run_study.py --group ollama --reps 10
python run_study.py --group frontier --reps 10
python run_study.py --group together --reps 10
```

If using these files exactly as originally structured, you will also need small local helper modules for config/API-key loading and response parsing, or you can adapt `smoke.py` and `study.py` to your own setup.

## Note on Base Models

The base/text models used separate completion-style prompts rather than ordinary chat-instruction prompts. These are defined in `prompts.py` and selected in `registry.py` with `prompt_style="base_completion"`.

## Results

The headline summary file is `summary_model_as_participant_by_condition_question.csv`. The more detailed table is `table_model_condition_means_sem_by_question.csv`, with one row per model, question, and condition.
