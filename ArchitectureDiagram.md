### Alma Lead Manager – Architecture Diagram

Below is a simple architecture overview (Due to time limitation written as markdown file. Could improve below if time permits):

#### System Architecture 

Prospect → Public API (/public/leads)
→ Validation (Pydantic)
→ Database (SQLite)
→ Email Service
→ Prospect receives confirmation email
→ Attorney receives notification email

Attorney → Internal API (/internal/leads)
→ Auth Layer (API key check)
→ Database (SQLite)
→ Update lead status

#### Main Components

FastAPI main application

Routers

public_leads

internal_leads

Services

email_service

attorney_service

Database layer (SQLAlchemy)

Config + environment variables

#### Data Flow (Lead Creation)

Prospect submits lead

Lead validated and stored

Email sent to prospect

Email sent to attorney

Lead returned with status PENDING

#### Data Flow (Attorney Workflow)

Attorney authenticates via X-API-Key

Lists leads

Opens individual lead

Updates status to REACHED_OUT

#### Deployment Overview (Recommended)

Containerized via Docker

Reverse proxy for HTTPS

Load balancer

Replace SQLite with Postgres

Use email provider (SES/Mailgun)

Use secret manager for environment variables