from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.enums import (
    AllocationStatus,
    AllocationType
)


class BedAllocationCreate(BaseModel):

    bed_id: str

    patient_id: str

    encounter_id: str

    allocated_by: Optional[str] = None

    allocation_type: AllocationType = AllocationType.ADMISSION

    recommendation_score: Optional[float] = None

    recommendation_reason: Optional[str] = None


class BedAllocationUpdate(BaseModel):

    released_at: Optional[datetime] = None

    status: Optional[AllocationStatus] = None


class BedAllocationResponse(BaseModel):

    id: str

    bed_id: str

    patient_id: str

    encounter_id: str

    allocated_by: Optional[str]

    allocation_type: AllocationType

    recommendation_score: Optional[float]

    recommendation_reason: Optional[str]

    allocated_at: datetime

    released_at: Optional[datetime]

    status: AllocationStatus

    class Config:
        from_attributes = True