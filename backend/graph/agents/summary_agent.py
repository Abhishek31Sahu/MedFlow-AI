"""
Summary Agent
"""

from graph.state import HospitalState

from graph.prompts.summary_prompt import (
    SUMMARY_PROMPT
)

from graph.models.summary import (
    SummaryDecision
)

from graph.utils.parser import (
    ask_llm
)

from graph.registry.summary_registry import (
    FUNCTIONS
)


from core.ai_permissions import authorize_function


def summary_agent(
    state: HospitalState
) -> HospitalState:

    try:
        history = state.get("messages", [])[-10:]
        history_text = "\n".join(f"{m.type}: {m.content}" for m in history)
            # ==========================================
            # Build Prompt
            # ==========================================
    
        prompt = f"""
    {SUMMARY_PROMPT}
    
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

            SummaryDecision

        )

        print("=" * 60)
        print("Summary Decision")
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
                f"Unknown Summary Function : {function_name}"
            )

        function = FUNCTIONS[
            function_name
        ]

        # ==========================================
        # PATIENT SUMMARY
        # ==========================================

        if function_name == "patient_summary":

            result = function(

                payload["patient_id"]

            )

        else:

            raise Exception(
                f"Unsupported Function : {function_name}"
            )

        # ==========================================
        # Save Result
        # ==========================================

        state["result"] = result

        return state

    except Exception as e:

        state["error"] = str(e)
        print(state["error"])
        return state