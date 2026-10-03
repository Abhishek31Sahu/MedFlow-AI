from langchain_core.messages import HumanMessage

from graph.workflows.doctor_lab_order.state import DoctorLabOrderState
from graph.workflows.doctor_lab_order.prompts.extract_lab_order_prompt import (
    EXTRACT_LAB_ORDER_PROMPT,
)
from graph.workflows.doctor_lab_order.models.extracted_lab_order import (
    ExtractedLabOrder,
)

from graph.utils.llm import llm


async def extract_lab_order(
    state: DoctorLabOrderState,
) -> DoctorLabOrderState:
    """
    Extract laboratory order information from the doctor's query.
    """

    structured_llm = llm.with_structured_output(
        ExtractedLabOrder
    )
    
    history = state.get("messages", [])[-10:]
    history_text = "\n".join(f"{m.type}: {m.content}" for m in history)

    response = await structured_llm.ainvoke(
        [
            HumanMessage(
                content=EXTRACT_LAB_ORDER_PROMPT.format(
                    query=state["user_query"],
                    history=history_text,
                )
            )
        ]
    )
    
    

    workflow_data = {

        "patient_name": response.patient_name,

        "tests": [
            {
                "code": test.code,
                "name": test.name,
            }
            for test in response.tests
        ],

        "priority": response.priority or "ROUTINE",

        "clinical_note": response.clinical_note,

    }

    return {
        **state,
        "workflow_data": workflow_data,
        "current_step": "LAB_ORDER_EXTRACTED",
    }