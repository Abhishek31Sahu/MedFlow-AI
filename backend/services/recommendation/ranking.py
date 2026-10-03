"""
Bed Ranking Engine
"""


class Ranking:

    @staticmethod
    def rank(scored_beds, limit: int = 3):
        """
        Sort beds by score (highest first)
        and return the top N.
        """

        return sorted(
            scored_beds,
            key=lambda bed: bed["score"],
            reverse=True
        )[:limit]