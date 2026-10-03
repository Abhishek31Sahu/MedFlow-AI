"""
Location Service
"""

from location.location import (
    create_location,
    get_location,
    search_location,
    delete_location,
)


def add_location(
    name: str,
    description: str = ""
):

    return create_location(
        name=name,
        description=description
    )


def get_location_details(
    location_id: str
):

    return get_location(
        location_id
    )


def search_location_by_name(
    name: str
):

    return search_location(
        name
    )


def remove_location(
    location_id: str
):

    return delete_location(
        location_id
    )
    

def get_or_create_location(
    name: str,
    description: str = ""
):

    bundle = search_location(name)
    print(f"Searching for location with name: {name}")
    print(f"Search results: {bundle}")
    entries = bundle.get("entry", [])

    if entries:

        return entries[0]["resource"]

    return create_location(
        name=name,
        description=description
    )