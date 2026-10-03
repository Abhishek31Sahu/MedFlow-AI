from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from models.laboratory import LaboratoryOrder
from models.enums import (
    LabOrderStatus,
    SampleStatus,
)

from repositories.laboratory_repository import LaboratoryRepository

from schemas.laboratory import (
    CreateLabOrderRequest,
    SubmitLabResultRequest,
)

from fhir.service_request import ServiceRequestFHIR
from fhir.diagnostic_report import DiagnosticReportFHIR

from services.observation_service import add_observation


class LaboratoryService:

    def __init__(self, db: Session):

        self.repo = LaboratoryRepository(db)

        self.service_request = ServiceRequestFHIR()

        self.report = DiagnosticReportFHIR()

    # ======================================================
    # Doctor Workflow
    # ======================================================

    def create_lab_order(
        self,
        request: CreateLabOrderRequest,
    ):

        created_orders = []
        print("Creating laboratory order for patient:", request.patient_id)
        # ---------------------------------------
        # Create one ServiceRequest per test
        # ---------------------------------------

        for test in request.tests:

            # -------------------------------
            # Create FHIR ServiceRequest
            # -------------------------------

            fhir_response = self.service_request.create(
                patient_id=request.patient_id,
                practitioner_id=request.practitioner_id,
                encounter_id=request.encounter_id,
                test_name=test.name,
                test_code=test.code,
                priority=request.priority.value,
                note=request.clinical_note,
            )

            service_request_id = fhir_response["id"]

            # -------------------------------
            # Save Local Record
            # -------------------------------

            order = LaboratoryOrder(

                service_request_id=service_request_id,

                patient_id=request.patient_id,

                encounter_id=request.encounter_id,

                practitioner_id=request.practitioner_id,

                technician_id=None,

                test_code=test.code,

                test_name=test.name,

                priority=request.priority,

                status=LabOrderStatus.PENDING,

                sample_status=SampleStatus.NOT_COLLECTED,

                clinical_note=request.clinical_note,
            )

            created_order = self.repo.create(order)

            created_orders.append(created_order)

        return created_orders

    # ======================================================
    # Pending Orders
    # ======================================================

    def get_pending_orders(self):

        return self.repo.get_pending_orders()

    # ======================================================
    # Get Patient Orders
    # ======================================================

    def get_patient_orders(
        self,
        patient_id: str,
    ):

        return self.repo.get_patient_orders(patient_id)
    
    def get_laboratory_orders(
            self,
            service_request_id: str,
        ):
    
            return self.repo.get_by_service_request(service_request_id)

    # ======================================================
    # Lab Technician Workflow
    # ======================================================

    def submit_results(
        self,
        request: SubmitLabResultRequest,
    ):

        # ---------------------------------------
        # Find Order
        # ---------------------------------------

        order = self.repo.get_by_service_request(
            request.service_request_id
        )

        if order is None:

            raise ValueError(
                "Laboratory order not found."
            )

        observation_ids: List[str] = []

        # ---------------------------------------
        # Create Observation Resources
        # ---------------------------------------

        for parameter in request.parameters:

            observation = add_observation(

                patient_id=order.patient_id,

                encounter_id=order.encounter_id,

                code=parameter.code,

                display=parameter.name,

                value=parameter.value,

                unit=parameter.unit,

            )

            observation_ids.append(
                observation["observation_id"]
            )

        # ---------------------------------------
        # Create Diagnostic Report
        # ---------------------------------------

        report = self.report.create(

            patient_id=order.patient_id,

            encounter_id=order.encounter_id,

            practitioner_id=order.practitioner_id,

            service_request_id=order.service_request_id,

            test_name=order.test_name,

            observation_ids=observation_ids,

        )

        # ---------------------------------------
        # Update ServiceRequest
        # ---------------------------------------

        self.service_request.update_status(

            order.service_request_id,

            "completed",

        )

        # ---------------------------------------
        # Update Local Order
        # ---------------------------------------

        order.status = LabOrderStatus.COMPLETED

        order.sample_status = SampleStatus.RECEIVED

        order.technician_id = request.technician_id

        order.completed_at = datetime.utcnow()

        self.repo.update(order)

        return report

    # ======================================================
    # Report
    # ======================================================

    def get_report(
        self,
        report_id: str,
    ):

        return self.report.get(report_id)

    # ======================================================
    # Pending FHIR Orders
    # ======================================================

    def get_pending_fhir_orders(self):

        return self.service_request.search_pending()

    # ======================================================
    # Patient Reports
    # ======================================================

    def get_report_by_patient_id(
        self,
        patient_id: str,
    ):

        return self.report.get_patient_reports(
            patient_id
        )

    # ======================================================
    # ServiceRequest Reports
    # ======================================================

    def get_report_by_service_request(
        self,
        service_request_id: str,
    ):

        return self.report.get_by_service_request(
            service_request_id=service_request_id
        )