"""
Practitioner CRUD Operations
"""

from fhir.client import fhir_client


# ==========================================================
# CREATE PRACTITIONER
# ==========================================================

def create_practitioner(
    first_name: str,
    last_name: str = "",
    gender: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    designation: str | None = None,
):
    """
    Create a FHIR Practitioner and return the created resource.

    The returned resource should contain the FHIR Practitioner ID
    in:

        practitioner["id"]
    """

    resource = {
        "resourceType": "Practitioner",
        "active": True,
        "name": [
            {
                "use": "official",
                "family": last_name or "",
                "given": [first_name],
            }
        ],
    }

    # ------------------------------------------------------
    # Gender
    # ------------------------------------------------------
    if gender:
        resource["gender"] = gender

    # ------------------------------------------------------
    # Phone / Email
    # ------------------------------------------------------
    telecom = []

    if phone:
        telecom.append(
            {
                "system": "phone",
                "value": phone,
                "use": "work",
            }
        )

    if email:
        telecom.append(
            {
                "system": "email",
                "value": email,
                "use": "work",
            }
        )

    if telecom:
        resource["telecom"] = telecom

    # ------------------------------------------------------
    # Designation
    # ------------------------------------------------------
    if designation:
        resource["qualification"] = [
            {
                "code": {
                    "text": designation
                }
            }
        ]

    return fhir_client.create(
        "Practitioner",
        resource
    )


# ==========================================================
# READ
# ==========================================================

def get_practitioner(practitioner_id):
    """
    Get Practitioner by FHIR Practitioner ID.
    """

    return fhir_client.read(
        "Practitioner",
        practitioner_id
    )


# ==========================================================
# SEARCH
# ==========================================================

def search_practitioner(name):
    name = name.strip()

    # Remove doctor prefix
    prefixes = [
        "Dr. ",
        "Dr ",
        "Doctor ",
        "doctor ",
    ]

    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):].strip()
            break

    parts = name.split()

    # Full name: Rahul Sharma
    if len(parts) >= 2:
        given = parts[0]
        family = " ".join(parts[1:])

        return fhir_client.search(
            "Practitioner",
            {
                "given": given,
                "family": family,
            },
        )

    # Single name: Rahul
    return fhir_client.search(
        "Practitioner",
        {
            "name": name,
        },
    )


# ==========================================================
# UPDATE
# ==========================================================

def update_practitioner(
    practitioner_id,
    first_name,
    last_name,
    gender=None,
    phone=None,
    email=None,
    designation=None,
):
    """
    Update an existing Practitioner.
    """

    practitioner = get_practitioner(
        practitioner_id
    )

    # ------------------------------------------------------
    # Name
    # ------------------------------------------------------
    practitioner["name"] = [
        {
            "use": "official",
            "family": last_name or "",
            "given": [first_name],
        }
    ]

    # ------------------------------------------------------
    # Gender
    # ------------------------------------------------------
    if gender:
        practitioner["gender"] = gender
    else:
        practitioner.pop("gender", None)

    # ------------------------------------------------------
    # Telecom
    # ------------------------------------------------------
    telecom = []

    if phone:
        telecom.append(
            {
                "system": "phone",
                "value": phone,
                "use": "work",
            }
        )

    if email:
        telecom.append(
            {
                "system": "email",
                "value": email,
                "use": "work",
            }
        )

    if telecom:
        practitioner["telecom"] = telecom
    else:
        practitioner.pop("telecom", None)

    # ------------------------------------------------------
    # Designation
    # ------------------------------------------------------
    if designation:
        practitioner["qualification"] = [
            {
                "code": {
                    "text": designation
                }
            }
        ]
    else:
        practitioner.pop("qualification", None)

    return fhir_client.update(
        "Practitioner",
        practitioner_id,
        practitioner
    )


# ==========================================================
# DELETE
# ==========================================================

def delete_practitioner(
    practitioner_id
):
    """
    Delete Practitioner by FHIR Practitioner ID.
    """

    return fhir_client.delete(
        "Practitioner",
        practitioner_id
    )