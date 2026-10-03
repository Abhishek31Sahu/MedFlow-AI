from typing import Optional

from fhir.client import FHIRClient


class ServiceRequestFHIR:

    def __init__(self):
        self.client = FHIRClient()

    def create(
        self,
        patient_id: str,
        practitioner_id: str,
        test_code: str,
        test_name: str,
        priority: str = "routine",
        encounter_id: Optional[str] = None,
        note: Optional[str] = None,
    ) -> dict:

        resource = {
            "resourceType": "ServiceRequest",
            "status": "active",
            "intent": "order",
            "priority": priority.lower(),
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "requester": {
                "reference": f"Practitioner/{practitioner_id}"
            },
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": test_code,
                        "display": test_name
                    }
                ],
                "text": test_name
            }
        }

        if encounter_id:
            resource["encounter"] = {
                "reference": f"Encounter/{encounter_id}"
            }

        if note:
            resource["note"] = [
                {
                    "text": note
                }
            ]

        return self.client.create(
            "ServiceRequest",
            resource,
        )

    def get(
        self,
        service_request_id: str,
    ) -> dict:

        return  self.client.read(
            "ServiceRequest",
            service_request_id,
        )

    def update_status(
        self,
        service_request_id: str,
        status: str,
    ) -> dict:

        resource =  self.get(service_request_id)

        resource["status"] = status

        return  self.client.update(
            "ServiceRequest",
            service_request_id,
            resource,
        )

    def search_pending(self):

        return  self.client.search(
            "ServiceRequest",
            {
                "status": "active"
            },
        )