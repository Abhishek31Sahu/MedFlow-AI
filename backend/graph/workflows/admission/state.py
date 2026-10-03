from typing import Any
from graph.state import HospitalState


class AdmissionState(HospitalState):

    # user_query, messages, practitioner_id, workflow_status,
    # workflow_data, resolved_patient, candidate_patients,
    # result, error — all inherited from HospitalState, no need
    # to redeclare them here.

    # ==========================================================
    # Workflow
    # ==========================================================
    workflow_id: str | None
    current_step: str | None

    # ==========================================================
    # Patient Requirements (LLM Structured Output)
    # ==========================================================
    patient_requirements: dict | None

    # ==========================================================
    # Candidate Beds
    # ==========================================================
    candidate_beds: list

    # ==========================================================
    # AI Recommendations
    # ==========================================================
    recommended_beds: list

    # ==========================================================
    # Doctor Selection
    # ==========================================================
    selected_bed_id: str | None
    selected_bed: dict | None

    # ==========================================================
    # Reserved Bed
    # ==========================================================
    reserved_bed: dict | None

    # ==========================================================
    # Bed Assignment
    # ==========================================================
    bed_id: str | None
    bed_status: str | None

    # ==========================================================
    # Bed Allocation
    # ==========================================================
    allocation_id: str | None
    allocation: dict | None
    allocation_status: str | None

    # ==========================================================
    # Encounter
    # ==========================================================
    encounter_id: str | None
    encounter: dict | None
    active_encounter: dict | None

    # ==========================================================
    # FHIR Location
    # ==========================================================
    location_id: str | None
    location: dict | None

    # ==========================================================
    # Workflow Result
    # ==========================================================
    workflow_results: list