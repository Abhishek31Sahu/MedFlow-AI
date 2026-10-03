
import os

# ==========================================================
# FHIR SERVER
# ==========================================================

AIDBOX_URL = os.environ["AIDBOX_URL"]              
AIDBOX_CLIENT_ID = os.environ["AIDBOX_CLIENT_ID"] 
AIDBOX_CLIENT_SECRET = os.environ["AIDBOX_CLIENT_SECRET"]

FHIR_BASE_URL = f"{AIDBOX_URL}/fhir"
