"""
Patient Search Agent

Responsible for resolving a patient before
executing any workflow.

This agent DOES NOT use an LLM.
"""

from graph.state import HospitalState

from services.patient_search_service import (
    resolve_patient
)
from graph.models.patient_search import (
    PatientSearchResult,
    PatientSearchInput
    
)
from graph.prompts.patient_search_prompt import (
    PATIENT_SEARCH_PROMPT
)

from graph.utils.parser import (
    ask_llm
)

def patient_search_agent(
    state: HospitalState
) -> HospitalState:

    try:

        history = state.get("messages", [])[-10:]
        history_text = "\n".join(f"{m.type}: {m.content}" for m in history)

                
        prompt = f"""
                {PATIENT_SEARCH_PROMPT}
                
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
        
                    PatientSearchInput
        
                )
        
        patient_name = decision.name

        result = resolve_patient(
            patient_name
        )

        status = result["status"]

        # ------------------------------------------
        # Patient Not Found
        # ------------------------------------------

        if status == "not_found":

            state["error"] = result["message"]

            state["workflow_status"] = (
                "need_patient_registration"
            )

            return state

        # ------------------------------------------
        # Multiple Patients
        # ------------------------------------------

        if status == "multiple":

            state["result"]= result["patients"]

            return state

        # ------------------------------------------
        # Successfully Resolved
        # ------------------------------------------

        state["result"]= result["patient"]

        return state

    except Exception as e:

        state["error"] = str(e)

        return state