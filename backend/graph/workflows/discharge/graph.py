"""
Discharge Workflow Graph
"""

from langgraph.graph import (
    StateGraph,
    END
)

from graph.workflows.discharge.state import (
    DischargeState
)

# Nodes
from graph.workflows.discharge.nodes.extract_input import (
    extract_input
)
from graph.workflows.discharge.nodes.resolve_patient import (
    resolve_patient_node
)
from graph.workflows.discharge.nodes.find_active_encounter import (
    find_active_encounter_node
)
from graph.workflows.discharge.nodes.find_active_allocation import (
    find_active_allocation
)
from graph.workflows.discharge.nodes.review_active_medications import (
    review_active_medications
)
from graph.workflows.discharge.nodes.ai_medication_review import (
    ai_medication_review
)
from graph.workflows.discharge.nodes.doctor_medication_review import (
    doctor_medication_review
)
from graph.workflows.discharge.nodes.update_medications import (
    update_medications
)
from graph.workflows.discharge.nodes.complete_encounter import (
    complete_encounter
)
from graph.workflows.discharge.nodes.release_bed import (
    release_bed
)
from graph.workflows.discharge.nodes.complete_allocation import (
    complete_allocation
)
from graph.workflows.discharge.nodes.verify_discharge import (
    verify_discharge
)
from graph.workflows.discharge.nodes.discharge_summary import (
    discharge_summary
)

# Router
from graph.workflows.discharge.router import (
    route_after_patient_resolution,
    route_after_active_encounter,
    route_after_active_allocation,
    route_after_medications,
    route_after_doctor_approval,
    route_after_update_medications,
    route_after_complete_encounter,
    route_after_release_bed,
    route_after_complete_allocation,
    route_after_verification
)


def build_discharge_graph():

    builder = StateGraph(
        DischargeState
    )

    # ======================================================
    # Nodes
    # ======================================================

    builder.add_node(
        "extract_input",
        extract_input
    )

    builder.add_node(
        "resolve_patient",
        resolve_patient_node
    )

    builder.add_node(
        "find_active_encounter",
        find_active_encounter_node
    )

    builder.add_node(
        "find_active_allocation",
        find_active_allocation
    )

    builder.add_node(
        "review_active_medications",
        review_active_medications
    )

    builder.add_node(
        "ai_medication_review",
        ai_medication_review
    )

    builder.add_node(
        "doctor_medication_review",
        doctor_medication_review
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
        "release_bed",
        release_bed
    )

    builder.add_node(
        "complete_allocation",
        complete_allocation
    )

    builder.add_node(
        "verify_discharge",
        verify_discharge
    )

    builder.add_node(
        "discharge_summary",
        discharge_summary
    )

    # ======================================================
    # Entry Point
    # ======================================================

    builder.set_entry_point(
        "extract_input"
    )

    builder.add_edge(
        "extract_input",
        "resolve_patient"
    )

    # ======================================================
    # Resolve Patient
    # ======================================================

    builder.add_conditional_edges(

        "resolve_patient",

        route_after_patient_resolution,

        {

            "find_active_encounter":
                "find_active_encounter",

            "END":
                END

        }

    )

    # ======================================================
    # Active Encounter
    # ======================================================

    builder.add_conditional_edges(

        "find_active_encounter",

        route_after_active_encounter,

        {

            "find_active_allocation":
                "find_active_allocation",

            "END":
                END

        }

    )

    # ======================================================
    # Active Allocation
    # ======================================================

    builder.add_conditional_edges(

        "find_active_allocation",

        route_after_active_allocation,

        {

            "review_active_medications":
                "review_active_medications",

            "END":
                END

        }

    )

    # ======================================================
    # Medication Review
    # ======================================================

    builder.add_conditional_edges(

        "review_active_medications",

        route_after_medications,

        {

            "ai_medication_review":
                "ai_medication_review",

            "complete_encounter":
                "complete_encounter",

            "END":
                END

        }

    )

    # ======================================================
    # AI Review
    # ======================================================

    builder.add_edge(

        "ai_medication_review",

        "doctor_medication_review"

    )

    # ======================================================
    # Doctor Review (Interrupt)
    # ======================================================

    builder.add_conditional_edges(

        "doctor_medication_review",

        route_after_doctor_approval,

        {

            "update_medications":
                "update_medications",

            "END":
                END

        }

    )

    # ======================================================
    # Medication Update
    # ======================================================

    builder.add_conditional_edges(

        "update_medications",

        route_after_update_medications,

        {

            "complete_encounter":
                "complete_encounter",

            "END":
                END

        }

    )

    # ======================================================
    # Encounter
    # ======================================================

    builder.add_conditional_edges(

        "complete_encounter",

        route_after_complete_encounter,

        {

            "release_bed":
                "release_bed",

            "END":
                END

        }

    )

    # ======================================================
    # Release Bed
    # ======================================================

    builder.add_conditional_edges(

        "release_bed",

        route_after_release_bed,

        {

            "complete_allocation":
                "complete_allocation",

            "END":
                END

        }

    )

    # ======================================================
    # Complete Allocation
    # ======================================================

    builder.add_conditional_edges(

        "complete_allocation",

        route_after_complete_allocation,

        {

            "verify_discharge":
                "verify_discharge",

            "END":
                END

        }

    )

    # ======================================================
    # Verification
    # ======================================================

    builder.add_conditional_edges(

        "verify_discharge",

        route_after_verification,

        {

            "discharge_summary":
                "discharge_summary",

            "END":
                END

        }

    )

    # ======================================================
    # Summary
    # ======================================================

    builder.add_edge(

        "discharge_summary",

        END

    )

    return builder