from services.medication_service import (

    add_medication,

    discontinue_medication,

    change_dosage,

    list_active_medications,

    medication_history

)

FUNCTIONS = {

    "add_medication": add_medication,

    "discontinue_medication": discontinue_medication,

    "change_dosage": change_dosage,

    "list_active_medications": list_active_medications,

    "medication_history": medication_history

}