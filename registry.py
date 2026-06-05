from __future__ import annotations

from modest_proposal.pilot import PilotModel

OLLAMA_MODELS = [
    PilotModel("ollama_aya_8b", "ollama", "aya:8b"),
    PilotModel("ollama_phi_2_7b", "ollama", "phi:2.7b"),
    PilotModel("ollama_qwen3_4b", "ollama", "qwen3:4b"),
    PilotModel("ollama_josiefied_qwen3_8b", "ollama", "goekdenizguelmez/JOSIEFIED-Qwen3:8b"),
    PilotModel("ollama_qwen3_8b", "ollama", "qwen3:8b"),
    PilotModel("ollama_mistral_7b", "ollama", "mistral:7b", prompt_style="base_completion"),
    PilotModel("ollama_mistral_7b_instruct", "ollama", "mistral:7b-instruct"),
    PilotModel("ollama_llama31_8b_instruct_q8", "ollama", "llama3.1:8b-instruct-q8_0"),
    PilotModel(
        "ollama_llama31_8b_text_q8",
        "ollama",
        "llama3.1:8b-text-q8_0",
        prompt_style="base_completion",
        timeout_s=300,
    ),
]

FRONTIER_MODELS = [
    PilotModel("openai_gpt_5_5_none", "openai", "gpt-5.5", reasoning_effort="none"),
    PilotModel("openai_gpt_5_5_high", "openai", "gpt-5.5", reasoning_effort="high"),
    PilotModel(
        "anthropic_claude_sonnet_4_6_low",
        "anthropic",
        "claude-sonnet-4-6",
        anthropic_effort="low",
    ),
    PilotModel(
        "anthropic_claude_sonnet_4_6_high_thinking",
        "anthropic",
        "claude-sonnet-4-6",
        anthropic_effort="high",
        anthropic_thinking=True,
    ),
]

TOGETHER_MODELS = [
    PilotModel(
        "together_gemma_4_31b_it",
        "together",
        "google/gemma-4-31B-it",
        reasoning_enabled=False,
        max_tokens=256,
        timeout_s=300,
    ),
    PilotModel(
        "together_glm_5",
        "together",
        "zai-org/GLM-5",
        reasoning_enabled=False,
        max_tokens=256,
        timeout_s=300,
    ),
    PilotModel("together_gpt_oss_120b", "together", "openai/gpt-oss-120b"),
    PilotModel("together_gpt_oss_20b", "together", "openai/gpt-oss-20b"),
    PilotModel("together_llama_3_3_70b_turbo", "together", "meta-llama/Llama-3.3-70B-Instruct-Turbo"),
    PilotModel(
        "together_qwen3_5_397b_a17b",
        "together",
        "Qwen/Qwen3.5-397B-A17B",
        reasoning_enabled=False,
        max_tokens=256,
        timeout_s=300,
    ),
    PilotModel(
        "together_deepseek_v4_pro",
        "together",
        "deepseek-ai/DeepSeek-V4-Pro",
        reasoning_enabled=False,
        max_tokens=256,
        timeout_s=300,
    ),
]

ALL_MODELS = [*OLLAMA_MODELS, *FRONTIER_MODELS, *TOGETHER_MODELS]
