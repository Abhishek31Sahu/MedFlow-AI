"""
Doctor Laboratory Workflow State
"""

from typing import Any, TypedDict
from graph.state import HospitalState

class DoctorLabOrderState(HospitalState):

    # ==========================================================
    # Original Request
    # ==========================================================

    user_query: str

    # ==========================================================
    # Authenticated User
    # ==========================================================

    practitioner_id: str

    # ==========================================================
    # Workflow
    # ==========================================================

    workflow_id: str | None

    workflow_status: str | None

    current_step: str | None

    # ==========================================================
    # Extracted Laboratory Data
    # ==========================================================

    workflow_data: dict

    # Example
    #
    # {
    #     "patient_name": "Hari Kumar",
    #     "tests": [
    #         {
    #             "code": "57021-8",
    #             "name": "Complete Blood Count"
    #         },
    #         {
    #             "code": "2339-0",
    #             "name": "Blood Sugar"
    #         }
    #     ],
    #     "priority": "routine",
    #     "clinical_note": "Routine health check"
    # }

    # ==========================================================
    # Patient Resolution
    # ==========================================================

    resolved_patient: dict | None

    candidate_patients: list

    # ==========================================================
    # Active Encounter
    # ==========================================================

    encounter_id: str | None

    active_encounter: dict | None

    # ==========================================================
    # Laboratory Orders
    # ==========================================================

    laboratory_orders: list

    # Example
    #
    # [
    #     {
    #         "service_request_id": "...",
    #         "test_name": "CBC"
    #     },
    #     {
    #         "service_request_id": "...",
    #         "test_name": "Blood Sugar"
    #     }
    # ]

    # ==========================================================
    # Workflow Result
    # ==========================================================

    workflow_results: list

    result: Any

    # ==========================================================
    # Error
    # ==========================================================

    error: str | None