"""
Patient Transfer Workflow Graph
"""

from langgraph.graph import (
    StateGraph,
    END
)

from graph.workflows.transfer.state import (
    TransferState
)

from graph.workflows.transfer.router import (

    route_resolve_patient,

    route_verify_encounter,

    route_build_patient_requirements,

    route_recommend_bed,

    route_select_bed,

    route_validate_manual_bed,
    
    route_transfer_patient,
    
    route_update_encounter,
    
    route_complete_allocation,
    
    route_find_active_allocation
)

from graph.workflows.transfer.nodes.extract_input import (
    extract_input
)

from graph.workflows.transfer.nodes.resolve_patient import (
    resolve_patient_node
)

from graph.workflows.transfer.nodes.verify_encounter import (
    verify_encounter_node
)

from graph.workflows.transfer.nodes.bed_select import (
    select_bed
)

from graph.workflows.transfer.nodes.build_patient_requirements import (
    build_patient_requirements
)

from graph.workflows.transfer.nodes.transfer_patient import (
    transfer_patient_node
)

from graph.workflows.transfer.nodes.create_allocation import (
    create_allocation
)

from graph.workflows.transfer.nodes.transfer_summary import (
    transfer_summary
)

from graph.workflows.transfer.nodes.update_encounter import (
    update_encounter_node
)

from graph.workflows.transfer.nodes.validate_manual_bed import (
    validate_manual_bed
)
from graph.workflows.transfer.nodes.recommend_bed import (
    recommend_bed
)

from graph.workflows.transfer.nodes.find_active_allocation import (
    find_active_allocation
)

from graph.workflows.transfer.nodes.complete_allocation import (
    complete_allocation
)
# ==========================================================
# Graph
# ==========================================================
def build_transfer_graph():
    
    builder = StateGraph(
        TransferState
    )


# ==========================================================
# Nodes
# ==========================================================

    builder.add_node(
    "extract_input",
    extract_input
)

    builder.add_node(
    "resolve_patient",
    resolve_patient_node
)

    builder.add_node(
    "verify_encounter",
    verify_encounter_node
)

    builder.add_node(
    "build_patient_requirements",
    build_patient_requirements
)

    builder.add_node(
    "select_bed",
    select_bed
)

    builder.add_node(
    "transfer_patient",
    transfer_patient_node
)

    builder.add_node(
    "create_allocation",
    create_allocation
)

    builder.add_node(
    "update_encounter",
    update_encounter_node
)
    builder.add_node(
    "validate_manual_bed",
    validate_manual_bed
)
    builder.add_node(
    "transfer_summary",
    transfer_summary
)
    builder.add_node(
    "recommend_bed",
    recommend_bed
)
    builder.add_node(
    "find_active_allocation",
    find_active_allocation
)
    builder.add_node(
    "complete_allocation",
    complete_allocation
)


# ==========================================================
# Entry
# ==========================================================

    builder.set_entry_point(
        "extract_input"
    )


# ==========================================================
# Linear Flow
# ==========================================================

    builder.add_edge(
        "extract_input",
        "resolve_patient"
    )


    builder.add_conditional_edges(
        "resolve_patient",
        route_resolve_patient,
        {
            "success": "verify_encounter",
            "error": "transfer_summary"
        }
    )


    builder.add_conditional_edges(
        "verify_encounter",
        route_verify_encounter,
        {
            "success": "build_patient_requirements",
            "error": "transfer_summary"
        }
    )

    builder.add_conditional_edges(
        "build_patient_requirements",
        route_build_patient_requirements,
        {
            "success": "recommend_bed",
            "error": "transfer_summary"
        }
    )

    builder.add_conditional_edges(
        "recommend_bed",
        route_recommend_bed,
        {
            "success": "select_bed",
            "error": "transfer_summary"
        }
    )

    builder.add_conditional_edges(
        "select_bed",
        route_select_bed,
        {
            "success": "find_active_allocation",
            "manual": "validate_manual_bed",
            "reject": "transfer_summary",
            "error": "transfer_summary"
        }
    )
    
    

    builder.add_conditional_edges(
        "validate_manual_bed",
        route_validate_manual_bed,
        {
            "success": "find_active_allocation",
            "error": "transfer_summary"
        }
    )
    
    
    builder.add_conditional_edges(
        "find_active_allocation",
        route_find_active_allocation,
        {
            "success": "complete_allocation",
            "error": "transfer_summary"
        }
    )
    
    builder.add_conditional_edges(
        "complete_allocation",
        route_complete_allocation,
        {
            "success": "transfer_patient",
            "error": "transfer_summary"
        }
    )

    builder.add_conditional_edges(
        "transfer_patient",
        route_transfer_patient,
        {
            "success": "update_encounter",
            "error": "transfer_summary"
        }
    )
    
    builder.add_edge(
        "update_encounter",
        "create_allocation"
    )

    builder.add_conditional_edges(
        "create_allocation",
        route_update_encounter,
        {
            "success": "transfer_summary",
            "error": "transfer_summary"
        }
    )


# ==========================================================
# Compile
# ==========================================================

    return builder