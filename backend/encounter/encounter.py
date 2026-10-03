"""
Encounter CRUD Operations
"""

from datetime import datetime

from fhir.client import fhir_client
from location.location import search_location


# ==========================================================
# CREATE ENCOUNTER
# ==========================================================

def create_encounter(

    patient_id: str,

    practitioner_id: str,

    location_id: str,

    encounter_type: str = "IMP",

    service_type: str = "General Medicine",

    reason: str = "General Checkup",

    priority: str = "routine",

    diagnosis: str | None = None,

    admission_source: str | None = None,

    discharge_disposition: str | None = None,

):

    encounter = {

        "resourceType": "Encounter",

        "status": "in-progress",

        "class": {

            "system":
            "http://terminology.hl7.org/CodeSystem/v3-ActCode",

            "code": encounter_type

        },

        "type": [

            {

                "text": encounter_type

            }

        ],

        "priority": {

            "text": priority

        },

        "serviceType": {

            "text": service_type

        },

        "subject": {

            "reference": f"Patient/{patient_id}"

        },

        "participant": [

            {

                "individual": {

                    "reference":f"Practitioner/{practitioner_id}"

                }

            }

        ],

        "period": {

            "start": datetime.utcnow().isoformat()

        },

        "reasonCode": [

            {

                "text": reason

            }

        ],

        "location": [

            {

                "location": {

                    "reference":
                    f"Location/{location_id}"

                }

            }

        ]

    }

    # Diagnosis

    if diagnosis:

        encounter["diagnosis"] = [

            {

                "condition": {

                    "display": diagnosis

                }

            }

        ]

    # Hospitalization

    encounter["hospitalization"] = {}

    if admission_source:

        encounter["hospitalization"]["admitSource"] = {

            "text": admission_source

        }

    if discharge_disposition:

        encounter["hospitalization"]["dischargeDisposition"] = {

            "text": discharge_disposition

        }

    return fhir_client.create(
        "Encounter",
        encounter
    )


# ==========================================================
# READ
# ==========================================================

def get_encounter(encounter_id):

    return fhir_client.read(
        "Encounter",
        encounter_id
    )


# ==========================================================
# SEARCH BY PATIENT
# ==========================================================

def get_patient_encounters(patient_id):

    return fhir_client.search(
        "Encounter",
        {
            "patient": patient_id
        }
    )


# ==========================================================
# UPDATE LOCATION
# ==========================================================

def transfer_patient(
    encounter_id,
    location_id
):

    encounter = get_encounter(
        encounter_id
    )

    encounter["location"] = [
        {
            "location": {
                "reference":
                f"Location/{location_id}"
            }
        }
    ]

    return fhir_client.update(
        "Encounter",
        encounter_id,
        encounter
    )


# ==========================================================
# COMPLETE ENCOUNTER
# ==========================================================

def complete_encounter(
    encounter_id
):

    encounter = get_encounter(
        encounter_id
    )

    encounter["status"] = "finished"

    encounter["period"]["end"] = (
        datetime.utcnow().isoformat()
    )

    return fhir_client.update(
        "Encounter",
        encounter_id,
        encounter
    )


# ==========================================================
# CANCEL
# ==========================================================

def cancel_encounter(
    encounter_id
):

    encounter = get_encounter(
        encounter_id
    )

    encounter["status"] = "cancelled"

    return fhir_client.update(
        "Encounter",
        encounter_id,
        encounter
    )


# ==========================================================
# PRINT
# ==========================================================

def print_encounter(encounter):

    print("=" * 60)

    print(
        "Encounter ID:",
        encounter.get("id")
    )

    print(
        "Status:",
        encounter.get("status")
    )

    print(
        "Patient:",
        encounter["subject"]["reference"]
    )

    print(
        "Class:",
        encounter["class"]["code"]
    )

    if "period" in encounter:

        print(
            "Start:",
            encounter["period"].get("start")
        )

        print(
            "End:",
            encounter["period"].get("end")
        )

    if "location" in encounter:

        print(
            "Location:",
            encounter["location"][0]["location"]["reference"]
        )

    print("=" * 60)
    
    
    
# ==========================================================
# SEARCH ACTIVE ENCOUNTER
# ==========================================================

def search_active_encounter(
    patient_id: str
):

    return fhir_client.search(

        "Encounter",

        params={

            "patient": patient_id,

            "status": "in-progress"

        }

    )
    
# ==========================================================
# SEARCH BY PATIENT
# ==========================================================

def get_patient_encounters(patient_id):

    return fhir_client.search(
        "Encounter",
        {
            "patient": patient_id
        }
    )


# ==========================================================
# GET ALL ENCOUNTERS
# ==========================================================

def get_all_encounters():

    return fhir_client.search(
        "Encounter",
        {}
    )