# app/attorney_service.py

from typing import Optional
from .attorney_config import ATTORNEY_MAPPINGS, DEFAULT_ATTORNEY


def get_attorney_email_for_prospect(prospect_email: str) -> str:
    mapping = ATTORNEY_MAPPINGS.get(prospect_email)
    if mapping and "email" in mapping:
        return mapping["email"]
    return DEFAULT_ATTORNEY["email"]
