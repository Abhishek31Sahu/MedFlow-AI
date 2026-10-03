"""
Extract Appointment Booking Input
"""

from graph.workflows.appointment_booking.state import (
    AppointmentBookingState
)

from graph.workflows.appointment_booking.prompts.booking_prompt import (
    BOOKING_PROMPT
)

from graph.workflows.appointment_booking.models.booking_input import (
    BookingInput
)

from graph.utils.parser import (
    ask_llm
)


def extract_input(
    state: AppointmentBookingState
) -> AppointmentBookingState:

    history = state.get(
        "messages",
        []
    )[-10:]

    history_text = "\n".join(
        f"{m.type}: {m.content}"
        for m in history
    )

    prompt = f"""
{BOOKING_PROMPT}

Conversation so far:

{history_text}

User Query:

{state["user_query"]}
"""

    booking = ask_llm(
        prompt,
        BookingInput
    )
    print(booking.model_dump());
    state["workflow_data"] = (
        booking.model_dump()
    )

    state["workflow_status"] = (
        "IN_PROGRESS"
    )

    state["current_step"] = (
        "BOOKING_INPUT_EXTRACTED"
    )

    return state