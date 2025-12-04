from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import LeadStatus


class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    resume_url: str


class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None


class LeadOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume_url: str
    status: LeadStatus

    class Config:
        orm_mode = True
