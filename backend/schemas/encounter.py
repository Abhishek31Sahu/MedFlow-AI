from pydantic import BaseModel


class EncounterInfo(BaseModel):
    id: str
    status: str
    encounter_class: str
    start: str | None = None
    end: str | None = None
    location: str | None = None