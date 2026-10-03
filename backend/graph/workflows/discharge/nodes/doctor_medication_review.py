from langgraph.types import interrupt
from graph.workflows.discharge.models.doctor_decision import DoctorDecision


def doctor_medication_review(state):

    if state.get("medication_review") is None:
        return state

    # Don't interrupt again if decisions are already present
    if state.get("doctor_decision"):
        return state

    decision = interrupt({
        "type": "MEDICATION_REVIEW",
        "message": "Review AI medication recommendations.",
        "patient": state.get("resolved_patient"),
        "medications": state.get("medications", []),
        "ai_review": state.get("medication_review"),
    })

    print("RESUMED VALUE:", repr(decision))
    print("RESUMED TYPE:", type(decision))

    if not isinstance(decision, dict):
        raise ValueError(
            f"Expected doctor decision dict, got: {type(decision).__name__}"
        )

    raw_decisions = decision.get("doctor_decision")

    if not isinstance(raw_decisions, list):
        raise ValueError(
            f"doctor_decision must be a list, got: {type(raw_decisions).__name__}"
        )

    state["doctor_decision"] = [
        DoctorDecision.model_validate(item)
        for item in raw_decisions
    ]

    return state