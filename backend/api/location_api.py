from fastapi import APIRouter

from pydantic import BaseModel

from services.location_service import (
    add_location,
    get_location_details,
    search_location_by_name,
    remove_location,
)

router = APIRouter(
    prefix="/locations",
    tags=["Location"]
)


class LocationRequest(BaseModel):

    name: str

    description: str = ""


@router.post("/")
def create_location_api(
    request: LocationRequest
):

    return add_location(

        name=request.name,

        description=request.description

    )


@router.get("/{location_id}")
def read_location(
    location_id: str
):

    return get_location_details(
        location_id
    )


@router.get("/")
def search_location(
    name: str
):

    return search_location_by_name(
        name
    )


@router.delete("/{location_id}")
def delete_location_api(
    location_id: str
):

    return remove_location(
        location_id
    )