"""
Execute Discharge Workflow
"""

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.workflows.discharge.state import (
    DischargeState
)

from graph.workflows.discharge.nodes.update_medications import (
    update_medications
)

from graph.workflows.discharge.nodes.complete_encounter import (
    complete_encounter
)

from graph.workflows.discharge.nodes.verify_discharge import (
    verify_discharge
)

from graph.workflows.discharge.nodes.discharge_summary import (
    discharge_summary
)

from graph.workflows.discharge.nodes.complete_allocation import(
    complete_allocation
)

from graph.workflows.discharge.nodes.release_bed import(
    release_bed
)

builder = StateGraph(
    DischargeState
)

builder.add_node(
    "update_medications",
    update_medications
)

builder.add_node(
    "complete_encounter",
    complete_encounter
)

builder.add_node(
    "verify_discharge",
    verify_discharge
)

builder.add_node(
    "discharge_summary",
    discharge_summary
)

builder.add_node(
    "release_bed",
    release_bed
)

builder.add_node(
    "complete_allocation",
    complete_allocation
)

builder.add_edge(
    START,
    "update_medications"
)

builder.add_edge(
    "update_medications",
    "complete_encounter"
)

builder.add_edge(
    "complete_encounter",
    "release_bed"
)

builder.add_edge(
    "release_bed",
    "verify_discharge"
)

# builder.add_edge(
#     "complete_allocation",
#     "verify_discharge"
# )

builder.add_edge(
    "verify_discharge",
    "discharge_summary"
)

builder.add_edge(
    "discharge_summary",
    END
)

execute_discharge_graph = builder.compile()