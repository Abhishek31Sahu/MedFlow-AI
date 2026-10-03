"""
Medication Service

Business logic for medication management.
"""
import requests
from fastapi import  HTTPException
from medication.medication import (
    create_medication,
    find_active_medication,
    stop_medication,
    update_dosage,
    get_patient_medications,
)


# ==========================================================
# ADD MEDICATION
# ==========================================================

def add_medication(
    patient_id: str,
    practitioner_id: str,
    medicine_name: str,
    dosage: str,
    frequency: str,
):

    # ----------------------------------
    # Already Active?
    # ----------------------------------

    existing = find_active_medication(
        patient_id,
        medicine_name
    )

    if existing:

        return {
            "success": False,
            "message":
                f"{medicine_name} is already active.",
            "medication_request_id":
                existing["id"]
        }

    medication = create_medication(

        patient_id,

        practitioner_id,

        medicine_name,

        dosage,

        frequency
    )

    return {

        "success": True,

        "message": "Medication Added",

        "medication_request_id":
            medication["id"]
    }


# ==========================================================
# STOP MEDICATION
# ==========================================================

def discontinue_medication(
    patient_id: str,
    medicine_name: str,
):

    medication = find_active_medication(

        patient_id,

        medicine_name
    )

    if medication is None:

        return {

            "success": False,

            "message":
                "Medication not found."
        }

    stop_medication(
        medication["id"]
    )

    return {

        "success": True,

        "message":
            f"{medicine_name} stopped."
    }


# ==========================================================
# CHANGE DOSE
# ==========================================================

def change_dosage(
    patient_id: str,
    medicine_name: str,
    dosage: str,
    frequency: str,
):

    medication = find_active_medication(

        patient_id,

        medicine_name
    )

    if medication is None:

        return {

            "success": False,

            "message":
                "Medication not found."
        }

    update_dosage(

        medication["id"],

        dosage,

        frequency
    )

    return {

        "success": True,

        "message":
            "Dosage updated."
    }


# ==========================================================
# LIST ACTIVE MEDICATIONS
# ==========================================================

def list_active_medications(
    patient_id: str
):

    bundle = get_patient_medications(
        patient_id
    )

    medicines = []

    if "entry" not in bundle:

        return medicines

    for entry in bundle["entry"]:

        resource = entry["resource"]

        if resource.get("status") != "active":
            continue

        medicines.append({

            "id":
                resource["id"],

            "medicine":
                resource[
                    "medicationCodeableConcept"
                ]["text"],

            "dosage":
                resource[
                    "dosageInstruction"
                ][0]["text"]
        })

    return medicines


# ==========================================================
# MEDICATION HISTORY
# ==========================================================

def medication_history(
    patient_id: str
):

    bundle = get_patient_medications(
        patient_id
    )

    history = []

    if "entry" not in bundle:

        return history

    for entry in bundle["entry"]:

        resource = entry["resource"]

        history.append({

            "id":
                resource["id"],

            "medicine":
                resource[
                    "medicationCodeableConcept"
                ]["text"],

            "status":
                resource["status"]
        })

    return history

from fhir.client import fhir_client
def get_all_active_medications():
    try:
        bundle = fhir_client.search(
            "MedicationRequest",
            params={
                "status": "active",
                "_count": 100
            }
        )

        medications = []

        for entry in bundle.get("entry", []):
            resource = entry.get("resource", {})

            # -----------------------------
            # Patient
            # -----------------------------
            subject = resource.get("subject", {})
            patient_reference = subject.get("reference", "")

            patient_id = patient_reference.replace(
                "Patient/",
                ""
            )

            # -----------------------------
            # Medicine
            # -----------------------------
            medication_data = resource.get(
                "medicationCodeableConcept",
                {}
            )

            medicine_name = medication_data.get(
                "text",
                "Unknown"
            )

            # -----------------------------
            # Dosage
            # -----------------------------
            dosage_instruction = resource.get(
                "dosageInstruction",
                []
            )

            dosage = ""

            if dosage_instruction:
                dosage = dosage_instruction[0].get(
                    "text",
                    ""
                )

            medications.append({
                "id": resource.get("id"),
                "patient_id": patient_id,
                "medicine": medicine_name,
                "dosage": dosage,
                "status": resource.get("status")
            })

        return {
            "total": len(medications),
            "medications": medications
        }

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch medications: {str(e)}"
        )