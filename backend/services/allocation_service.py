"""
Bed Allocation Service
"""

from repositories.allocation_repository import (
    AllocationRepository
)


class AllocationService:

    def __init__(self, db):

        self.repo = AllocationRepository(db)

    # ==========================================================
    # Create Allocation
    # ==========================================================

    def create_allocation(
        self,
        request
    ):

        return self.repo.create_allocation(
            request
        )

    # ==========================================================
    # Get Allocation
    # ==========================================================

    def get_allocation(
        self,
        allocation_id
    ):

        return self.repo.get_allocation(
            allocation_id
        )

    # ==========================================================
    # Active Allocation
    # ==========================================================

    def get_active_allocation(
        self,
        patient_id
    ):

        return self.repo.get_active_allocation(
            patient_id
        )

    # ==========================================================
    # Active Bed Allocation
    # ==========================================================

    def get_active_bed_allocation(
        self,
        bed_id
    ):

        return self.repo.get_active_bed_allocation(
            bed_id
        )

    # ==========================================================
    # Patient History
    # ==========================================================

    def get_patient_history(
        self,
        patient_id
    ):

        return self.repo.get_patient_history(
            patient_id
        )

    # ==========================================================
    # Bed History
    # ==========================================================

    def get_bed_history(
        self,
        bed_id
    ):

        return self.repo.get_bed_history(
            bed_id
        )

    # ==========================================================
    # Complete Allocation
    # ==========================================================

    def complete_allocation(
        self,
        allocation_id
    ):

        return self.repo.complete_allocation(
            allocation_id
        )

    # ==========================================================
    # Cancel Allocation
    # ==========================================================

    def cancel_allocation(
        self,
        allocation_id
    ):

        return self.repo.cancel_allocation(
            allocation_id
        )

    # ==========================================================
    # Delete Allocation
    # ==========================================================

    def delete_allocation(
        self,
        allocation_id
    ):

        return self.repo.delete_allocation(
            allocation_id
        )
        

    def get_active_allocation_by_encounter(

        self,

        encounter_id

    ):

        return self.repo.get_active_allocation_by_encounter(

            encounter_id

        )