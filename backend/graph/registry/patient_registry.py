"""
Patient Registry
"""

from services.patient_service import (

    add_patient,

    patient_details,

    edit_patient,

    remove_patient

)

FUNCTIONS = {

    "add_patient": add_patient,

    "patient_details": patient_details,

    "edit_patient": edit_patient,

    "remove_patient": remove_patient

}