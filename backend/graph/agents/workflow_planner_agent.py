"""
Workflow Planner Agent

Determines whether the request should execute
a SINGLE agent or a CLINICAL WORKFLOW.
"""

from graph.state import HospitalState

from graph.prompts.workflow_prompt import (
    WORKFLOW_PROMPT
)

from graph.models.workflow import (
    WorkflowPlannerOutput
)

from graph.utils.parser import (
    ask_llm
)


def workflow_planner_agent(
    state: HospitalState
) -> HospitalState:

    try:

        # ==========================================
        # Build Prompt
        # ==========================================

        prompt = f"""
{WORKFLOW_PROMPT}

User Query:

{state["user_query"]}
"""

        # ==========================================
        # Ask LLM
        # ==========================================

        decision = ask_llm(

            prompt,

            WorkflowPlannerOutput

        )

        print("=" * 60)
        print("Workflow Planner Decision")
        print(decision)
        print("=" * 60)

        # ==========================================
        # Save Workflow Decision
        # ==========================================

        state["workflow"] = decision

        return state

    except Exception as e:

        state["error"] = str(e)

        return state