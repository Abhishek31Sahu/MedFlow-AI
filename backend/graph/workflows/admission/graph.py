"""
Patient Admission Workflow
"""

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.workflows.admission.state import (
    AdmissionState
)

# ==========================================================
# Nodes
# ==========================================================

from graph.workflows.admission.nodes.extract_input import (
    extract_input
)

from graph.workflows.admission.nodes.resolve_patient import (
    resolve_patient_node
)

from graph.workflows.admission.nodes.check_active_encounter import (
    check_active_encounter
)

from graph.workflows.admission.nodes.create_encounter import (
    create_encounter
)


from graph.workflows.admission.nodes.admission_summary import (
    admission_summary
)



from graph.workflows.admission.nodes.bed_select import (
    select_bed
)

from graph.workflows.admission.nodes.recommend_bed import (
    recommend_bed
)

from graph.workflows.admission.nodes.build_patient_requirements import (
    build_patient_requirements
)

from graph.workflows.admission.nodes.release_reserve_bed import (
    release_reserved_bed
)

from graph.workflows.admission.nodes.assign_bed import (
    assign_bed
)

from graph.workflows.admission.nodes.reserve_bed import (
    reserve_bed
)
from graph.workflows.admission.nodes.create_allocation import(
    create_allocation
)
# ==========================================================
# Routers
# ==========================================================

from graph.workflows.admission.router import (
    route_after_patient_resolution,
    route_after_active_encounter,
    route_after_allocate_bed,
    route_after_create_encounter,
    route_after_create_allocation,
    route_after_release_reserved_bed
)

# ==========================================================
# Build Graph
# ==========================================================
def build_admission_graph():
    builder = StateGraph(
    AdmissionState
    )

# ==========================================================
# Register Nodes
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
    "check_active_encounter",
    check_active_encounter
)

    builder.add_node(
    "create_encounter",
    create_encounter
)

    builder.add_node(
    "admission_summary",
    admission_summary
)


    builder.add_node(
    "select_bed",
    select_bed
)

    builder.add_node(
    "recommend_bed",
    recommend_bed
)
    builder.add_node(
    "build_patient_requirements",
    build_patient_requirements
)
    builder.add_node(
    "release_reserved_bed",
    release_reserved_bed
)
    
    builder.add_node(
    "reserve_bed",
    reserve_bed
)
    builder.add_node(
    "assign_bed",
    assign_bed
)
    builder.add_node(
    "create_allocation",
    create_allocation
)
# ==========================================================
# Edges
# ==========================================================

    builder.add_edge(
    START,
    "extract_input"
)

    builder.add_edge(
    "extract_input",
    "resolve_patient"
)

# ==========================================================
# Conditional Routing
# ==========================================================

    builder.add_conditional_edges(

    "resolve_patient",

    route_after_patient_resolution,

    {

        "check_active_encounter":
            "check_active_encounter",

        "admission_summary":
            "admission_summary",

    }

)


    builder.add_conditional_edges(

    "check_active_encounter",

    route_after_active_encounter,

    {

        "build_patient_requirements":
            "build_patient_requirements",

        "admission_summary":
            "admission_summary",

    }

)


    builder.add_edge(
    "build_patient_requirements",
    "recommend_bed"
)

    builder.add_edge(
    "recommend_bed",
    "select_bed"
)

    builder.add_edge(
    "select_bed",
    "reserve_bed"
)


    builder.add_conditional_edges(

    "reserve_bed",

    route_after_allocate_bed,

    {

        "create_encounter":
            "create_encounter",

        "admission_summary":
            "admission_summary",

    }

)


    builder.add_conditional_edges(

    "create_encounter",

    route_after_create_encounter,

    {

        "assign_bed":
            "assign_bed",

        "release_reserved_bed":
            "release_reserved_bed",

    }

)


    builder.add_edge(
    "assign_bed",
    "create_allocation"
)


    builder.add_conditional_edges(

    "create_allocation",

    route_after_create_allocation,

    {

        "admission_summary":
            "admission_summary",

        "release_reserved_bed":
            "release_reserved_bed",

    }

)


    builder.add_conditional_edges(

    "release_reserved_bed",

    route_after_release_reserved_bed,

    {

        "admission_summary":
            "admission_summary",

    }

)


    builder.add_edge(
    "admission_summary",
    END
)

# ==========================================================
# Compile
# ==========================================================

    return builder