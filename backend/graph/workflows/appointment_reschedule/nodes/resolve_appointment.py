from services.appointment_service import (
    get_appointment,
    get_patient_id_from_appointment
)



def resolve_appointment(state):
    """
    Resolve the appointment and extract the related
    patient and practitioner IDs.

    No patient lookup is performed here.
    """

    workflow_data = {
        **state.get("workflow_data", {})
    }

    appointment_id = workflow_data.get(
        "appointment_id"
    )

    print(
        "\n========== RESOLVE APPOINTMENT =========="
    )
    print(
        "appointment_id:",
        appointment_id,
    )

    # --------------------------------------------------
    # Appointment ID missing
    # --------------------------------------------------

    if not appointment_id:
        return {
            "active_workflow":
                "appointment_reschedule",

            "workflow_status":
                "WAITING_FOR_APPOINTMENT_ID",

            "workflow_data":
                workflow_data,

            "missing_fields":
                ["appointment_id"],

            "result": {
                "success": True,
                "title":
                    "Appointment ID Required",
                "message": (
                    "Please provide the appointment "
                    "ID you want to reschedule."
                ),
            },
        }

    # --------------------------------------------------
    # Fetch appointment
    # --------------------------------------------------

    try:
        appointment = get_appointment(
            appointment_id
        )

        print("APPOINTMENT:")
        print(appointment)

    except Exception as e:

        print(
            "GET APPOINTMENT ERROR:",
            repr(e),
        )

        return {
            "active_workflow":
                "appointment_reschedule",

            "workflow_status":
                "ERROR",

            "error":
                str(e),

            "result": {
                "success": False,
                "title":
                    "Appointment Not Found",
                "message": (
                    f"Appointment {appointment_id} "
                    "could not be found."
                ),
            },
        }

    # --------------------------------------------------
    # Validate appointment
    # --------------------------------------------------

    if not isinstance(
        appointment,
        dict,
    ):
        return {
            "active_workflow":
                "appointment_reschedule",

            "workflow_status":
                "ERROR",

            "result": {
                "success": False,
                "title":
                    "Invalid Appointment",
                "message": (
                    "The appointment data returned "
                    "from FHIR is invalid."
                ),
            },
        }

    # --------------------------------------------------
    # Extract participants
    # --------------------------------------------------

    participants = appointment.get(
        "participant",
        [],
    )

    patient_id = None
    practitioner_id = None

    for participant in participants:

        if not isinstance(
            participant,
            dict,
        ):
            continue

        actor = participant.get(
            "actor",
            {},
        )

        if not isinstance(
            actor,
            dict,
        ):
            continue

        reference = actor.get(
            "reference"
        )

        if not reference:
            continue

        # -----------------------------
        # Patient/1452
        # -----------------------------

        if reference.startswith(
            "Patient/"
        ):

            patient_id = (
                reference.split(
                    "/",
                    1,
                )[1]
            )

        # -----------------------------
        # Practitioner/1551
        # -----------------------------

        elif reference.startswith(
            "Practitioner/"
        ):

            practitioner_id = (
                reference.split(
                    "/",
                    1,
                )[1]
            )

    print(
        "PATIENT ID:",
        patient_id,
    )

    print(
        "PRACTITIONER ID:",
        practitioner_id,
    )

    # --------------------------------------------------
    # Validate practitioner
    # --------------------------------------------------

    if not practitioner_id:

        return {
            "active_workflow":
                "appointment_reschedule",

            "workflow_status":
                "ERROR",

            "result": {
                "success": False,
                "title":
                    "Practitioner Not Found",
                "message": (
                    "The appointment does not "
                    "contain a practitioner."
                ),
            },
        }

    # --------------------------------------------------
    # Save resolved information
    # --------------------------------------------------

    workflow_data[
        "appointment_id"
    ] = appointment_id

    workflow_data[
        "patient_id"
    ] = patient_id

    workflow_data[
        "practitioner_id"
    ] = practitioner_id

    return {
        "active_workflow":
            "appointment_reschedule",

        "workflow_status":
            "APPOINTMENT_RESOLVED",

        "workflow_data":
            workflow_data,

        "appointment_id":
            appointment_id,

        "patient_id":
            patient_id,

        "practitioner_id":
            practitioner_id,

        "appointment":
            appointment,

        "missing_fields":
            [],

        "error":
            None,
    }