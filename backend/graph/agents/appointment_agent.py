"""
Appointment Agent
"""

# from backend.graph.workflows.appointment_booking import state
from graph.state import HospitalState

from graph.prompts.appointment_prompt import (
    APPOINTMENT_PROMPT
)

from graph.models.appointment import (
    AppointmentDecision
)

from graph.utils.parser import (
    ask_llm
)

from graph.registry.appointment_registry import (
    FUNCTIONS
)
from graph.utils.date_time import (
    make_datetime,
)

from core.ai_permissions import authorize_function


def appointment_agent(
    state: HospitalState
) -> HospitalState:

    try:

        history = state.get("messages", [])[-10:]

        history_text = "\n".join(
            f"{m.type}: {m.content}"
            for m in history
        )

        # ==========================================
        # Build Prompt
        # ==========================================

        prompt = f"""
{APPOINTMENT_PROMPT}

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

            AppointmentDecision

        )

        print("=" * 60)
        print("Appointment Decision")
        print(decision)
        print("=" * 60)

        function_name = decision.function

        if not authorize_function(
            state,
            function_name,
        ):
            return state
        
        payload = decision.payload or {}

        # ==========================================
        # Function Exists?
        # ==========================================

        if function_name not in FUNCTIONS:

            raise Exception(
                f"Unknown Appointment Function : {function_name}"
            )

        function = FUNCTIONS[
            function_name
        ]

        # ==========================================
        # CHECK AVAILABILITY
        # ==========================================

        if function_name == "check_availability":

            date_text = payload.get("date")
            start_time = payload.get("start_time")
            end_time = payload.get("end_time")

            if not start_time or not end_time:
                state["error"] = "Start time and end time are required."
                return state

            start = make_datetime(
                date_text,
                start_time
            )

            end = make_datetime(
                date_text,
                end_time
            )

            payload["start"] = start
            payload["end"] = end

            # Remove temporary extraction fields
            payload.pop("date", None)
            payload.pop("start_time", None)
            payload.pop("end_time", None)

            result = function(**payload)

            state["result"] = result

            return state

        # ==========================================
        # APPOINTMENT DETAILS
        # ==========================================

        elif function_name == "appointment_details":

            result = function(

                payload["appointment_id"]

            )

        # ==========================================
        # PATIENT APPOINTMENTS
        # ==========================================

        elif function_name == "patient_appointments":

            result = function(

                payload["patient_id"]

            )

        # ==========================================
        # PRACTITIONER APPOINTMENTS
        # ==========================================

        elif function_name == "practitioner_appointments":

            result = function(

                payload["practitioner_id"]

            )
            print(result);
        # ==========================================
        # CANCEL APPOINTMENT
        # ==========================================

        elif function_name == "cancel_appointment":

            result = function(

                payload["appointment_id"]

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