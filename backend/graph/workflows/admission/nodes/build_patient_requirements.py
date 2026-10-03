from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")
from graph.workflows.admission.prompts.patient_requirement import (
    SYSTEM_PROMPT
)
from graph.workflows.admission.models.patient_requirement import (
    PatientRequirements
)
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
)

def build_patient_requirements(state):
    
    decider = llm.with_structured_output(PatientRequirements)
    decision = decider.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["user_query"]),
        ]
    )
    state["patient_requirements"] = decision.model_dump()
    return state