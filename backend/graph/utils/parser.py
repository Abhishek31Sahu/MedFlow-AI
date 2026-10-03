"""
LLM Parser
"""

from pydantic import BaseModel
from graph.utils.llm import llm


def ask_llm(
    prompt: str,
    response_model: type[BaseModel],
):
    structured_llm = llm.with_structured_output(
        response_model,
        method="function_calling"
    )

    response = structured_llm.invoke(prompt)

    return response