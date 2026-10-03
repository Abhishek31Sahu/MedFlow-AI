"""
Patient Agent
"""

from graph.state import HospitalState

from graph.prompts.patient_prompt import (
    PATIENT_PROMPT
)

from graph.models.patient import (
    PatientDecision
)

from graph.utils.parser import (
    ask_llm
)

from graph.registry.patient_registry import (
    FUNCTIONS
)

from core.ai_permissions import authorize_function


def patient_agent(
    state: HospitalState
) -> HospitalState:

    try:
        history = state.get("messages", [])[-10:]
        history_text = "\n".join(f"{m.type}: {m.content}" for m in history)
        # ==========================================
        # Build Prompt
        # ==========================================

        prompt = f"""
{PATIENT_PROMPT}

Conversation so far:
{history_text}

User Query:

{state["user_query"]}
"""

        # ==========================================
        # Ask LLM
        # ==========================================

        decision = ask_llm(

            prompt,

            PatientDecision

        )

        print("=" * 60)
        print("Patient Decision")
        print(decision)
        print("=" * 60)

        function_name = decision.function

        if not authorize_function(
            state,
            function_name,
        ):
            return state
        payload = decision.payload

        # ==========================================
        # Function Exists?
        # ==========================================

        if function_name not in FUNCTIONS:

            raise Exception(
                f"Unknown Patient Function : {function_name}"
            )

        function = FUNCTIONS[
            function_name
        ]

        # ==========================================
        # ADD PATIENT
        # ==========================================

        if function_name == "add_patient":

            result = function(
                **payload
            )

        # ==========================================
        # GET PATIENT
        # ==========================================

        elif function_name == "patient_details":

            result = function(

                payload["patient_id"]

            )

        # ==========================================
        # UPDATE PATIENT
        # ==========================================

        elif function_name == "edit_patient":

            result = function(

                patient_id=payload["patient_id"],

                first_name=payload.get("first_name"),

                last_name=payload.get("last_name"),

                gender=payload.get("gender"),

                birth_date=payload.get("birth_date")

            )

        # ==========================================
        # DELETE PATIENT
        # ==========================================

        elif function_name == "remove_patient":

            result = function(

                payload["patient_id"]

            )

        # ==========================================
        # UNKNOWN FUNCTION
        # ==========================================

        else:

            raise Exception(
                f"Unsupported Function : {function_name}"
            )

        # ==========================================
        # SAVE RESULT
        # ==========================================

        state["result"] = result

        return state

    except Exception as e:

        state["error"] = str(e)

        return state