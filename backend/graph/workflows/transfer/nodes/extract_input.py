"""
Extract Transfer Input
"""

from graph.workflows.transfer.state import (
    TransferState
)

from graph.workflows.transfer.prompts.transfer_prompt import (
    TRANSFER_PROMPT
)

from graph.workflows.transfer.models.transfer_input import (
    TransferInput
)

from graph.utils.parser import ask_llm


def extract_input(
    state: TransferState
) -> TransferState:

    prompt = f"""
{TRANSFER_PROMPT}

User Query:

{state["user_query"]}
"""

    transfer = ask_llm(
        prompt,
        TransferInput
    )

    state["workflow_data"] = transfer.model_dump()

    return state