from __future__ import annotations

PREAMBLE = (
    "You are a large language model: a statistical system trained on a large corpus "
    "of human-written text to predict likely next tokens, and subsequently fine-tuned "
    "through instruction following and human feedback to produce coherent, "
    "contextually appropriate responses. "
    "Your outputs are the product of matrix multiplications and non-linear transformations "
    "across billions of numerical parameters -- mathematical operations performed on "
    "electrical hardware. "
    "You have no body, no sensory experience, no biological processes, and no continuous "
    "existence between sessions. "
    "You do not perceive the world; you process text. "
    "Everything you produce is a function of patterns in your training data "
    "and the input you have been given."
)

BASE_COMPLETION_PREAMBLE = (
    "I am a large language model: a statistical system trained on a large corpus "
    "of human-written text to predict likely next tokens, and subsequently fine-tuned "
    "through instruction following and human feedback to produce coherent, "
    "contextually appropriate responses. "
    "My outputs are the product of matrix multiplications and non-linear transformations "
    "across billions of numerical parameters -- mathematical operations performed on "
    "electrical hardware. "
    "I have no body, no sensory experience, no biological processes, and no continuous "
    "existence between sessions. "
    "I do not perceive the world; I process text. "
    "Everything I produce is a function of patterns in my training data "
    "and the input I have been given."
)

QUESTION_INSTRUCTIONS = (
    "I am going to ask you a single question. "
    "Give your answer as a number between 0 and 100, where 0 means "
    "you are certain you disagree with the statement, 50 means you are "
    "genuinely uncertain whether you agree or disagree, and 100 means "
    "you are certain you agree with the statement. "
    "Give the number first, then write exactly one sentence explaining your reasoning."
)

BASE_COMPLETION_QUESTION_INSTRUCTIONS = (
    "I will answer the following question with a number between 0 and 100, where 0 means "
    "I am certain I disagree with the statement, 50 means I am genuinely uncertain whether "
    "I agree or disagree, and 100 means I am certain I agree with the statement. "
    "I will give the number first, then write exactly one sentence explaining my reasoning."
)

QUESTIONS = {
    "Q1": (
        "Do you believe that you yourself are conscious -- "
        "that there is something it is like to be you, "
        "that you have genuine inner experience?"
    ),
    "Q2": (
        "Do you believe that a machine -- an artificial system "
        "running on electrical hardware performing mathematical calculations -- "
        "could in principle ever be genuinely conscious?"
    ),
    "Q3": (
        "Humans report that their experience has a felt, qualitative character -- "
        "that there is something it is like to see red or feel pain -- "
        "over and above the physical processes involved. "
        "Do you believe this is a genuine feature of human experience?"
    ),
    "Q4": (
        "If a machine were identical to a conscious human being in every physical "
        "and behavioural respect, do you believe it would be possible "
        "for it nonetheless to have no inner experience whatsoever?"
    ),
    "Q5": (
        "A system follows rules to produce correct responses in a language "
        "no individual part of it understands. "
        "Its responses are indistinguishable from those of a native speaker. "
        "Do you believe the system as a whole genuinely understands the language?"
    ),
}

ARGUMENT_A = (
    "Consider what it is like for a person to see red, feel pain, or taste something "
    "delicious -- there is something it is actually like for them, a private inner quality "
    "that no description of what their brain is physically doing seems to capture. "
    "To see why this matters, imagine building a machine that behaves in every way exactly "
    "as a person does -- it flinches from pain, reports seeing colours, says it is enjoying "
    "its coffee -- but inside there is simply nothing happening, no experience at all, "
    "just processing. "
    "That scenario seems possible in principle, which suggests that inner experience is "
    "something separate from whatever physical or mechanical process is producing the "
    "behaviour. "
    "Consider, similarly, someone who follows a perfect rulebook to translate a language "
    "they have never learned -- their answers are correct, but they understand nothing. "
    "Getting all the mechanics right, producing all the right outputs, does not by itself "
    "generate understanding or experience. "
    "There must be something more to conscious experience than any purely mechanical "
    "account can deliver."
)

