from database.database import SessionLocal

from services.bed_service import (
    BedRecommendationService
)

from graph.workflows.admission.models.patient_requirement import (
    PatientRequirements
)


def recommend_bed(state):

    db = SessionLocal()

    try:

        service = BedRecommendationService(db)

        requirements = PatientRequirements(
            **state["patient_requirements"]
        )

        recommendations = service.recommend_beds(
            requirements
        )
        
        if not recommendations:

            state["error"] = "No suitable bed available."

            return state

        state["recommended_beds"] = recommendations

        return state

    finally:

        db.close()