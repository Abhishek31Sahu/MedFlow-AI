"""
Bed Service
"""
from repositories.bed_repository import BedRepository

from services.recommendation.recommendation import RecommendationEngine


class BedRecommendationService:

    def __init__(self, db):

        self.repo = BedRepository(db)

        self.engine = RecommendationEngine()

    def recommend_beds(
        self,
        patient_requirements
    ):

        candidate_beds = self.repo.get_candidate_beds()

        return self.engine.recommend(
            patient_requirements,
            candidate_beds
        )


class BedService:

    def __init__(self, db):

        self.repo = BedRepository(db)

    # CRUD

    def create_bed(self, request):
        return self.repo.create_bed(request)

    def get_bed(self, bed_id):
        return self.repo.get_bed(bed_id)

    def get_all_beds(self):
        return self.repo.get_all_beds()

    def update_bed(self, bed_id, request):
        return self.repo.update_bed(
            bed_id,
            request.model_dump(exclude_unset=True,mode="json")
        )

    def delete_bed(self, bed_id):
        return self.repo.delete_bed(bed_id)

    # Recommendation

    # def recommend_beds(self, patient):
    #     ...
    #     # Recommendation Engine

    # Reservation

    def reserve_bed(self, bed_id):
        return self.repo.reserve_bed(bed_id)

    def release_reserved_bed(self, bed_id):
        return self.repo.release_reserved_bed(bed_id)

    # Admission

    def assign_bed(self, bed_id, patient_id, encounter_id):

        return self.repo.assign_bed(
            bed_id,
            patient_id,
            encounter_id
        )

    # Discharge

    def release_bed(self, bed_id):
        return self.repo.release_bed(bed_id)
    
    # Transfer
    
    def release_bed_by_encounter_id(self, encounter_id):
        return  self.repo.release_bed_by_encounter(encounter_id)

    # Housekeeping

    def mark_cleaning(self, bed_id):
        return self.repo.mark_cleaning(bed_id)

    def mark_available(self, bed_id):
        return self.repo.mark_available(bed_id)

    # Dashboard

    def get_available_beds(self):
        return self.repo.get_available_beds()

    def get_occupied_beds(self):
        return self.repo.get_occupied_beds()

    def get_bed_statistics(self):
        return self.repo.get_bed_statistics()