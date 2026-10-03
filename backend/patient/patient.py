"""
Patient CRUD Operations

This module contains all Patient-related operations.
"""

from fhir.client import fhir_client


# ==========================================================
# CREATE
# ==========================================================

def create_patient(
    first_name: str,
    last_name: str,
    gender: str,
    birth_date: str
):
    """
    birth_date format:
    YYYY-MM-DD
    """

    patient = {
        "resourceType": "Patient",
        "active": True,
        "name": [
            {
                "family": last_name,
                "given": [
                    first_name
                ]
            }
        ],
        "gender": gender,
        "birthDate": birth_date
    }

    return fhir_client.create(
        "Patient",
        patient
    )


# ==========================================================
# READ
# ==========================================================

def get_patient(patient_id: str):

    return fhir_client.read(
        "Patient",
        patient_id
    )


# ==========================================================
# SEARCH
# ==========================================================

def search_patient_by_family(last_name: str):

    return fhir_client.search(
        "Patient",
        {
            "family": last_name
        }
    )


def search_patient_by_given(first_name: str):

    return fhir_client.search(
        "Patient",
        {
            "given": first_name
        }
    )


def search_patient(
    patient_name: str
):
    """
    Search patient using FHIR family and given parameters.
    Example:
        "Sakshi Sahu"
        -> given=Sakshi
        -> family=Sahu
    """
    print(type(patient_name))
    print(patient_name)
    parts = patient_name.strip().split()

    if len(parts) == 1:
        given = parts[0]
        family = ""
    else:
        given = " ".join(parts[:-1])
        family = parts[-1]

    return fhir_client.search(
        "Patient",
        {
            "given": given,
            "family": family
        }
    )
# ==========================================================
# UPDATE
# ==========================================================

def update_patient(patient_id: str, **updates):

    patient = get_patient(patient_id)

    # --------------------------
    # Update Gender
    # --------------------------
    if "gender" in updates:
        patient["gender"] = updates["gender"]

    # --------------------------
    # Update Birth Date
    # --------------------------
    if "birth_date" in updates:
        patient["birthDate"] = updates["birth_date"]

    # --------------------------
    # Update Name
    # --------------------------
    if "first_name" in updates:

        patient["name"][0]["given"] = [
            updates["first_name"]
        ]

    if "last_name" in updates:

        patient["name"][0]["family"] = updates["last_name"]

    # --------------------------
    # Update Active
    # --------------------------
    if "active" in updates:

        patient["active"] = updates["active"]

    return fhir_client.update(
        "Patient",
        patient_id,
        patient
    )


# ==========================================================
# DELETE
# ==========================================================

def delete_patient(patient_id: str):

    return fhir_client.delete(
        "Patient",
        patient_id
    )


# ==========================================================
# PRINT
# ==========================================================

def print_patient(patient):

    print("=" * 50)

    print(
        "Patient ID :",
        patient.get("id")
    )

    name = patient["name"][0]

    print(
        "Name       :",
        name["given"][0],
        name["family"]
    )

    print(
        "Gender     :",
        patient.get("gender")
    )

    print(
        "Birth Date :",
        patient.get("birthDate")
    )

    print("=" * 50)
    
import requests
from fastapi import HTTPException
from fhir.client import fhir_client


def fetch_all_patients():
    try:
        bundle = fhir_client.search(
            "Patient",
            params={"_count": 100}
        )

        patients = []

        for entry in bundle.get("entry", []):
            resource = entry.get("resource", {})

            name = resource.get("name", [])

            full_name = ""

            if name:
                given = name[0].get("given", [])
                family = name[0].get("family", "")

                full_name = " ".join(given)

                if family:
                    full_name += f" {family}"

            patients.append({
                "id": resource.get("id"),
                "name": full_name,
                "gender": resource.get("gender"),
                "birth_date": resource.get("birthDate"),
                "active": resource.get("active", True),
            })

        return {
            "total": bundle.get("total", 0),
            "patients": patients,
        }

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch patients: {str(e)}",
        )