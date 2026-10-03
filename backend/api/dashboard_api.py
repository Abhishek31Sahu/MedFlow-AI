from fastapi import APIRouter, HTTPException
from fhir.client import fhir_client

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_fhir_count(resource_type: str) -> int:
    try:
        bundle = fhir_client.search(
            resource_type,
            params={"_summary": "count"}
        )
        return bundle.get("total", 0)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get {resource_type} count: {str(e)}"
        )


@router.get("/dashboard-stats")
def get_dashboard_stats():
    return {
        "patients": get_fhir_count("Patient"),
        "service_requests": get_fhir_count("ServiceRequest"),
        "diagnostic_reports": get_fhir_count("DiagnosticReport"),
        "observations": get_fhir_count("Observation"),
        "medication_requests": get_fhir_count("MedicationRequest"),
    }