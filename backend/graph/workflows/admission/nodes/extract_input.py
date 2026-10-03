"""
Extract Admission Input
"""

from graph.workflows.admission.state import (
    AdmissionState
)

from graph.workflows.admission.prompts.admission_prompt import (
    ADMISSION_PROMPT
)

from graph.workflows.admission.models.admission_input import (
    AdmissionInput
)

from graph.utils.parser import (
    ask_llm
)
from graph.workflows.discharge import state


def extract_input(
    state: AdmissionState
) -> AdmissionState:
    history = state.get("messages", [])[-10:]
    history_text = "\n".join(f"{m.type}: {m.content}" for m in history)

    prompt = f"""
{ADMISSION_PROMPT}

Conversation so far:
{history_text}

User Query:

{state["user_query"]}
"""

    admission = ask_llm(

        prompt,

        AdmissionInput

    )
    
    

    state["workflow_data"] = (

        admission.model_dump()

    )
    print("=" * 60)
    print(state,"hello")
    print("=" * 60)

    return state