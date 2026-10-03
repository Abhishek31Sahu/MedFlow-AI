"""
Patient Search Service

Shared service used by all workflows.

Responsibilities

- Search patient by name
- Resolve a unique patient
- Handle duplicate patients
"""

from patient.patient import (
    search_patient
)


# ==========================================================
# SEARCH BY NAME
# ==========================================================

def search_patient_by_name(
    patient_name: str
):
    print("search_patient_by_name")
    print(type(patient_name))
    print(patient_name)
    bundle = search_patient(
        patient_name
    )

    patients = []

    if "entry" not in bundle:

        return patients

    for entry in bundle["entry"]:

        resource = entry["resource"]

        patient_id = resource.get("id")

        names = resource.get("name", [])

        full_name = ""

        if names:

            given = " ".join(

                names[0].get(
                    "given",
                    []
                )

            )

            family = names[0].get(
                "family",
                ""
            )

            full_name = (
                f"{given} {family}"
            ).strip()

        patients.append({

            "id": patient_id,

            "name": full_name,

            "gender":
                resource.get(
                    "gender"
                ),

            "birth_date":
                resource.get(
                    "birthDate"
                )

        })

    return patients


# ==========================================================
# RESOLVE PATIENT
# ==========================================================

def resolve_patient(
    patient_name: str
):
    
    patients = search_patient_by_name(
        patient_name
    )

    # --------------------------------------
    # No patient found
    # --------------------------------------

    if len(patients) == 0:

        return {

            "status":
                "not_found",

            "message":
                f"No patient named '{patient_name}' was found.",

            "patient":
                None

        }

    # --------------------------------------
    # One patient
    # --------------------------------------

    if len(patients) == 1:

        return {

            "status":
                "resolved",

            "message":
                "Patient resolved successfully.",

            "patient":
                patients[0]

        }

    # --------------------------------------
    # Multiple patients
    # --------------------------------------

    return {

        "status":
            "multiple",

        "message":
            "Multiple patients found.",

        "patients":
            patients

    }


# ==========================================================
# GET PATIENT ID
# ==========================================================

def resolve_patient_id(
    patient_name: str
):

    result = resolve_patient(
        patient_name
    )

    if result["status"] != "resolved":

        return result

    return {

        "status":
            "resolved",

        "patient_id":
            result["patient"]["id"]

    }