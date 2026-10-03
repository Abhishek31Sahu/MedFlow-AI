from database.database import SessionLocal

from services.bed_service import BedService


def reserve_bed(state):

    db = SessionLocal()

    try:

        service = BedService(db)

        bed = service.reserve_bed(

            state["selected_bed_id"]

        )

        state["reserved_bed"] = {

            "id": bed.id,

            "bed_number": bed.bed_number,

            "status": bed.status

        }
        
        state["location_id"]=bed.location_id

        state["bed_id"] = bed.id

        state["bed_status"] = bed.status

        return state

    finally:

        db.close()