"""
Appointment Booking Workflow Router
"""

from graph.workflows.appointment_booking.state import (
    AppointmentBookingState
)


def route_after_patient(
    state: AppointmentBookingState
):

    if state.get("error"):

        return "response"

    return "next"


def route_after_practitioner(
    state: AppointmentBookingState
):

    if state.get("error"):

        return "response"

    return "next"


def route_after_availability(
    state: AppointmentBookingState
):

    if state.get("error"):

        return "response"

    return "next"


def route_after_confirmation(
    state: AppointmentBookingState
):

    if state.get(
        "booking_confirmed"
    ) is True:

        return "create"

    return "response"


def route_after_creation(
    state: AppointmentBookingState
):

    if state.get("error"):

        return "response"

    return "response"