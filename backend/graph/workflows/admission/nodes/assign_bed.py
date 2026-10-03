from database.database import SessionLocal

from services.bed_service import BedService


def assign_bed(state):

    db = SessionLocal()

    try:

        service = BedService(db)

        bed = service.assign_bed(

            bed_id=state["bed_id"],

            patient_id=state["resolved_patient"]["id"],

            encounter_id=state["encounter_id"]

        )

        state["bed_status"] = bed.status

        return state

    finally:

        db.close()