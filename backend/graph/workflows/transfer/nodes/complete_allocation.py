from database.database import SessionLocal

from services.allocation_service import (
    AllocationService
)


def complete_allocation(state):

    db = SessionLocal()

    try:
        if state["allocation_status"] == "ACTIVE":
            service = AllocationService(db)

            allocation = service.complete_allocation(

                state["allocation_id"]

            )

            state["allocation_status"] = allocation.status

            state["allocation"] = {

                "id": allocation.id,

                "status": allocation.status,

                "released_at": allocation.released_at

            }

            return state
        else:
            state["error"] = "Status is not active"

    finally:

        db.close()