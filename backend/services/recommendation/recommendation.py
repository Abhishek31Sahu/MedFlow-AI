"""
Recommendation Engine
"""

from services.recommendation.eligibility import Eligibility

from services.recommendation.scoring import Scoring

from services.recommendation.ranking import Ranking

from services.recommendation.explanation import Explanation


class RecommendationEngine:

    def recommend(
        self,
        patient,
        beds
    ):
        """
        Complete recommendation pipeline.
        """

        # Step 1
        eligible_beds = Eligibility.filter(
            patient,
            beds
        )

        # Step 2
        scored_beds = Scoring.calculate(
            patient,
            eligible_beds
        )

        # Step 3
        ranked_beds = Ranking.rank(
            scored_beds
        )

        # Step 4
        recommendations = Explanation.build(
            ranked_beds
        )

        return recommendations