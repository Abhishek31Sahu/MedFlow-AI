from typing import Optional

from pydantic import BaseModel

from models.enums import (
    BedStatus,
    BedType,
    GenderPolicy
)


class BedCreate(BaseModel):

    bed_number: str

    ward: str

    room_number: str

    department: str

    floor: Optional[str] = None

    location_id: str

    bed_type: BedType = BedType.GENERAL

    gender_policy: GenderPolicy = GenderPolicy.ANY

    oxygen: bool = False

    ventilator: bool = False

    isolation: bool = False

    cardiac_monitor: bool = False

    dialysis: bool = False

    pediatric: bool = False

    maternity: bool = False


class BedUpdate(BaseModel):

    status: Optional[BedStatus] = None

    occupied_by: Optional[str] = None

    encounter_id: Optional[str] = None

    cleaning_required: Optional[bool] = None


class BedResponse(BaseModel):

    id: str

    bed_number: str

    ward: str

    room_number: str

    department: str

    floor: Optional[str]

    location_id: str

    bed_type: BedType

    status: BedStatus

    gender_policy: GenderPolicy

    oxygen: bool

    ventilator: bool

    isolation: bool

    cardiac_monitor: bool

    dialysis: bool

    pediatric: bool

    maternity: bool

    cleaning_required: bool

    occupied_by: Optional[str]

    encounter_id: Optional[str]

    class Config:
        from_attributes = True