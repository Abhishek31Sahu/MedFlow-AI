from typing import List

from fhir.client import FHIRClient


class DiagnosticReportFHIR:

    def __init__(self):
        self.client = FHIRClient()

    # ======================================================
    # Create Diagnostic Report
    # ======================================================

    def create(
        self,
        patient_id: str,
        encounter_id: str,
        practitioner_id: str,
        service_request_id: str,
        test_name: str,
        observation_ids: List[str],
    ):

        result = {
            "resourceType": "DiagnosticReport",
            "status": "final",

            "code": {
                "text": test_name
            },

            "subject": {
                "reference": f"Patient/{patient_id}"
            },

            "encounter": {
                "reference": f"Encounter/{encounter_id}"
            },

            "performer": [
                {
                    "reference": f"Practitioner/{practitioner_id}"
                }
            ],

            "basedOn": [
                {
                    "reference": f"ServiceRequest/{service_request_id}"
                }
            ],

            "result": [
                {
                    "reference": f"Observation/{obs}"
                }
                for obs in observation_ids
            ]
        }

        return self.client.create(
            "DiagnosticReport",
            result,
        )

    # ======================================================
    # Get Diagnostic Report
    # ======================================================

    def get(
        self,
        report_id: str,
    ):

        return self.client.read(
            "DiagnosticReport",
            report_id,
        )

    # ======================================================
    # Get Patient Reports
    # ======================================================

    def get_patient_reports(
        self,
        patient_id: str,
    ):

        return self.client.search(
            "DiagnosticReport",
            {
                "subject": f"Patient/{patient_id}"
            },
        )

    # ======================================================
    # Get Reports by ServiceRequest
    # ======================================================

    def get_by_service_request(
        self,
        service_request_id: str,
    ):

        return self.client.search(
            "DiagnosticReport",
            {
                "based-on": f"ServiceRequest/{service_request_id}"
            },
        )