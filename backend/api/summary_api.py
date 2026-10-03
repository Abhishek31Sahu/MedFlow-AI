from fastapi import APIRouter  

from services.patient_summary_service import (

    patient_summary

)

router = APIRouter(

    prefix="/summary",

    tags=["Summary"]

)

@router.get("/{patient_id}")
def summary(patient_id):

    return patient_summary(patient_id)