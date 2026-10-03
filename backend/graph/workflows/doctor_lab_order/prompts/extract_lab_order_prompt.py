EXTRACT_LAB_ORDER_PROMPT = """
You are a hospital laboratory assistant.

Extract the laboratory order information.

Return only structured data.

Conversation so far:
{history}

Doctor Request:
{query}

Extract:

- patient_name
- tests
- priority
- clinical_note

If patient_name is not in the current request, check the conversation above
for a patient already discussed and reuse that name. Only leave it blank if
no patient appears anywhere in the conversation.

For tests:

Return a list.

Example:

[
    {{
        "code": "57021-8",
        "name": "Complete Blood Count"
    }},
    {{
        "code": "2339-0",
        "name": "Blood Glucose"
    }}
]

If code not available in query then return empty string.

Priority Rules

If doctor mentions:

urgent
immediately
as soon as possible

→ URGENT

If doctor mentions:

stat
emergency
critical

→ STAT

Otherwise

→ ROUTINE
"""
