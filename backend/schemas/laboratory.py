from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from models.enums import (
    LabOrderStatus,
    Priority,
    SampleStatus,
)


# ==========================================================
# Doctor -> Create Lab Order
# ==========================================================

class LabTest(BaseModel):
    code: str
    name: str


class CreateLabOrderRequest(BaseModel):
    patient_id: str
    encounter_id: str|  None = None
    practitioner_id: str

    tests: list[LabTest]

    priority: Priority

    clinical_note: str | None = None


# ==========================================================
# Response after creating order
# ==========================================================

class LabOrderResponse(BaseModel):
    id: UUID

    service_request_id: str

    patient_id: str

    encounter_id: Optional[str]

    practitioner_id: str

    technician_id: Optional[str]

    test_name: str

    priority: Priority

    status: LabOrderStatus

    sample_status: SampleStatus

    clinical_note: Optional[str]

    ordered_at: datetime

    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ==========================================================
# Pending Orders
# ==========================================================

class PendingLabOrder(BaseModel):
    id: UUID

    service_request_id: str

    patient_id: str

    test_name: str

    priority: Priority

    status: LabOrderStatus

    ordered_at: datetime

    class Config:
        from_attributes = True


# ==========================================================
# Lab Technician submits result
# ==========================================================

class LabParameter(BaseModel):
    code: str
    name: str

    value: float

    unit: str

    reference_range: Optional[str] = None


class SubmitLabResultRequest(BaseModel):
    service_request_id: str

    technician_id: str

    parameters: List[LabParameter]


# ==========================================================
# Diagnostic Report Response
# ==========================================================

class DiagnosticReportResponse(BaseModel):
    diagnostic_report_id: str

    service_request_id: str

    generated_by: str

    generated_at: datetime

    class Config:
        from_attributes = True


# ==========================================================
# Search
# ==========================================================

class LabOrderFilter(BaseModel):
    patient_id: Optional[str] = None

    practitioner_id: Optional[str] = None

    technician_id: Optional[str] = None

    status: Optional[LabOrderStatus] = None

    priority: Optional[Priority] = None