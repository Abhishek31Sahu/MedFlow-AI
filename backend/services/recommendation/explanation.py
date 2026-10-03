"""
Recommendation Explanation
"""


class Explanation:

    @staticmethod
    def build(scored_beds):
        """
        Convert scored beds into API response.
        """

        recommendations = []

        for item in scored_beds:

            bed = item["bed"]

            recommendations.append({

                "bed_id": bed.id,

                "bed_number": bed.bed_number,

                "ward": bed.ward,

                "room_number": bed.room_number,

                "department": bed.department,

                "score": item["score"],

                "reasons": item["reasons"]

            })

        return recommendations