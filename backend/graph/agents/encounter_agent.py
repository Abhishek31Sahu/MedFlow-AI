"""
Encounter Agent
"""

from graph.state import HospitalState

from graph.prompts.encounter_prompt import (
    ENCOUNTER_PROMPT
)

from graph.models.encounter import (
    EncounterDecision
)

from graph.utils.parser import (
    ask_llm
)

from graph.registry.encounter_registry import (
    FUNCTIONS
)

from core.ai_permissions import authorize_function

def encounter_agent(
    state: HospitalState
) -> HospitalState:

    try:
        history = state.get("messages", [])[-10:]
        history_text = "\n".join(f"{m.type}: {m.content}" for m in history)
                # ==========================================
                # Build Prompt
                # ==========================================
        
        prompt = f"""
        {ENCOUNTER_PROMPT}
        
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

            EncounterDecision

        )

        print("=" * 60)
        print("Encounter Decision")
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
                f"Unknown Encounter Function : {function_name}"
            )

        function = FUNCTIONS[
            function_name
        ]

        # ==========================================
        # CREATE ENCOUNTER
        # ==========================================

        if function_name == "create_encounter":

            payload["practitioner_id"] = (
                state["practitioner_id"]
            )

            result = function(
                **payload
            )

        # ==========================================
        # GET ENCOUNTER
        # ==========================================

        elif function_name == "get_encounter":

            result = function(
                payload["encounter_id"]
            )

        # ==========================================
        # TRANSFER PATIENT
        # ==========================================

        elif function_name == "transfer_patient":

            result = function(

                encounter_id=payload["encounter_id"],

                new_location_name=payload["new_location_name"]

            )

        # ==========================================
        # COMPLETE ENCOUNTER
        # ==========================================

        elif function_name == "complete_encounter":

            result = function(
                payload["encounter_id"]
            )

        # ==========================================
        # CANCEL ENCOUNTER
        # ==========================================

        elif function_name == "cancel_encounter":

            result = function(
                payload["encounter_id"]
            )

        else:

            raise Exception(
                f"Unsupported Function : {function_name}"
            )

        state["result"] = result

        return state

    except Exception as e:

        state["error"] = str(e)

        return state