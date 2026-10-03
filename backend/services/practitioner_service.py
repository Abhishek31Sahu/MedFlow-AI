"""
Practitioner Service
"""

from practitioner.practitioner import (
    create_practitioner,
    get_practitioner,
    search_practitioner,
    update_practitioner,
    delete_practitioner,
)


# ==========================================================
# REGISTER PRACTITIONER
# ==========================================================

def register_practitioner(
    first_name,
    last_name="",
    gender=None,
    phone=None,
    email=None,
    designation=None,
):
    practitioner = create_practitioner(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        phone=phone,
        email=email,
        designation=designation,
    )

    practitioner_id = practitioner.get("id")

    if not practitioner_id:
        raise RuntimeError(
            "FHIR Practitioner created but ID was not returned."
        )

    return {
        "success": True,
        "message": "Practitioner Registered",
        "practitioner_id": practitioner_id,
        "practitioner": practitioner,
    }


# ==========================================================
# GET PRACTITIONER DETAILS
# ==========================================================

def practitioner_details(
    practitioner_id,
):
    return get_practitioner(
        practitioner_id
    )


# ==========================================================
# SEARCH PRACTITIONER
# ==========================================================

def search_practitioners(
    name,
):
    """
    Search Practitioners by name.

    Returns the FHIR Bundle returned by HAPI FHIR.
    """

    return search_practitioner(
        name
    )


# ==========================================================
# RESOLVE PRACTITIONER
# ==========================================================

def resolve_practitioner(practitioner_name):
    print("Searching practitioner:", practitioner_name)

    bundle = search_practitioner(practitioner_name)

    print("FHIR bundle:", bundle)

    entries = bundle.get("entry", [])

    print("FHIR entries:", entries)

    # ======================================================
    # NOT FOUND
    # ======================================================

    if not entries:
        print("no entries found")

        return {
            "status": "not_found",
            "message": (
                f"No practitioner found for "
                f"'{practitioner_name}'."
            ),
            "practitioners": [],
        }

    # ======================================================
    # EXTRACT PRACTITIONERS
    # ======================================================

    practitioners = []

    for entry in entries:

        practitioner = entry.get(
            "resource"
        )

        if not practitioner:
            continue

        practitioner_id = practitioner.get(
            "id"
        )

        if not practitioner_id:
            continue

        # --------------------------------------------------
        # Extract name
        # --------------------------------------------------

        name_data = (
            practitioner
            .get("name", [{}])[0]
        )

        given = " ".join(
            name_data.get(
                "given",
                []
            )
        )

        family = name_data.get(
            "family",
            ""
        )

        full_name = (
            f"{given} {family}"
        ).strip()

        # --------------------------------------------------
        # Extract designation
        # --------------------------------------------------

        designation = None

        qualifications = (
            practitioner.get(
                "qualification",
                []
            )
        )

        if qualifications:

            designation = (
                qualifications[0]
                .get("code", {})
                .get("text")
            )

        # --------------------------------------------------
        # Extract contact
        # --------------------------------------------------

        phone = None
        email = None

        telecom = practitioner.get(
            "telecom",
            []
        )

        for contact in telecom:

            system = contact.get(
                "system"
            )

            value = contact.get(
                "value"
            )

            if system == "phone":
                phone = value

            elif system == "email":
                email = value

        practitioners.append(
            {
                "id": practitioner_id,
                "name": full_name,
                "first_name": given,
                "last_name": family,
                "gender": practitioner.get(
                    "gender"
                ),
                "phone": phone,
                "email": email,
                "designation": designation,
                "resource": practitioner,
            }
        )

    # ======================================================
    # NO VALID PRACTITIONERS
    # ======================================================

    if not practitioners:

        return {
            "status": "not_found",
            "message": (
                f"No valid practitioner found for "
                f"'{practitioner_name}'."
            ),
            "practitioners": [],
        }

    # ======================================================
    # SINGLE PRACTITIONER
    # ======================================================

    if len(practitioners) == 1:

        practitioner = practitioners[0]

        return {
            "status": "resolved",
            "practitioner": practitioner,
            "practitioners": practitioners,
        }

    # ======================================================
    # MULTIPLE PRACTITIONERS
    # ======================================================

    return {
        "status": "multiple",
        "message": (
            f"Multiple practitioners found for "
            f"'{practitioner_name}'."
        ),
        "practitioners": practitioners,
    }


# ==========================================================
# UPDATE PRACTITIONER
# ==========================================================

def edit_practitioner(
    practitioner_id,
    first_name,
    last_name="",
    gender=None,
    phone=None,
    email=None,
    designation=None,
):
    return update_practitioner(
        practitioner_id=practitioner_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        phone=phone,
        email=email,
        designation=designation,
    )


# ==========================================================
# DELETE PRACTITIONER
# ==========================================================

def remove_practitioner(
    practitioner_id,
):
    return delete_practitioner(
        practitioner_id
    )