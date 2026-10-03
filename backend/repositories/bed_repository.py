
from sqlalchemy.orm import Session

from models.bed import Bed
from models.enums import BedStatus,BedType


class BedRepository:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------
    # CREATE
    # -----------------------------

    def create_bed(self, bed_data):

        data = bed_data.model_dump()

        data["bed_type"] = data["bed_type"].value

        data["gender_policy"] = data["gender_policy"].value

        bed = Bed(**data)

        self.db.add(bed)

        self.db.commit()

        self.db.refresh(bed)

        return bed

    # -----------------------------
    # READ
    # -----------------------------

    def get_bed(self, bed_id):

        return (
            self.db.query(Bed)
            .filter(Bed.id == bed_id)
            .first()
        )

    def get_bed_encounter(self,encounter_id):
        
        return(
            self.db.query(Bed)
            .filter(Bed.encounter_id==encounter_id)
            .first()
        )
    
    def get_all_beds(self):

        return self.db.query(Bed).all()

    def get_candidate_beds(self):

        return (
            self.db.query(Bed)
            .filter(
                Bed.status == BedStatus.AVAILABLE.value,
                Bed.cleaning_required == False
            )
            .all()
        )

    # -----------------------------
    # UPDATE
    # -----------------------------

    def update_bed(self, bed_id, data):

        bed = self.get_bed(bed_id)

        if not bed:
            return None

        for key, value in data.items():
            setattr(bed, key, value)

        self.db.commit()

        self.db.refresh(bed)

        return bed

    # -----------------------------
    # DELETE
    # -----------------------------

    def delete_bed(self, bed_id):

        bed = self.get_bed(bed_id)

        if not bed:
            return False

        self.db.delete(bed)

        self.db.commit()

        return True

    # -----------------------------
    # RESERVE
    # -----------------------------

    def reserve_bed(self, bed_id):

        bed = self.get_bed(bed_id)

        if not bed:
            raise Exception("Bed not found")

        bed.status = BedStatus.RESERVED.value

        self.db.commit()

        self.db.refresh(bed)

        return bed

    def release_reserved_bed(self, bed_id):

        bed = self.get_bed(bed_id)

        if not bed:
            raise Exception("Bed not found")

        bed.status = BedStatus.AVAILABLE.value

        self.db.commit()

        self.db.refresh(bed)

        return bed

    # -----------------------------
    # ASSIGN
    # -----------------------------

    def assign_bed(
        self,
        bed_id,
        patient_id,
        encounter_id
    ):

        bed = self.get_bed(bed_id)

        if not bed:
            raise Exception("Bed not found")

        bed.status = BedStatus.OCCUPIED.value

        bed.occupied_by = patient_id

        bed.encounter_id = encounter_id

        self.db.commit()

        self.db.refresh(bed)

        return bed

    # -----------------------------
    # RELEASE
    # -----------------------------

    def release_bed(self, bed_id):

        bed = self.get_bed(bed_id)

        if not bed:
            raise Exception("Bed not found")

        bed.status = BedStatus.CLEANING.value

        bed.occupied_by = None

        bed.encounter_id = None

        self.db.commit()

        self.db.refresh(bed)

        return bed

    def release_bed_by_encounter(self,encounter_id):
        bed = self.get_bed_encounter(encounter_id)
        
        if not bed:
            raise Exception("Bed not found")
        
        bed.status = BedStatus.CLEANING.value
        
        bed.occupied_by = None

        bed.encounter_id = None

        self.db.commit()

        self.db.refresh(bed)

        return bed
    # -----------------------------
    # CLEANING
    # -----------------------------

    def mark_cleaning(self, bed_id):

        bed = self.get_bed(bed_id)

        bed.status = BedStatus.CLEANING.value

        self.db.commit()

        self.db.refresh(bed)

        return bed

    def mark_available(self, bed_id):

        bed = self.get_bed(bed_id)

        bed.status = BedStatus.AVAILABLE.value

        self.db.commit()

        self.db.refresh(bed)

        return bed

    # -----------------------------
    # DASHBOARD
    # -----------------------------

    def get_available_beds(self):

        return (
            self.db.query(Bed)
            .filter(
                Bed.status == BedStatus.AVAILABLE.value
            )
            .all()
        )

    def get_occupied_beds(self):

        return (
            self.db.query(Bed)
            .filter(
                Bed.status == BedStatus.OCCUPIED.value
            )
            .all()
        )

    from models.enums import BedStatus, BedType

    def get_bed_statistics(self):

        return {
            # Overall
            "total_beds": self.db.query(Bed).count(),

            "available": self.db.query(Bed)
            .filter(Bed.status == BedStatus.AVAILABLE.value)
            .count(),

            "occupied": self.db.query(Bed)
            .filter(Bed.status == BedStatus.OCCUPIED.value)
            .count(),

            "reserved": self.db.query(Bed)
            .filter(Bed.status == BedStatus.RESERVED.value)
            .count(),

            "cleaning": self.db.query(Bed)
            .filter(Bed.status == BedStatus.CLEANING.value)
            .count(),

            # Bed Types
            "icu": self.db.query(Bed)
            .filter(Bed.bed_type == BedType.ICU.value)
            .count(),

            "general": self.db.query(Bed)
            .filter(Bed.bed_type == BedType.GENERAL.value)
            .count(),

            # Equipment
            "oxygen": self.db.query(Bed)
            .filter(Bed.oxygen == True)
            .count(),

            "ventilator": self.db.query(Bed)
            .filter(Bed.ventilator == True)
            .count(),

            "isolation": self.db.query(Bed)
            .filter(Bed.isolation == True)
            .count(),

            "cardiac_monitor": self.db.query(Bed)
            .filter(Bed.cardiac_monitor == True)
            .count(),

            "dialysis": self.db.query(Bed)
            .filter(Bed.dialysis == True)
            .count(),

            # Special Beds
            "pediatric": self.db.query(Bed)
            .filter(Bed.pediatric == True)
            .count(),

            "maternity": self.db.query(Bed)
            .filter(Bed.maternity == True)
            .count(),
        }