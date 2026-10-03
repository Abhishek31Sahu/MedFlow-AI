"""
Bed Eligibility Filter
"""

from typing import List

from models.bed import Bed


class Eligibility:

    @staticmethod
    def filter(patient, beds: List[Bed]) -> List[Bed]:
        """
        Returns only beds that satisfy the patient's
        mandatory requirements.
        """

        eligible_beds = []

        for bed in beds:

            # -----------------------------
            # Bed must be available
            # -----------------------------
            if bed.status != "AVAILABLE":
                continue

            # -----------------------------
            # Bed must not require cleaning
            # -----------------------------
            if bed.cleaning_required:
                continue

            # -----------------------------
            # Oxygen
            # -----------------------------
            if (
                getattr(patient, "need_oxygen", False)
                and
                not bed.oxygen
            ):
                continue

            # -----------------------------
            # Ventilator
            # -----------------------------
            if (
                getattr(patient, "need_ventilator", False)
                and
                not bed.ventilator
            ):
                continue

            # -----------------------------
            # Isolation
            # -----------------------------
            if (
                getattr(patient, "need_isolation", False)
                and
                not bed.isolation
            ):
                continue

            # -----------------------------
            # ICU
            # -----------------------------
            if (
                getattr(patient, "need_icu", False)
                and
                bed.bed_type != "ICU"
            ):
                continue

            # -----------------------------
            # Pediatric
            # -----------------------------
            if (
                getattr(patient, "pediatric", False)
                and
                not bed.pediatric
            ):
                continue

            # -----------------------------
            # Maternity
            # -----------------------------
            if (
                getattr(patient, "maternity", False)
                and
                not bed.maternity
            ):
                continue

            # Passed all mandatory checks
            eligible_beds.append(bed)

        return eligible_beds