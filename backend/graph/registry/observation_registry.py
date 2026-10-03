from services.observation_service import (

    add_observation,

    get_observation_details,

    list_patient_observations,

    search_test,

    latest_test_result,

    change_observation_value,

    remove_observation

)

FUNCTIONS = {

    "add_observation": add_observation,

    "get_observation": get_observation_details,

    "list_patient_observations": list_patient_observations,

    "search_test": search_test,

    "latest_test_result": latest_test_result,

    "change_observation_value": change_observation_value,

    "remove_observation": remove_observation

}