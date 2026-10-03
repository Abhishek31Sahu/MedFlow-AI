from database.database import SessionLocal

from services.bed_service import BedService


def release_bed(state):

    db = SessionLocal()

    try:

        service = BedService(db)

        bed = service.release_bed(

            state["bed_id"]

        )

        state["bed_status"] = bed.status

        return state

    finally:

        db.close()