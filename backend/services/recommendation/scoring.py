"""
Bed Scoring Engine
"""

from models.enums import BedType


class Scoring:

    @staticmethod
    def calculate(patient, beds):
        """
        Calculate a score for each eligible bed.
        """

        scored_beds = []

        for bed in beds:

            score = 0

            reasons = []

            # ---------------------------------
            # Department Match
            # ---------------------------------

            if patient.department == bed.department:

                score += 30

                reasons.append("Department Match")

            # ---------------------------------
            # General Bed Preference
            # ---------------------------------

            if (
                not getattr(patient, "need_icu", False)
                and bed.bed_type == BedType.GENERAL.value
            ):

                score += 10

                reasons.append("General Bed")

            # ---------------------------------
            # ICU Match
            # ---------------------------------

            if (
                getattr(patient, "need_icu", False)
                and bed.bed_type == BedType.ICU.value
            ):

                score += 20

                reasons.append("ICU Bed")

            # ---------------------------------
            # Oxygen
            # ---------------------------------

            if (
                getattr(patient, "need_oxygen", False)
                and bed.oxygen
            ):

                score += 20

                reasons.append("Oxygen Available")

            # ---------------------------------
            # Ventilator
            # ---------------------------------

            if (
                getattr(patient, "need_ventilator", False)
                and bed.ventilator
            ):

                score += 10

                reasons.append("Ventilator")

            # ---------------------------------
            # Isolation
            # ---------------------------------

            if (
                getattr(patient, "need_isolation", False)
                and bed.isolation
            ):

                score += 20

                reasons.append("Isolation Room")

            # ---------------------------------
            # Cardiac Monitor
            # ---------------------------------

            if bed.cardiac_monitor:

                score += 5

                reasons.append("Cardiac Monitor")

            # ---------------------------------
            # Dialysis
            # ---------------------------------

            if (
                getattr(patient, "need_dialysis", False)
                and bed.dialysis
            ):

                score += 15

                reasons.append("Dialysis Support")

            scored_beds.append(
                {
                    "bed": bed,
                    "score": score,
                    "reasons": reasons
                }
            )

        return scored_beds