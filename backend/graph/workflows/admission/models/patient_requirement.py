from pydantic import BaseModel
class PatientRequirements(BaseModel):

    department: str

    need_icu: bool = False

    need_oxygen: bool = False

    need_ventilator: bool = False

    need_isolation: bool = False

    pediatric: bool = False

    maternity: bool = False