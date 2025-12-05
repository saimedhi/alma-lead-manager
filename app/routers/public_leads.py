from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app import schemas, models, email_service, attorney_service
from app.database import get_db

router = APIRouter(
    prefix="/public/leads",
    tags=["public_leads"],
)

@router.post("", response_model=schemas.LeadOut)
def create_lead(lead_in: schemas.LeadCreate, db: Session = Depends(get_db)):
    lead = models.Lead(
        first_name=lead_in.first_name,
        last_name=lead_in.last_name,
        email=lead_in.email,
        resume_url=lead_in.resume_url,
        status=models.LeadStatus.PENDING,
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    attorney_email = attorney_service.get_attorney_email_for_prospect(lead.email)

    # these two MUST be here
    email_service.send_email_to_prospect(lead.email, lead.id)
    email_service.send_email_to_attorney(attorney_email, lead.id)

    return lead
