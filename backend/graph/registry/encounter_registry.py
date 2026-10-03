"""
Encounter Function Registry
"""

from services.encounter_service import (

    admit_patient,

    encounter_details,

    transfer_to_new_location,

    discharge_patient,

    cancel_patient_encounter

)


FUNCTIONS = {

    "create_encounter": admit_patient,

    "get_encounter": encounter_details,

    "transfer_patient": transfer_to_new_location,

    "complete_encounter": discharge_patient,

    "cancel_encounter": cancel_patient_encounter

}