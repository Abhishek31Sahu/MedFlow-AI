"""
Extract Discharge Input
"""

from graph.workflows.discharge.state import (
    DischargeState
)

from graph.workflows.discharge.prompts.discharge_prompt import (
    DISCHARGE_PROMPT
)

from graph.workflows.discharge.models.discharge_input import (
    DischargeInput
)

from graph.utils.parser import ask_llm


def extract_input(
    state: DischargeState
) -> DischargeState:

    prompt = f"""
{DISCHARGE_PROMPT}

User Query:

{state["user_query"]}
"""

    discharge = ask_llm(
        prompt,
        DischargeInput
    )

    state["workflow_data"] = discharge.model_dump()
    print("check input")
    print(state["workflow_data"])
    return state