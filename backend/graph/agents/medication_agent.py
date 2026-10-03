"""
Medication Agent
"""
from graph.state import HospitalState

from graph.prompts.medication_prompt import (
    MEDICATION_PROMPT
)

from graph.models.medication import (
    MedicationDecision
)

from graph.utils.parser import (
    ask_llm
)

from graph.registry.medication_registry import (
    FUNCTIONS
)
from core.ai_permissions import authorize_function

def medication_agent(
    state: HospitalState
) -> HospitalState:

    try:
        history = state.get("messages", [])[-10:]
        history_text = "\n".join(f"{m.type}: {m.content}" for m in history)
                # ==========================================
                # Build Prompt
                # ==========================================
        
        prompt = f"""
        {MEDICATION_PROMPT}
        
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

            MedicationDecision

        )

        print("=" * 60)
        print("Medication Decision")
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
                f"Unknown Medication Function : {function_name}"
            )

        function = FUNCTIONS[
            function_name
        ]

        # ==========================================
        # ADD MEDICATION
        # ==========================================

        if function_name == "add_medication":

            payload["practitioner_id"] = (
                state["practitioner_id"]
            )

            result = function(
                **payload
            )

        # ==========================================
        # STOP MEDICATION
        # ==========================================

        elif function_name == "discontinue_medication":

            result = function(

                patient_id=payload["patient_id"],

                medicine_name=payload["medicine_name"]

            )

        # ==========================================
        # CHANGE DOSAGE
        # ==========================================

        elif function_name == "change_dosage":

            result = function(

                patient_id=payload["patient_id"],

                medicine_name=payload["medicine_name"],

                dosage=payload["dosage"],

                frequency=payload["frequency"]

            )

        # ==========================================
        # LIST ACTIVE MEDICATIONS
        # ==========================================

        elif function_name == "list_active_medications":

            result = function(

                payload["patient_id"]

            )

        # ==========================================
        # MEDICATION HISTORY
        # ==========================================

        elif function_name == "medication_history":

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
    
    
    
# ✅ services/aiService.js

# ✅ hook/useChat.js

# ✅ components/ui/MessageBubble.jsx

# ✅ components/ui/MessageList.jsx

# ✅ components/forms/ChatInput.jsx

# ✅ components/common/ChatHeader.jsx

# ✅ components/common/EmptyChat.jsx

# ✅ components/ui/TypingIndicator.jsx

# ✅ pages/AI/AIChat.jsx