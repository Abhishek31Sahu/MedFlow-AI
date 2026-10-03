"""
Observation Service

Business logic for Observation Management
"""

from observation.observation import (
    create_observation,
    get_observation,
    get_patient_observations,
    get_observation_by_test,
    latest_observation,
    update_observation,
    delete_observation,
)


# ==========================================================
# ADD OBSERVATION
# ==========================================================

def add_observation(
    patient_id: str,
    
    code: str,
    display: str,
    value,
    unit: str,
    encounter_id: str | None = None,
    practitioner_id: str | None = None,
    category: str = "laboratory",
    interpretation: str | None = None,
    note: str | None = None,
    low_reference=None,
    high_reference=None,
):

    observation = create_observation(
        patient_id=patient_id,
        practitioner_id=practitioner_id,
        encounter_id=encounter_id ,
        code=code,
        display=display,
        value=value,
        unit=unit,
        category=category,
        interpretation=interpretation,
        note=note,
        low_reference=low_reference,
        high_reference=high_reference,
    )

    return {
        "success": True,
        "message": "Observation Created",
        "observation_id": observation["id"],
    }


# ==========================================================
# GET OBSERVATION
# ==========================================================

def get_observation_details(
    observation_id: str
):

    return get_observation(
        observation_id
    )


# ==========================================================
# GET ALL OBSERVATIONS OF PATIENT
# ==========================================================

def list_patient_observations(
    patient_id: str
):

    bundle = get_patient_observations(
        patient_id
    )

    observations = []

    if "entry" not in bundle:
        return observations

    for entry in bundle["entry"]:

        resource = entry["resource"]

        observations.append({

            "id":
                resource["id"],

            "test":
                resource["code"]["text"],

            "status":
                resource["status"],

            "value":
                resource["valueQuantity"]["value"],

            "unit":
                resource["valueQuantity"]["unit"],

            "date":
                resource["effectiveDateTime"]

        })

    return observations


# ==========================================================
# SEARCH TEST
# ==========================================================

def search_test(
    patient_id: str,
    test_name: str
):

    return get_observation_by_test(
        patient_id,
        test_name
    )


# ==========================================================
# LATEST RESULT
# ==========================================================

def latest_test_result(
    patient_id: str,
    test_name: str
):

    return latest_observation(
        patient_id,
        test_name
    )


# ==========================================================
# UPDATE VALUE
# ==========================================================

def change_observation_value(
    observation_id: str,
    value
):

    update_observation(
        observation_id,
        value
    )

    return {

        "success": True,

        "message": "Observation Updated"

    }


# ==========================================================
# DELETE
# ==========================================================

def remove_observation(
    observation_id: str
):

    delete_observation(
        observation_id
    )

    return {

        "success": True,

        "message": "Observation Deleted"

    }