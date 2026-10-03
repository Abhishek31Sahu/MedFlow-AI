"""
Response Agent
===============

The single funnel every specialist agent and every clinical
workflow passes through before the doctor sees anything (see
graph.py: every branch has an edge into "response" -> END).

Responsibility split, on purpose:

- Control fields (success, status, category, workflow) are derived
  HERE, in code, straight from HospitalState. They are ground truth
  and must never depend on an LLM's judgement, so the frontend can
  trust them 1:1 and render the same layout every time regardless
  of which agent ran.

- Content fields (title, message, highlights,
  suggested_replies) are written by the LLM, constrained to the
  narrow `ResponseContent` schema, from the same ground truth data.

The result is always a `ResponseOutput` — one fixed shape, whatever
produced it.
"""

import json

from langchain_core.messages import AIMessage

from graph.state import HospitalState

from graph.prompts.response_prompt import RESPONSE_PROMPT

from graph.models.response import (
    Highlight,
    ResponseTable,
    ResponseContent,
    ResponseOutput,
    WorkflowInfo,
)

from graph.utils.parser import ask_llm
from graph.utils.response_extract import (
    ground_truth_highlights,
    ground_truth_tables,
)


# ==================================================================
# Helpers
# ==================================================================

def _json_default(obj):
    """
    Fallback serializer for objects json.dumps can't handle natively
    (Pydantic models, dataclasses, or plain objects with __dict__).
    """
    if hasattr(obj, "model_dump"):      # Pydantic v2
        return obj.model_dump()
    if hasattr(obj, "dict"):            # Pydantic v1
        return obj.dict()
    if hasattr(obj, "__dict__"):        # dataclass / plain object
        return obj.__dict__
    raise TypeError(
        f"Object of type {obj.__class__.__name__} is not JSON serializable"
    )


# Terminal workflow states that mean "this workflow is done" one way
# or another, as opposed to still waiting on the doctor.
_TERMINAL_WORKFLOW_STATUSES = {
    "COMPLETED",
    "CANCELLED",
    "CONFIRMED",
    "FAILED",
    "ERROR",
}


def _derive_category(state: HospitalState) -> str:
    """
    Stable machine-readable source identifier. A workflow in
    progress always wins (it's the thing actually driving the
    conversation); otherwise fall back to whichever specialist
    agent the planner routed to.
    """

    active_workflow = state.get("active_workflow")

    if active_workflow:
        return active_workflow

    planner = state.get("planner")

    if planner is not None:
        return planner.target

    return "general"


def _derive_status(state: HospitalState, has_result: bool) -> tuple[bool, str]:
    """
    Returns (success, status). This is the ONLY place in the
    codebase that decides these two values — never the LLM.
    """

    error = state.get("error")

    if error:
        return False, "error"

    workflow_status = state.get("workflow_status")
    missing_fields = state.get("missing_fields") or []

    # A workflow is mid-flight and needs something from the doctor
    # (a missing field, or an explicit confirmation step).
    if workflow_status and workflow_status not in _TERMINAL_WORKFLOW_STATUSES:
        if missing_fields or workflow_status.startswith("WAITING_FOR"):
            return True, "action_required"
        return True, "in_progress"

    if workflow_status == "FAILED" or workflow_status == "ERROR":
        return False, "error"

    return True, "success"


def _derive_workflow_info(state: HospitalState) -> WorkflowInfo | None:
    active_workflow = state.get("active_workflow")

    if not active_workflow:
        return None

    return WorkflowInfo(
        name=active_workflow,
        status=state.get("workflow_status") or "IN_PROGRESS",
        step=state.get("current_step"),
        missing_fields=state.get("missing_fields") or [],
    )


def _apply_ground_truth(
    highlights: list[Highlight],
    result,
    max_items: int = 6,
) -> list[Highlight]:
    """
    Corrects or fills in the LLM's highlights using values read
    directly from the backend result (see response_extract.py).
    An identity field the LLM got right is left untouched; one it
    got wrong or blanked out ("-", "N/A", "") is overwritten in
    place; one it missed entirely is added. This is what guarantees
    a doctor never sees an incorrect name, ID, dosage, etc. because
    the model mis-transcribed it.
    """

    truths = dict(ground_truth_highlights(result, max_items=max_items))

    if not truths:
        return highlights[:max_items]

    by_label = {h.label.strip().lower(): i for i, h in enumerate(highlights)}
    corrected = list(highlights)
    prepend: list[Highlight] = []

    for label, value in truths.items():
        idx = by_label.get(label.lower())

        if idx is not None:
            corrected[idx] = Highlight(
                label=label,
                value=value,
                emphasis=corrected[idx].emphasis,
            )
        else:
            prepend.append(Highlight(label=label, value=value))

    return (prepend + corrected)[:max_items]


# ==================================================================
# Agent
# ==================================================================

def response_agent(
    state: HospitalState
) -> HospitalState:

    result = state.get("result")
    error = state.get("error")

    success, status = _derive_status(state, has_result=result is not None)
    category = _derive_category(state)
    workflow = _derive_workflow_info(state)

    prompt = f"""
{RESPONSE_PROMPT}

Source

{category}

Status

{status}

User Query

{state["user_query"]}

Backend Result

{json.dumps(result, indent=2, default=_json_default)}

Backend Error

{error}

Workflow Context

{json.dumps(workflow.model_dump() if workflow else None, indent=2)}
"""

    content: ResponseContent = ask_llm(
        prompt,
        ResponseContent,
    )

    highlights = _apply_ground_truth(content.highlights, result)

    response = ResponseOutput(
        success=success,
        status=status,
        category=category,
        title=content.title,
        message=content.message,
        highlights=highlights,
        # Tables come from the raw result in code, never the LLM, so
        # IDs and values are always exact.
        tables=[ResponseTable(**t) for t in ground_truth_tables(result)],
        # Only ever surface reply chips when a doctor is actually
        # being asked for something — guards against the LLM
        # attaching them out of habit on a plain success/error.
        suggested_replies=(
            content.suggested_replies if status == "action_required" else []
        ),
        data=result if isinstance(result, (dict, list)) else None,
        workflow=workflow,
    )
    
    print(state["authorization_denied"])
    print(response)
    state["response"] = response
    state["messages"] = [AIMessage(content=response.message)]

    return state