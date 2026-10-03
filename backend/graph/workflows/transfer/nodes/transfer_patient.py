"""
Transfer Patient Node
"""

from database.database import SessionLocal
from services.bed_service import BedService


def transfer_patient_node(state):

    db = SessionLocal()

    try:

        bed_service = BedService(db)

        patient = state["resolved_patient"]

        encounter = state["active_encounter"]

        selected_bed = state["selected_bed"]

        # ---------------------------------------
        # Release previous bed (if any)
        # ---------------------------------------

        previous_bed_id = state["encounter_id"]

        if previous_bed_id:

            bed_service.release_bed_by_encounter_id(previous_bed_id)

        # ---------------------------------------
        # Assign new bed
        # ---------------------------------------

        assigned_bed = bed_service.assign_bed(

            bed_id=selected_bed["bed_id"],

            patient_id=patient["id"],

            encounter_id=encounter["id"]

        )

        state["assigned_bed"] = {
    "bed_id": str(assigned_bed.id),
    "bed_number": assigned_bed.bed_number,
    "ward": assigned_bed.ward,
    "room_number": assigned_bed.room_number,
    "department": assigned_bed.department,
    "location_id": assigned_bed.location_id,
}

        return state

    except Exception as e:

        state["error"] = str(e)

        return state

    finally:

        db.close()