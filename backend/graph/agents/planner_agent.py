"""
Planner Agent

Responsibility:
Only decide which specialist agent
should handle the user's request.
"""

import json

from graph.state import HospitalState

from graph.prompts.planner_prompt import (
    PLANNER_PROMPT
)

from graph.models.planner import (
    PlannerOutput
)

from graph.utils.llm import llm


def planner_agent(
    state: HospitalState
) -> HospitalState:

    try:

        prompt = f"""
{PLANNER_PROMPT}

User Query:

{state["user_query"]}
"""

        response = llm.invoke(prompt)

        print("=" * 60)
        print("Planner Raw Response")
        print(response.content)
        print("=" * 60)

        data = json.loads(
            response.content
        )

        planner = PlannerOutput.model_validate(
            data
        )
        
        state["planner"] = planner

        return state

    except Exception as e:
        

        print("=" * 60)
        print("PLANNER ERROR")
        print(type(e))
        print(e)
        print("=" * 60)

        state["error"] = str(e)

        return state