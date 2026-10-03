"""
MedicationRequest CRUD Operations
"""

from fhir.client import fhir_client
import requests
from fastapi import HTTPException

# ==========================================================
# CREATE MEDICATION
# ==========================================================

def create_medication(
    patient_id: str,
    practitioner_id: str,
    medicine_name: str,
    dosage: str,
    frequency: str,
):

    resource = {
        "resourceType": "MedicationRequest",

        "status": "active",

        "intent": "order",

        "subject": {
            "reference": f"Patient/{patient_id}"
        },

        "requester": {
            "reference": f"Practitioner/{practitioner_id}"
        },

        "medicationCodeableConcept": {
            "text": medicine_name
        },

        "dosageInstruction": [
            {
                "text": f"{dosage} - {frequency}"
            }
        ]
    }

    return fhir_client.create(
        "MedicationRequest",
        resource
    )


# ==========================================================
# READ
# ==========================================================

def get_medication(
    medication_request_id: str
):

    return fhir_client.read(
        "MedicationRequest",
        medication_request_id
    )


# ==========================================================
# SEARCH BY PATIENT
# ==========================================================

def get_patient_medications(
    patient_id: str
):

    return fhir_client.search(
        "MedicationRequest",
        {
            "patient": patient_id
        }
    )


# ==========================================================
# SEARCH ACTIVE MEDICATION
# ==========================================================

def find_active_medication(
    patient_id: str,
    medicine_name: str
):

    bundle = get_patient_medications(
        patient_id
    )

    if "entry" not in bundle:
        return None

    for entry in bundle["entry"]:

        resource = entry["resource"]

        status = resource.get("status")

        if status != "active":
            continue

        medication = (
            resource
            .get("medicationCodeableConcept", {})
            .get("text", "")
        )

        if medication.lower() == medicine_name.lower():
            return resource

    return None


# ==========================================================
# STOP MEDICATION
# ==========================================================

def stop_medication(
    medication_request_id: str
):

    medication = get_medication(
        medication_request_id
    )

    medication["status"] = "completed"

    return fhir_client.update(
        "MedicationRequest",
        medication_request_id,
        medication
    )


# ==========================================================
# UPDATE DOSAGE
# ==========================================================

def update_dosage(
    medication_request_id: str,
    dosage: str,
    frequency: str
):

    medication = get_medication(
        medication_request_id
    )

    medication["dosageInstruction"] = [
        {
            "text": f"{dosage} - {frequency}"
        }
    ]

    return fhir_client.update(
        "MedicationRequest",
        medication_request_id,
        medication
    )


# ==========================================================
# CANCEL
# ==========================================================

def cancel_medication(
    medication_request_id: str
):

    medication = get_medication(
        medication_request_id
    )

    medication["status"] = "cancelled"

    return fhir_client.update(
        "MedicationRequest",
        medication_request_id,
        medication
    )


# ==========================================================
# PRINT
# ==========================================================

def print_medication(
    medication
):

    print("=" * 60)

    print(
        "MedicationRequest ID:",
        medication.get("id")
    )

    print(
        "Medicine:",
        medication["medicationCodeableConcept"]["text"]
    )

    print(
        "Status:",
        medication["status"]
    )

    if medication.get("dosageInstruction"):

        print(
            "Dosage:",
            medication["dosageInstruction"][0]["text"]
        )

    print("=" * 60)
    
    

