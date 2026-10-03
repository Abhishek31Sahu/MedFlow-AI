"""
Observation Agent
"""

from graph.state import HospitalState

from graph.prompts.observation_prompt import (
    OBSERVATION_PROMPT
)

from graph.models.observation import (
    ObservationDecision
)

from graph.utils.parser import (
    ask_llm
)

from graph.registry.observation_registry import (
    FUNCTIONS
)
from core.ai_permissions import authorize_function

def observation_agent(
    state: HospitalState
) -> HospitalState:

    try:
        history = state.get("messages", [])[-10:]
        history_text = "\n".join(f"{m.type}: {m.content}" for m in history)
            # ==========================================
            # Build Prompt
            # ==========================================
    
        prompt = f"""
    {OBSERVATION_PROMPT}
    
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

            ObservationDecision

        )

        print("=" * 60)
        print("Observation Decision")
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
                f"Unknown Observation Function : {function_name}"
            )

        function = FUNCTIONS[
            function_name
        ]

        # ==========================================
        # ADD OBSERVATION
        # ==========================================

        if function_name == "add_observation":

            payload["practitioner_id"] = (
                state["practitioner_id"]
            )

            result = function(
                **payload
            )

        # ==========================================
        # GET OBSERVATION
        # ==========================================

        elif function_name == "get_observation":

            result = function(
                payload["observation_id"]
            )

        # ==========================================
        # LIST PATIENT OBSERVATIONS
        # ==========================================

        elif function_name == "list_patient_observations":

            result = function(
                payload["patient_id"]
            )

        # ==========================================
        # SEARCH TEST
        # ==========================================

        elif function_name == "search_test":

            result = function(

                patient_id=payload["patient_id"],

                test_name=payload["test_name"]

            )

        # ==========================================
        # LATEST TEST RESULT
        # ==========================================

        elif function_name == "latest_test_result":

            result = function(

                patient_id=payload["patient_id"],

                test_name=payload["test_name"]

            )

        # ==========================================
        # UPDATE OBSERVATION VALUE
        # ==========================================

        elif function_name == "change_observation_value":

            result = function(

                observation_id=payload["observation_id"],

                value=payload["value"]

            )

        # ==========================================
        # DELETE OBSERVATION
        # ==========================================

        elif function_name == "remove_observation":

            result = function(
                payload["observation_id"]
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