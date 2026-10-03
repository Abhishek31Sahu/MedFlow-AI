from pydantic import BaseModel


class RescheduleInput(BaseModel):

    appointment_id: str | None = None

    date: str | None = None

    start_time: str | None = None

    end_time: str | None = None

    confirmation: bool | None = None