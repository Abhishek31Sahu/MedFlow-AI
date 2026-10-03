"""
Bed Allocation Repository
"""

from datetime import datetime

from sqlalchemy.orm import Session

from models.bed_allocation import BedAllocation
from models.enums import AllocationStatus


class AllocationRepository:

    def __init__(self, db: Session):

        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    def create_allocation(self, allocation_data):

        data = allocation_data.model_dump()

        data["allocation_type"] = data["allocation_type"].value

        allocation = BedAllocation(**data)

        self.db.add(allocation)

        self.db.commit()

        self.db.refresh(allocation)

        return allocation

    # ==========================================================
    # Get by ID
    # ==========================================================

    def get_allocation(self, allocation_id):

        return (

            self.db.query(BedAllocation)

            .filter(
                BedAllocation.id == allocation_id
            )

            .first()

        )

    # ==========================================================
    # Active Allocation
    # ==========================================================

    def get_active_allocation(

        self,

        patient_id

    ):

        return (

            self.db.query(BedAllocation)

            .filter(

                BedAllocation.patient_id == patient_id,

                BedAllocation.status == AllocationStatus.ACTIVE.value

            )

            .first()

        )

    # ==========================================================
    # Bed Current Allocation
    # ==========================================================

    def get_active_bed_allocation(

        self,

        bed_id

    ):

        return (

            self.db.query(BedAllocation)

            .filter(

                BedAllocation.bed_id == bed_id,

                BedAllocation.status == AllocationStatus.ACTIVE.value

            )

            .first()

        )

    # ==========================================================
    # Patient History
    # ==========================================================

    def get_patient_history(

        self,

        patient_id

    ):

        return (

            self.db.query(BedAllocation)

            .filter(

                BedAllocation.patient_id == patient_id

            )

            .order_by(

                BedAllocation.allocated_at.desc()

            )

            .all()

        )

    # ==========================================================
    # Bed History
    # ==========================================================

    def get_bed_history(

        self,

        bed_id

    ):

        return (

            self.db.query(BedAllocation)

            .filter(

                BedAllocation.bed_id == bed_id

            )

            .order_by(

                BedAllocation.allocated_at.desc()

            )

            .all()

        )

    # ==========================================================
    # Complete Allocation
    # ==========================================================

    def complete_allocation(

        self,

        allocation_id

    ):

        allocation = self.get_allocation(

            allocation_id

        )

        if allocation is None:

            raise Exception(

                "Allocation not found"

            )

        allocation.status = AllocationStatus.COMPLETED.value

        allocation.released_at = datetime.utcnow()

        self.db.commit()

        self.db.refresh(allocation)

        return allocation

    # ==========================================================
    # Cancel Allocation
    # ==========================================================

    def cancel_allocation(

        self,

        allocation_id

    ):

        allocation = self.get_allocation(

            allocation_id

        )

        if allocation is None:

            raise Exception(

                "Allocation not found"

            )

        allocation.status = AllocationStatus.CANCELLED.value

        allocation.released_at = datetime.utcnow()

        self.db.commit()

        self.db.refresh(allocation)

        return allocation

    # ==========================================================
    # Delete
    # ==========================================================

    def delete_allocation(

        self,

        allocation_id

    ):

        allocation = self.get_allocation(

            allocation_id

        )

        if allocation is None:

            return False

        self.db.delete(allocation)

        self.db.commit()

        return True
    
    def get_active_allocation_by_encounter(
        self,
        encounter_id
    ):

        return (

        self.db.query(BedAllocation)

        .filter(

            BedAllocation.encounter_id == encounter_id,

            BedAllocation.status == AllocationStatus.ACTIVE.value

        )

        .first()

    )