"""
Patient Service

Business logic for Patient operations.
"""

from patient.patient import (
    create_patient,
    get_patient,
    update_patient,
    delete_patient,
)


# ==========================================================
# CREATE
# ==========================================================

def add_patient(
    first_name: str,
    last_name: str,
    gender: str,
    birth_date: str,
):

    patient = create_patient(

        first_name=first_name,

        last_name=last_name,

        gender=gender,

        birth_date=birth_date,

    )

    return patient


# ==========================================================
# READ
# ==========================================================

def patient_details(
    patient_id: str,
):

    return get_patient(
        patient_id
    )


# ==========================================================
# UPDATE
# ==========================================================

def edit_patient(
    patient_id: str,
    first_name=None,
    last_name=None,
    gender=None,
    birth_date=None,
):

    return update_patient(

        patient_id=patient_id,

        first_name=first_name,

        last_name=last_name,

        gender=gender,

        birth_date=birth_date,

    )


# ==========================================================
# DELETE
# ==========================================================

def remove_patient(
    patient_id: str,
):

    return delete_patient(
        patient_id
    )