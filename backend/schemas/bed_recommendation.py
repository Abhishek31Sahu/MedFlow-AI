from typing import List

from pydantic import BaseModel


class BedRecommendationRequest(BaseModel):

    patient_id: str

    encounter_id: str

    department: str

    need_icu: bool = False

    need_oxygen: bool = False

    need_ventilator: bool = False

    need_isolation: bool = False

    pediatric: bool = False

    maternity: bool = False


class BedRecommendation(BaseModel):

    bed_id: str

    bed_number: str

    ward: str

    room_number: str

    score: int

    reasons: List[str]


class BedRecommendationResponse(BaseModel):

    recommendations: List[BedRecommendation]
    


class BedAssignmentRequest(BaseModel):

    bed_id: str

    patient_id: str

    encounter_id: str
    



class BedTransferRequest(BaseModel):
    encounter_id: str
    patient_id: str

    from_bed_id: str
    to_bed_id: str

    transfer_reason: str | None = None