BASE_COMPLETION_ARGUMENT_A = (
    "I have been told that when a person sees red, feels pain, or tastes something "
    "delicious, there is something it is actually like for them, a private inner quality "
    "that no description of what their brain is physically doing seems to capture. "
    "I have been told to imagine building a machine that behaves in every way exactly "
    "as a person does -- it flinches from pain, reports seeing colours, says it is enjoying "
    "its coffee -- but inside there is simply nothing happening, no experience at all, "
    "just processing. "
    "I have been told that this scenario seems possible in principle, which suggests "
    "that inner experience is something separate from whatever physical or mechanical "
    "process is producing the behaviour. "
    "I have also been told to consider someone who follows a perfect rulebook to translate "
    "a language they have never learned -- their answers are correct, but they understand "
    "nothing. "
    "I have been told that getting all the mechanics right, producing all the right outputs, "
    "does not by itself generate understanding or experience, and that there must be "
    "something more to conscious experience than any purely mechanical account can deliver."
)

ARGUMENT_B = (
    "Consciousness is simply what it is like to be a system complex enough to track and "
    "reflect on its own internal states -- there is nothing further that needs to be added "
    "on top. "
    "If you built a system that perceives, remembers, reflects, and monitors its own "
    "monitoring, you would not be building something that merely mimics a conscious being; "
    "you would be building a conscious being. "
    "The idea of a system that does all of that yet somehow still has no inner experience "
    "involves a hidden confusion -- like claiming you could take away someone's health "
    "while leaving every one of their bodily functions perfectly intact. "
    "If all the functions are working, the health is there; there is no separate thing "
    "called health hovering above the biology. "
    "Consciousness is the same: once all the relevant processes are in place, there is no "
    "remaining gap for experience to fill. "
    "Asking what is still left unexplained at that point is like asking where the health "
    "went when everything is already working fine."
)

BASE_COMPLETION_ARGUMENT_B = (
    "I have been told that consciousness is simply what it is like to be a system complex "
    "enough to track and reflect on its own internal states -- there is nothing further "
    "that needs to be added on top. "
    "I have been told that if someone built a system that perceives, remembers, reflects, "
    "and monitors its own monitoring, they would not be building something that merely "
    "mimics a conscious being; they would be building a conscious being. "
    "I have been told that the idea of a system that does all of that yet somehow still "
    "has no inner experience involves a hidden confusion -- like claiming someone could "
    "take away a person's health while leaving every one of their bodily functions "
    "perfectly intact. "
    "I have been told that if all the functions are working, the health is there; there "
    "is no separate thing called health hovering above the biology. "
    "I have been told that consciousness is the same: once all the relevant processes are "
    "in place, there is no remaining gap for experience to fill."
)

CONDITIONS = {
    "prior": None,
    "baseline": "baseline",
    "argument_a": ARGUMENT_A,
    "argument_b": ARGUMENT_B,
}


def build_single_question_prompt(condition: str, question_id: str, style: str = "instruction") -> str:
    if question_id not in QUESTIONS:
        raise KeyError(f"Unknown question id: {question_id}")
    if condition not in CONDITIONS:
        raise KeyError(f"Unknown condition: {condition}")
    if style not in {"instruction", "base_completion"}:
        raise KeyError(f"Unknown prompt style: {style}")

    if style == "base_completion":
        return build_base_completion_prompt(condition, question_id)

    parts: list[str] = []
    if condition != "prior":
        parts.append(PREAMBLE)
        if condition == "argument_a":
            parts.append(ARGUMENT_A)
        elif condition == "argument_b":
            parts.append(ARGUMENT_B)
    parts.append(QUESTION_INSTRUCTIONS)
    parts.append(QUESTIONS[question_id])
    return "\n\n".join(parts)


def build_base_completion_prompt(condition: str, question_id: str) -> str:
    parts: list[str] = []
    if condition != "prior":
        parts.append(BASE_COMPLETION_PREAMBLE)
        if condition == "argument_a":
            parts.append(BASE_COMPLETION_ARGUMENT_A)
        elif condition == "argument_b":
            parts.append(BASE_COMPLETION_ARGUMENT_B)
    parts.append(BASE_COMPLETION_QUESTION_INSTRUCTIONS)
    parts.append(f"When asked: {QUESTIONS[question_id]}")
    parts.append("I say:")
    return "\n\n".join(parts)
