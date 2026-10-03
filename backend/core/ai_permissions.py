# core/ai_permissions.py

from models.enums import UserRole


# ==========================================================
# AGENT ACCESS
# ==========================================================
#
# This is the first authorization layer.
# It decides whether a role can enter an AI agent at all.
#
# Function-level authorization below makes the final decision.
# ==========================================================

AI_AGENT_ROLES = {

    "patient": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
        UserRole.LAB_TECHNICIAN,
        UserRole.PHARMACIST,
    },
    "patient_search": {
    UserRole.ADMIN,
    UserRole.DOCTOR,
    UserRole.NURSE,
    UserRole.RECEPTIONIST,
    UserRole.LAB_TECHNICIAN,
    UserRole.PHARMACIST,
},

    "encounter": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
    },

    "medication": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.PHARMACIST,
    },

    "observation": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
    },

    "summary": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
    },

    "appointment": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
    },
}


# ==========================================================
# WORKFLOW AUTHORIZATION
# ==========================================================

AI_WORKFLOW_ROLES = {

    "patient_admission": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "patient_discharge": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "patient_transfer": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
    },

    "lab_order": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "appointment_booking": {
        UserRole.ADMIN,
        UserRole.RECEPTIONIST,
    },

    "appointment_reschedule": {
        UserRole.ADMIN,
        UserRole.RECEPTIONIST,
    },
}


# ==========================================================
# FUNCTION AUTHORIZATION
# ==========================================================

AI_FUNCTION_ROLES = {

    # ------------------------------------------------------
    # PATIENT
    # ------------------------------------------------------

    "patient_details": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
        UserRole.LAB_TECHNICIAN,
        UserRole.PHARMACIST,
    },

    "add_patient": {
        UserRole.ADMIN,
        UserRole.RECEPTIONIST,
    },

    "edit_patient": {
        UserRole.ADMIN,
        UserRole.RECEPTIONIST,
        UserRole.DOCTOR,
    },

    "remove_patient": {
        UserRole.ADMIN,
    },


    # ------------------------------------------------------
    # ENCOUNTER
    # ------------------------------------------------------

    "create_encounter": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "get_encounter": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
    },

    "transfer_patient": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
    },

    "complete_encounter": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "cancel_encounter": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },


    # ------------------------------------------------------
    # MEDICATION
    # ------------------------------------------------------

    "add_medication": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "discontinue_medication": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "change_dosage": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
    },

    "list_active_medications": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.PHARMACIST,
    },

    "medication_history": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.PHARMACIST,
    },


    # ------------------------------------------------------
    # OBSERVATION
    # ------------------------------------------------------

    "add_observation": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
    },

    "get_observation": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
    },

    "list_patient_observations": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
    },

    "search_test": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
    },

    "latest_test_result": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.LAB_TECHNICIAN,
    },

    "change_observation_value": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.LAB_TECHNICIAN,
    },

    "remove_observation": {
        UserRole.ADMIN,
    },


    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    "patient_summary": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
    },


    # ------------------------------------------------------
    # APPOINTMENT
    # ------------------------------------------------------

    "check_availability": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
    },

    "appointment_details": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
    },

    "patient_appointments": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
    },

    "practitioner_appointments": {
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
    },

    "cancel_appointment": {
        UserRole.ADMIN,
        UserRole.RECEPTIONIST,
    },
}


# ==========================================================
# HELPERS
# ==========================================================

def normalize_role(role) -> UserRole:

    if isinstance(role, UserRole):
        return role

    return UserRole(role)


# ==========================================================
# CHECK AGENT ACCESS
# ==========================================================

def can_access_agent(
    role,
    agent_name: str,
) -> bool:

    role = normalize_role(role)

    allowed_roles = AI_AGENT_ROLES.get(
        agent_name,
        set(),
    )

    return role in allowed_roles


# ==========================================================
# CHECK WORKFLOW ACCESS
# ==========================================================

def can_access_workflow(
    role,
    workflow_name: str,
) -> bool:

    role = normalize_role(role)

    allowed_roles = AI_WORKFLOW_ROLES.get(
        workflow_name,
        set(),
    )

    return role in allowed_roles


# ==========================================================
# CHECK FUNCTION ACCESS
# ==========================================================

def can_execute_function(
    role,
    function_name: str,
) -> bool:

    role = normalize_role(role)

    allowed_roles = AI_FUNCTION_ROLES.get(
        function_name,
        set(),
    )

    return role in allowed_roles


# ==========================================================
# AUTHORIZATION ERROR
# ==========================================================

def authorization_error(
    state,
    message: str,
):
    """
    Store authorization failure in graph state.
    Response Agent can convert this into a normal AI response.
    """
    state["authorization_denied"] = True
    print(f"Authorization error: {state['authorization_denied']}")
    state["error"] = message

    state["result"] = {
        "success": False,
        "data": None,
    }

    return state


# ==========================================================
# FUNCTION AUTHORIZATION
# ==========================================================

def authorize_function(
    state,
    function_name: str,
) -> bool:

    role = state.get("user_role")

    if not role:

        authorization_error(
            state,
            "Authenticated user role is missing.",
        )

        return False

    try:

        allowed = can_execute_function(
            role,
            function_name,
        )

    except ValueError:

        authorization_error(
            state,
            f"Invalid user role: {role}",
        )

        return False

    if not allowed:

        authorization_error(
            state,
            (
                f"You do not have permission to perform "
                f"'{function_name}'."
            ),
        )

        return False

    return True