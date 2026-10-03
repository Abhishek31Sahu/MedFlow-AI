"""
Location CRUD Operations
"""

from fhir.client import fhir_client


# ==========================================================
# CREATE LOCATION
# ==========================================================

def create_location(
    name: str,
    description: str = "",
    status: str = "active"
):

    resource = {

        "resourceType": "Location",

        "status": status,

        "name": name,

        "description": description

    }

    return fhir_client.create(
        "Location",
        resource
    )


# ==========================================================
# READ LOCATION
# ==========================================================

def get_location(
    location_id: str
):

    return fhir_client.read(
        "Location",
        location_id
    )


# ==========================================================
# SEARCH LOCATION
# ==========================================================

def search_location(
    name: str
):

    return fhir_client.search(

        "Location",

        {
            "name": name
        }

    )


# ==========================================================
# DELETE LOCATION
# ==========================================================

def delete_location(
    location_id: str
):

    return fhir_client.delete(
        "Location",
        location_id
    )