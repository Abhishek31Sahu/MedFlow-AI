"""
Encounter Service

Business Logic for Encounter Management
"""

from encounter.encounter import (
    create_encounter,
    get_encounter,
    get_patient_encounters,
    get_all_encounters,
    transfer_patient,
    complete_encounter,
    cancel_encounter,
    search_active_encounter,
)

from location.location import search_location


# ==========================================================
# GET LOCATION ID BY NAME
# ==========================================================

def get_location_id_by_name(name: str) -> str | None:

    bundle = search_location(name)

    entries = bundle.get("entry", [])

    if not entries:
        return None

    return entries[0]["resource"]["id"]


# ==========================================================
# CREATE ENCOUNTER
# ==========================================================

def admit_patient(
    patient_id: str,
    practitioner_id: str,
    location_id: str,
    encounter_type: str = "IMP",
    service_type: str = "General Medicine",
    reason: str = "General Checkup",
    priority: str = "routine",
    diagnosis: str | None = None,
    admission_source: str | None = None,
):

    encounter = create_encounter(
        patient_id=patient_id,
        practitioner_id=practitioner_id,
        location_id=location_id,
        encounter_type=encounter_type,
        service_type=service_type,
        reason=reason,
        priority=priority,
        diagnosis=diagnosis,
        admission_source=admission_source,
    )

    return {
        "success": True,
        "message": "Patient admitted successfully.",
        "encounter_id": encounter["id"],
    }


# ==========================================================
# GET SINGLE ENCOUNTER
# ==========================================================

def encounter_details(
    encounter_id: str,
):

    return get_encounter(
        encounter_id
    )


# ==========================================================
# GET ALL ENCOUNTERS
# ==========================================================

def all_encounters():

    bundle = get_all_encounters()

    encounters = []

    for entry in bundle.get("entry", []):

        resource = entry.get("resource", {})

        # ==================================================
        # PATIENT ID
        # ==================================================

        patient_id = None

        subject = resource.get("subject", {})

        patient_reference = subject.get("reference")

        if patient_reference:
            patient_id = patient_reference.split("/")[-1]

        # ==================================================
        # PRACTITIONER ID
        # ==================================================

        practitioner_id = None

        participants = resource.get("participant", [])

        if participants:

            individual = participants[0].get(
                "individual",
                {}
            )

            practitioner_reference = individual.get(
                "reference"
            )

            if practitioner_reference:
                practitioner_id = (
                    practitioner_reference.split("/")[-1]
                )

        # ==================================================
        # ENCOUNTER TYPE
        # ==================================================

        encounter_type = (
            resource.get("class", {})
            .get("code")
        )

        # ==================================================
        # LOCATION ID
        # ==================================================

        location_id = None

        locations = resource.get("location", [])

        if locations:

            location = locations[0].get(
                "location",
                {}
            )

            location_reference = location.get(
                "reference"
            )

            if location_reference:
                location_id = (
                    location_reference.split("/")[-1]
                )

        # ==================================================
        # PERIOD
        # ==================================================

        period = resource.get(
            "period",
            {}
        )

        # ==================================================
        # FINAL RESPONSE
        # ==================================================

        encounters.append({

            "id": resource.get("id"),

            "patient_id": patient_id,

            "practitioner_id": practitioner_id,

            "encounter_type": encounter_type,

            "location_id": location_id,

            "status": resource.get("status"),

            "start": period.get("start"),

            "end": period.get("end"),

        })

    return encounters

# ==========================================================
# ENCOUNTER STATISTICS
# ==========================================================

def encounter_statistics():

    bundle = get_all_encounters()

    total = 0
    active = 0
    completed = 0

    for entry in bundle.get("entry", []):

        resource = entry.get("resource", {})

        status = resource.get("status")

        total += 1

        if status == "in-progress":
            active += 1

        elif status == "finished":
            completed += 1

    return {
        "total": total,
        "active": active,
        "completed": completed,
    }


# ==========================================================
# LIST PATIENT ENCOUNTERS
# ==========================================================

def patient_encounter_history(
    patient_id: str,
):

    bundle = get_patient_encounters(
        patient_id
    )

    encounters = []

    for entry in bundle.get("entry", []):

        resource = entry["resource"]

        location = None

        if resource.get("location"):

            location = (
                resource["location"][0]
                .get("location", {})
                .get("reference")
            )

        encounters.append({

            "id": resource.get("id"),

            "status": resource.get("status"),

            "class": resource.get(
                "class",
                {}
            ).get("code"),

            "start": resource.get(
                "period",
                {}
            ).get("start"),

            "end": resource.get(
                "period",
                {}
            ).get("end"),

            "location": location,

        })

    return encounters


# ==========================================================
# TRANSFER PATIENT
# ==========================================================

def transfer_to_new_location(
    encounter_id: str,
    new_location_id: str,
):

    transfer_patient(
        encounter_id,
        new_location_id,
    )

    return {
        "success": True,
        "message": "Patient transferred.",
    }


# ==========================================================
# COMPLETE ENCOUNTER
# ==========================================================

def discharge_patient(
    encounter_id: str,
):

    complete_encounter(
        encounter_id
    )

    return {
        "success": True,
        "message": "Patient discharged.",
    }


# ==========================================================
# CANCEL ENCOUNTER
# ==========================================================

def cancel_patient_encounter(
    encounter_id: str,
):

    cancel_encounter(
        encounter_id
    )

    return {
        "success": True,
        "message": "Encounter cancelled.",
    }


# ==========================================================
# FIND ACTIVE ENCOUNTER
# ==========================================================

def find_active_encounter(
    patient_id: str,
):

    bundle = search_active_encounter(
        patient_id
    )

    entries = bundle.get(
        "entry",
        []
    )

    if not entries:
        return None

    return entries[0]["resource"]