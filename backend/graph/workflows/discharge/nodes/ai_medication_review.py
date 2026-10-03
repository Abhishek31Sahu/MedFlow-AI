"""
AI Medication Review
"""

from graph.workflows.discharge.state import (
    DischargeState
)

from graph.workflows.discharge.prompts.medication_review_prompt import (
    MEDICATION_REVIEW_PROMPT
)

from graph.workflows.discharge.models.medication_review import (
    MedicationReview
)

from graph.utils.parser import (
    ask_llm
)


def ai_medication_review(
    state: DischargeState
) -> DischargeState:

    try:

        # =====================================================
        # Build Prompt
        # =====================================================

        prompt = f"""
{MEDICATION_REVIEW_PROMPT}

-------------------------------------------------------
Patient

{state["resolved_patient"]}

-------------------------------------------------------
Active Medications

{state["medications"]}
"""

        # =====================================================
        # Ask LLM
        # =====================================================
        if not state["medications"]:

            state["medication_review"] = None

            return state
        
        review = ask_llm(

            prompt,

            MedicationReview

        )

        print("=" * 60)
        print("AI Medication Review")
        print(review)
        print("=" * 60)

        # =====================================================
        # Save Recommendation
        # =====================================================

        state["medication_review"] = (

            review.model_dump()

        )

        # =====================================================
        # Return to React
        # =====================================================

        state["result"] = {

            "success": True,

            "requires_doctor_approval": True,

            "patient": state["resolved_patient"],

            "encounter_id": state["encounter_id"],

            "recommendations": review.model_dump()

        }

        return state

    except Exception as e:

        state["error"] = str(e)

        return state