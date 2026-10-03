import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from api.patient_api import router as patient_router
from api.medication_api import router as medication_router
from api.admission_api import router as admission_router
from api.observation_api import router as observation_router
from api.summary_api import router as summary_router
from api.encounter_api import router as encounter_router
from api.practitioner_api import router as practitioner_router
from api.ai_api import router as ai_router
from api.location_api import router as location_router
from api.discharge_api import router as discharge_router
from api.bed_api import router as bed_router
from api.allocation_api import router as allocation_router
from api.template_api import router as template_router
from api.laboratory_api import router as laborartory_router
from api.auth_api import router as auth_router
from api.user_api import router as user_router
from api.dashboard_api import router as dashboard_router
from api.practitioner_schedule_api import router as practitioner_schedule_router
from api.appointment_api import router as appointment_router
from contextlib import asynccontextmanager

from fastapi import FastAPI

from graph.graph import build_graph
from graph.persistence import checkpointer_context
from services.graph_service import graph_service
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
@asynccontextmanager
async def lifespan(app: FastAPI):

    async with checkpointer_context(DATABASE_URL) as checkpointer:

        graph_service.graph = (
            build_graph()
            .compile(checkpointer=checkpointer)
        )

        yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://med-flow-ai-yhhn.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ai_router)

app.include_router(dashboard_router)

app.include_router(laborartory_router)

app.include_router(discharge_router)

app.include_router(location_router)

app.include_router(practitioner_router)

app.include_router(patient_router)

app.include_router(medication_router)

app.include_router(admission_router)

app.include_router(observation_router)

app.include_router(summary_router)

app.include_router(encounter_router)

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(
    bed_router
)
app.include_router(
    practitioner_schedule_router
)

app.include_router(appointment_router)

app.include_router(
    allocation_router
)
app.include_router(template_router)
@app.get("/")
def home():

    return {

        "message":

        "Hospital Workflow AI Running"
    }