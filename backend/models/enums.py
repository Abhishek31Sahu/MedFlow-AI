from enum import Enum


class BedStatus(Enum):

    AVAILABLE = "AVAILABLE"

    OCCUPIED = "OCCUPIED"

    RESERVED = "RESERVED"

    CLEANING = "CLEANING"

    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    
    
class BedType(Enum):

    GENERAL = "GENERAL"

    ICU = "ICU"

    HDU = "HDU"

    EMERGENCY = "EMERGENCY"

    NICU = "NICU"

    PICU = "PICU"
    
class GenderPolicy(str, Enum):

    ANY = "ANY"

    MALE = "MALE"

    FEMALE = "FEMALE"
    
class AllocationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class AllocationType(str, Enum):
    ADMISSION = "ADMISSION"
    TRANSFER = "TRANSFER"
    MANUAL = "MANUAL"
    
class LabOrderStatus(str, Enum):
    PENDING = "PENDING"
    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SampleStatus(str, Enum):
    NOT_COLLECTED = "NOT_COLLECTED"
    COLLECTED = "COLLECTED"
    REJECTED = "REJECTED"
    RECEIVED = "RECEIVED"


class Priority(str, Enum):
    ROUTINE = "ROUTINE"
    URGENT = "URGENT"
    STAT = "STAT"
    
class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"
    LAB_TECHNICIAN = "lab_technician"
    PHARMACIST = "pharmacist"