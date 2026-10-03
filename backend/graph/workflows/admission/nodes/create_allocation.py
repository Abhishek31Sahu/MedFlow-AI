from database.database import SessionLocal
from services.allocation_service import AllocationService
from schemas.bed_allocation import BedAllocationCreate


def create_allocation(state):

    db = SessionLocal()

    try:

        service = AllocationService(db)

        request = BedAllocationCreate(

            bed_id=state["bed_id"],

            patient_id=state["resolved_patient"]["id"],

            encounter_id=state["encounter_id"],

            allocated_by=state["practitioner_id"],

            allocation_type="ADMISSION",

            recommendation_score=state["selected_bed"]["score"],

            recommendation_reason=", ".join(

                state["selected_bed"]["reasons"]

            )

        )

        allocation = service.create_allocation(request)

        state["allocation_id"] = allocation.id

        state["allocation"] = {

            "id": allocation.id,

            "bed_id": allocation.bed_id,

            "patient_id": allocation.patient_id,

            "encounter_id": allocation.encounter_id,

            "status": allocation.status

        }

        state["allocation_status"] = allocation.status

        # Clear previous error if successful
        state["error"] = None

    except Exception as e:

        state["allocation_id"] = None
        state["allocation"] = None
        state["allocation_status"] = None

        state["error"] = str(e)

    finally:

        db.close()

    return state