from repositories.bed_repository import BedRepository
from database.database import SessionLocal

def validate_manual_bed(state):
    db = SessionLocal()
    try:
        service = BedRepository(db)

        bed_id = state["selected_bed_id"]

        requirements = state["patient_requirements"]

        bed = service.get_bed(bed_id)

        if bed is None:

            state["error"] = f"Bed '{bed_id}' not found."

            return state

        if bed.status != "AVAILABLE":

            state["error"] = f"Bed '{bed_id}' is not available."

            return state

        # Example validations

        if requirements["bed_type"] != bed.bed_type:

            state["error"] = (
                f"Bed type mismatch. "
                f"Required: {requirements['bed_type']}, "
                f"Selected: {bed.bed_type}"
            )

            return state

        if requirements["oxygen"] and not bed.oxygen:

            state["error"] = "Selected bed does not have oxygen."

            return state

        if requirements["ventilator"] and not bed.ventilator:

            state["error"] = "Selected bed does not have a ventilator."

            return state

        if requirements["isolation"] and not bed.isolation:

            state["error"] = "Selected bed is not an isolation bed."

            return state

        if requirements["cardiac_monitor"] and not bed.cardiac_monitor:

            state["error"] = "Selected bed does not have a cardiac monitor."

            return state

        # Passed all validations

        state["selected_bed"] = {
    "bed_id": str(bed.id),
    "bed_number": bed.bed_number,
    "ward": bed.ward,
    "room_number": bed.room_number,
    "department": bed.department,
    "location_id": bed.location_id,
}

        return state
    finally:
        db.close()