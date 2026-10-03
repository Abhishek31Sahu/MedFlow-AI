from database.database import SessionLocal

from services.bed_service import BedService


def release_reserved_bed(state):

    db = SessionLocal()

    try:

        service = BedService(db)

        bed = service.release_reserved_bed(

            state["bed_id"]

        )

        state["bed_status"] = bed.status

        state["reserved_bed"] = None

        return state

    finally:

        db.close()