"""
Update Medications
"""

from graph.workflows.discharge.state import DischargeState
from graph.workflows.discharge.models.doctor_decision import DoctorDecision

from services.medication_service import (
    discontinue_medication,
    change_dosage,
)


def update_medications(
    state: DischargeState
) -> DischargeState:

    raw_decisions = state.get("doctor_decision", [])

    patient_id = state["resolved_patient"]["id"]

    for raw_item in raw_decisions:

        # LangGraph/checkpoint state may contain dictionaries
        # instead of Pydantic objects after resume.
        item = (
            raw_item
            if isinstance(raw_item, DoctorDecision)
            else DoctorDecision.model_validate(raw_item)
        )

        action = item.final_action
        medicine_name = item.medicine_name

        if action == "stop":

            discontinue_medication(
                patient_id,
                medicine_name
            )

        elif action == "modify":

            if not item.dosage or not item.frequency:
                raise ValueError(
                    f"Dosage and frequency are required "
                    f"when modifying '{item.medicine_name}'."
                )

            change_dosage(
                patient_id=patient_id,
                medicine_name=medicine_name,
                dosage=item.dosage,
                frequency=item.frequency,
            )

    return state