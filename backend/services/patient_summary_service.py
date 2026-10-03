"""
Patient Summary Service

Collects patient data from multiple FHIR resources
and returns one structured summary.
"""
import asyncio
from patient.patient import get_patient

from encounter.encounter import (
    get_patient_encounters
)

from medication.medication import (
    get_patient_medications
)

from observation.observation import (
    get_patient_observations
)

from fhir.diagnostic_report import DiagnosticReportFHIR
from observation.observation import get_observation_value
# Add later
#
# from condition.condition import get_conditions
#
# from allergy.allergy import get_allergies
report_service = DiagnosticReportFHIR()

# ==========================================================
# Helpers
# ==========================================================

def _safe_entries(bundle):
    if not isinstance(bundle, dict):
        return []

    return bundle.get("entry", [])

def _get_patient_name(patient):
    """
    Safely extract patient name from a FHIR Patient resource.
    """
    
    print("Extracting patient name from resource:", patient)

    if not isinstance(patient, dict):
        return "Unknown"

    names = patient.get("name", [])

    if not names:
        return "Unknown"

    name = names[0] or {}

    given = name.get("given", [])
    family = name.get("family", "")

    if isinstance(given, list):
        given_text = " ".join(
            str(value)
            for value in given
            if value
        )
    else:
        given_text = str(given or "")

    family_text = str(
        family or ""
    )

    full_name = (
        f"{given_text} {family_text}"
        .strip()
    )

    return full_name or "Unknown"
# ==========================================================
# Patient Summary
# ==========================================================

def patient_summary(patient_id):
    report_service = DiagnosticReportFHIR()
    # ------------------------------------
    # Patient
    # ------------------------------------

    patient = get_patient(patient_id)

    # ------------------------------------
    # Encounters
    # ------------------------------------

    encounters = get_patient_encounters(
        patient_id
    )

    # ------------------------------------
    # Medications
    # ------------------------------------

    medications = get_patient_medications(
        patient_id
    )

    # ------------------------------------
    # Observations
    # ------------------------------------

    observations = get_patient_observations(
        patient_id
    )
    # ------------------------------------
    # Report
    # ------------------------------------
    reports = report_service.get_patient_reports(patient_id)
    # ------------------------------------
    # Build Summary
    # ------------------------------------

    summary = {

        "patient": {

            "id":
                patient["id"],

            "name":
                _get_patient_name(patient),

            "gender":
                patient.get("gender"),

            "birth_date":
                patient.get("birthDate")
        },

        "encounters": [],

        "medications": [],

        "observations": [],
        
        "diagnostic_reports": []

    }

    # ------------------------------------
    # Encounters
    # ------------------------------------

    for entry in _safe_entries(encounters):

        e = entry["resource"]

        summary["encounters"].append({

            "id":
                e["id"],

            "status":
                e["status"],

            "class":
                e["class"]["code"]
        })

    # ------------------------------------
    # Medications
    # ------------------------------------

    for entry in _safe_entries(medications):

        m = entry["resource"]

        summary["medications"].append({

            "id":
                m["id"],

            "medicine":
                m["medicationCodeableConcept"]["text"],

            "status":
                m["status"],

            "dosage":
                m.get(
                    "dosageInstruction",
                    [{}]
                )[0].get(
                    "text",
                    ""
                )
        })

    # ------------------------------------
    # Observations
    # ------------------------------------

    for entry in _safe_entries(observations):

        o = entry["resource"]

        value, unit = get_observation_value(o)

        summary["observations"].append({

            "test":
                o.get("code", {}).get("text"),

            "value":
                value,

            "unit":
                unit,

            "date":
                o.get("effectiveDateTime")
        })
        
    for entry in _safe_entries(reports):

        report = entry["resource"]

        summary["diagnostic_reports"].append({

            "id": report["id"],

            "test_name": report.get("code", {}).get("text"),

            "status": report.get("status"),

            "issued": report.get("issued"),

            "results": len(report.get("result", []))

        })

    return summary