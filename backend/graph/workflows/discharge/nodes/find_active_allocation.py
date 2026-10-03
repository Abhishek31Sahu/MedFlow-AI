from database.database import SessionLocal

from services.allocation_service import (
    AllocationService
)


def find_active_allocation(state):

    db = SessionLocal()

    try:

        service = AllocationService(db)

        allocation = service.get_active_allocation_by_encounter(

            state["encounter_id"]

        )

        if allocation is None:

            state["error"] = "No active bed allocation found."

            return state

        state["allocation_id"] = allocation.id

        state["allocation_status"] = allocation.status

        state["allocation"] = {

            "id": allocation.id,

            "bed_id": allocation.bed_id,

            "patient_id": allocation.patient_id,

            "encounter_id": allocation.encounter_id

        }

        state["bed_id"] = allocation.bed_id

        return state

    finally:

        db.close()