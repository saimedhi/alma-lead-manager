from fastapi import FastAPI

from app.database import Base, engine
from app.routers import public_leads, internal_leads

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alma Lead Manager")

app.include_router(public_leads.router)
app.include_router(internal_leads.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
