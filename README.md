This repository contains a lightweight backend service built for the alma.  
start with **this README** and then refer to below documentation for better understanding of this project:

- **DESIGN.md** – System architecture, requirements, data model, production notes    
- **ArchitectureDiagram.md** – Visual overview of system flow  
- **DockerSetup.md** – Instructions to build and run the service using Docker  

- **Interactive API documentation** (Swagger UI):  
Use http://127.0.0.1:8000/docsz

- **[Here’s the link to the demo videos for this application](https://github.com/saimedhi/alma-lead-manager/pull/2#issue-3697257016)**

------


This README gives you the high-level overview.  
All deeper details are in the linked files above.

## Alma Lead Manager

- A lightweight backend application built with FastAPI to manage incoming leads.
Prospects submit their information publicly, and attorneys can review and update lead status through authenticated internal APIs.
The system also sends email notifications to both the prospect and the assigned attorney.

### Features

- Public endpoint for lead submission

- Internal API for attorneys to view and update leads

- Email notifications on every new lead

- Simple API key authentication for internal routes

- SQLite for persistence


### Tech Stack

FastAPI

SQLAlchemy

Pydantic

SQLite

SMTP email (Gmail App Password)

Python 3.11

### Running the App

- Install dependencies:
`pip install -r requirements.txt`

- Create a .env file with SMTP settings, API key, and DB URL

- Start the app:
`uvicorn app.main:app --reload`

- Open documentation:
http://127.0.0.1:8000/docs

### Public API

- `POST /public/leads`
 Accepts a new lead, saves it, and sends email notifications.

### Internal API (Requires header X-API-Key)

- `GET /internal/leads – list all leads`
- `GET /internal/leads/{id}` – view a particular lead
- `PATCH /internal/leads/{id}` – update status by attorney

### Status Flow done by attorney

PENDING → REACHED_OUT

### Folder Structure
```
app/
– routers/ (public_leads.py, internal_leads.py)
– models.py
– schemas.py
– email_service.py
– attorney_service.py
– deps.py
– main.py
```

### Limitations

- No UI for internal users and external users

- SQLite is not scalable

- Emails sent synchronously

- Simple API key auth

- Move to Postgres

- Background email worker

- No stronger auth 

- Logging, metrics, rate limiting can be done
