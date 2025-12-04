# app/routers/internal_leads.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


from app import schemas, models
from app.database import get_db
from app.deps import verify_api_key

router = APIRouter(
    prefix="/internal/leads",
    tags=["internal_leads"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("", response_model=List[schemas.LeadOut])
def list_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()


@router.get("/{lead_id}", response_model=schemas.LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()


@router.patch("/{lead_id}", response_model=schemas.LeadOut)
def update_lead_status(
    lead_id: int,
    update: schemas.LeadUpdate,
    db: Session = Depends(get_db),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if update.status:
        lead.status = update.status
    db.commit()
    db.refresh(lead)
    return lead
