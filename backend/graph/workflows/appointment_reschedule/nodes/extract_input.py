from graph.workflows.appointment_reschedule.models.reschedule_input import (
    RescheduleInput,
)

from graph.workflows.appointment_reschedule.prompts.reschedule_prompt import (
    RESCHEDULE_PROMPT,
)


def extract_input(
    state,
    llm,
):

    # --------------------------------------------------
    # Current user message
    # --------------------------------------------------

    query =state.get(
        "user_query",
        "",
    )

    print(
        "\n========== RESCHEDULE EXTRACTION =========="
    )
    print(
        "QUERY:",
        query,
    )

    # --------------------------------------------------
    # Preserve previous workflow data
    # --------------------------------------------------

    workflow_data = {
        **state.get(
            "workflow_data",
            {},
        )
    }

    current_status = state.get(
        "workflow_status"
    )

    # --------------------------------------------------
    # LLM extraction
    # --------------------------------------------------

    extractor = llm.with_structured_output(
        RescheduleInput
    )

    extracted = extractor.invoke(
        [
            {
                "role": "system",
                "content": RESCHEDULE_PROMPT,
            },
            {
                "role": "user",
                "content": query,
            },
        ]
    )

    print(
        "LLM OUTPUT:",
        extracted,
    )

    # --------------------------------------------------
    # Merge extracted values
    # --------------------------------------------------

    if extracted.appointment_id:
        workflow_data["appointment_id"] = (
            extracted.appointment_id
        )

    if extracted.date:
        workflow_data["date"] = (
            extracted.date
        )

    if extracted.start_time:
        workflow_data["start_time"] = (
            extracted.start_time
        )

    if extracted.end_time:
        workflow_data["end_time"] = (
            extracted.end_time
        )

    if extracted.confirmation is not None:
        workflow_data["confirmation"] = (
            extracted.confirmation
        )

    # --------------------------------------------------
    # Find missing fields
    # --------------------------------------------------

    missing_fields = []

    if not workflow_data.get(
        "appointment_id"
    ):
        missing_fields.append(
            "appointment_id"
        )

    if not workflow_data.get(
        "date"
    ):
        missing_fields.append(
            "date"
        )

    if not workflow_data.get(
        "start_time"
    ):
        missing_fields.append(
            "start_time"
        )

    # --------------------------------------------------
    # Confirmation stage
    # --------------------------------------------------

    if current_status == "WAITING_FOR_CONFIRMATION":

        confirmation = workflow_data.get(
            "confirmation"
        )

        if confirmation is True:

            return {
                "workflow_data": workflow_data,
                "active_workflow":
                    "appointment_reschedule",
                "workflow_status":
                    "CONFIRMED",
                "confirmation": True,
                "missing_fields": [],
                "result": None,
            }

        if confirmation is False:

            return {
                "workflow_data": workflow_data,
                "active_workflow":
                    "appointment_reschedule",
                "workflow_status":
                    "CANCELLED",
                "confirmation": False,
                "missing_fields": [],
                "result": {
                    "success": True,
                    "title": "Cancelled",
                    "message": (
                        "The appointment "
                        "reschedule has been cancelled."
                    ),
                },
            }

        return {
            "workflow_data": workflow_data,
            "active_workflow":
                "appointment_reschedule",
            "workflow_status":
                "WAITING_FOR_CONFIRMATION",
            "missing_fields": [],
            "result": {
                "success": True,
                "title":
                    "Confirmation Required",
                "message": (
                    "Please confirm whether "
                    "you want to reschedule "
                    "the appointment."
                ),
            },
        }

    # --------------------------------------------------
    # Missing appointment ID
    # --------------------------------------------------

    if "appointment_id" in missing_fields:

        return {
            "workflow_data": workflow_data,
            "active_workflow":
                "appointment_reschedule",
            "workflow_status":
                "WAITING_FOR_APPOINTMENT_ID",
            "missing_fields":
                ["appointment_id"],
            "result": {
                "success": True,
                "title":
                    "Appointment ID Required",
                "message": (
                    "Please provide the "
                    "appointment ID you want "
                    "to reschedule."
                ),
            },
        }

    # --------------------------------------------------
    # Missing date
    # --------------------------------------------------

    if "date" in missing_fields:

        return {
            "workflow_data": workflow_data,
            "active_workflow":
                "appointment_reschedule",
            "workflow_status":
                "WAITING_FOR_DATE",
            "missing_fields":
                ["date"],
            "result": {
                "success": True,
                "title": "Date Required",
                "message": (
                    "What date would you like "
                    f"to reschedule appointment "
                    f"{workflow_data['appointment_id']} "
                    "to?"
                ),
            },
        }

    # --------------------------------------------------
    # Missing time
    # --------------------------------------------------

    if "start_time" in missing_fields:

        return {
            "workflow_data": workflow_data,
            "active_workflow":
                "appointment_reschedule",
            "workflow_status":
                "WAITING_FOR_TIME",
            "missing_fields":
                ["start_time"],
            "result": {
                "success": True,
                "title": "Time Required",
                "message": (
                    "What time would you like "
                    "to reschedule the appointment "
                    "to?"
                ),
            },
        }

    # --------------------------------------------------
    # Everything available
    # --------------------------------------------------

    return {
        "workflow_data": workflow_data,
        "active_workflow":
            "appointment_reschedule",
        "workflow_status":
            "READY",
        "missing_fields": [],
        "result": None,
    }