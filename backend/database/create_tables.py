"""
Create Database Tables
"""

from database.database import Base, engine

# Import ALL models
from models.bed import Bed
from models.bed_allocation import BedAllocation
from models.lab_parameter import LabParameter
from models.lab_template import LabTemplate
from models.laboratory_result import LaboratoryResult
from models.laboratory import LaboratoryOrder
from models.user import User
from models.practitioner_schedule import PractitionerSchedule


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Tables created successfully."
    )


if __name__ == "__main__":

    create_tables()