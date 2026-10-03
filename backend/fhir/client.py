"""
FHIR Client

Reusable CRUD methods for the Aidbox FHIR server.
"""

import time
import requests

from config import (
    AIDBOX_URL,
    AIDBOX_CLIENT_ID,
    AIDBOX_CLIENT_SECRET,
    FHIR_BASE_URL,
)


class FHIRClient:

    def __init__(self):
        self.base_url = FHIR_BASE_URL
        self._token = None
        self._expires_at = 0

    # ============================================
    # AUTH
    # ============================================
    def _get_token(self):
        # reuse the token until 60 seconds before it expires
        if self._token and time.time() < self._expires_at - 60:
            return self._token

        response = requests.post(
            f"{AIDBOX_URL}/auth/token",
            json={
                "client_id": AIDBOX_CLIENT_ID,
                "client_secret": AIDBOX_CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()
        data = response.json()
        self._token = data["access_token"]
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return self._token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/fhir+json",
            "Accept": "application/fhir+json",
        }

    def _check(self, response):
        if not response.ok:
            print("Status Code:", response.status_code)
            print("FHIR Error:")
            print(response.text)
            response.raise_for_status()

    # ============================================
    # CREATE
    # ============================================
    def create(self, resource_type, resource):
        url = f"{self.base_url}/{resource_type}"
        response = requests.post(url, json=resource, headers=self._headers())
        self._check(response)
        return response.json()

    # ============================================
    # READ ONE
    # ============================================
    def read(self, resource_type, resource_id):
        url = f"{self.base_url}/{resource_type}/{resource_id}"
        response = requests.get(url, headers=self._headers())
        self._check(response)
        return response.json()

    # ============================================
    # SEARCH
    # ============================================
    def search(self, resource_type, params=None):
        url = f"{self.base_url}/{resource_type}"
        response = requests.get(url, headers=self._headers(), params=params)
        self._check(response)
        return response.json()

    # ============================================
    # UPDATE
    # ============================================
    def update(self, resource_type, resource_id, resource):
        url = f"{self.base_url}/{resource_type}/{resource_id}"
        response = requests.put(url, json=resource, headers=self._headers())
        self._check(response)
        return response.json()

    # ============================================
    # DELETE
    # ============================================
    def delete(self, resource_type, resource_id):
        url = f"{self.base_url}/{resource_type}/{resource_id}"
        response = requests.delete(url, headers=self._headers())
        self._check(response)
        return response.status_code


# Singleton instance
fhir_client = FHIRClient()