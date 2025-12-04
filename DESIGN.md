# Alma Lead Manager – System Design

## Goal
A lightweight backend service that:
- Accepts leads submitted by prospects.
- Stores each lead with an initial PENDING status.
- Sends notification emails to both the prospect and an assigned attorney.
- Provides internal, authenticated APIs for attorneys to list all leads and update lead status to REACHED_OUT.


## Functional Requirements

### Public Functionality
- Accept a new lead with the following fields:
  - first_name
  - last_name
  - email 
  - resume_url
- Validate input using Pydantic.
- Store each lead in the database with default status: PENDING.
- Send confirmation email to the prospect.
- Send notification email to the assigned attorney or fallback helpdesk.
- Assumed email is unique for each lead provider.
- Assumed If the lead provider/customer is existing he might already be assigned to a attorney so email must be sent to that particular attorney.  If no assigned attorney present then email notification goes to some help desk attorney  

### Internal Functionality
- List all leads.
- Retrieve a specific lead by ID.
- Update lead status from PENDING to REACHED_OUT.
- Protect all internal endpoints using an API key passed via the X-API-Key header.


## Non-Functional Requirements

### Simplicity
The service prioritizes clarity and ease of understanding. It is designed for an assessment environment rather than high-scale production.

### Performance
- Intended for low to moderate traffic.
- SQLite provides fast local reads/writes but is not suitable for distributed workloads.

### Reliability
- Email sending is synchronous; if SMTP is slow, requests may slow down.
- No retries for failed emails (acceptable for demo).

### Security
- Internal APIs protected by a static API key.
- No login system, OAuth, or JWT since not required for assessment.

### Configuration
- All secrets (SMTP, API key, database URL) are loaded through `.env`.
- No hardcoded credentials.

### Tradeoffs
- SQLite chosen over Postgres for fast setup.
- No background worker for email to keep architecture small.
- API key is sufficient here but not secure enough for real-world access control.


## Data Model

The system uses a single primary table: **leads**.

### leads Table

| Field       | Type       | Description |
|-------------|------------|-------------|
| id          | Integer PK | Auto-incrementing unique identifier |
| first_name  | String     | Prospect first name |
| last_name   | String     | Prospect last name |
| email       | String     | Prospect email address |
| resume_url  | String     | URL to uploaded or hosted resume |
| status      | Enum       | Allowed values: PENDING, REACHED_OUT |
| created_at  | DateTime   | Timestamp of creation |
| updated_at  | DateTime   | Timestamp of latest update |

### Status Enum
The lead status is strictly controlled by a Python Enum:
- `PENDING`
- `REACHED_OUT`

This prevents invalid states and enforces clean business logic.




## API Design

The service exposes two categories of endpoints:

- **Public Endpoints** — used by prospects submitting lead information.
- **Internal Endpoints** — used by attorneys; require API key authentication.

---

### Public API

#### POST /public/leads
Creates a new lead, sends two emails, and returns the stored record.



Request Body
```
{
  "first_name": "Sai",
  "last_name": "Maryada",
  "email": "example@gmail.com",
  "resume_url": "https://drive.google.com/..."
}
```
Response:
```
{
  "id": 1,
  "first_name": "Sai",
  "last_name": "Maryada",
  "email": "example@gmail.com",
  "resume_url": "https://drive.google.com/...",
  "status": "PENDING"
}
```

---
### Internal API (Authenticated)

All internal endpoints require an API key provided in the request header:


If the key is missing or incorrect, the server responds with **401 Unauthorized**.



### 1. GET /internal/leads
Retrieves a list of all leads stored in the system.

**Use case:**  
Attorneys view the full pipeline of prospects.

---

#### 2. GET /internal/leads/{id}
Returns details for a single lead identified by its ID.

**Use case:**  
Attorney views the prospect's full information before reaching out.

---

### 3. PATCH /internal/leads/{id}
Updates the status of a specific lead.

Allowed status change:
`PENDING → REACHED_OUT`

**Request Body:**
```
{
  "status": "REACHED_OUT"
}
```
**Use case:**
Attorney marks that they have contacted the prospect.

## Authentication

The system intentionally keeps authentication simple to meet the assessment requirements.

### Public Endpoints
- All `/public/*` routes are open and do not require authentication.
- These routes are safe because they only allow lead creation.

### Internal Endpoints
All `/internal/*` routes require an API key sent via request header:

`X-API-Key: <INTERNAL_API_KEY>``

### How Authentication Works
- The API key is loaded from environment variables.
- A FastAPI dependency (`verify_api_key`) intercepts each internal request.
- If the header is missing or does not match the valid key:
  - The request is rejected with `401 Unauthorized`.

### Why API Key Auth?
- Lightweight and simple for an assignment.
- Satisfies the requirement of protecting internal UI functionality.
- Avoids the complexity of JWT, OAuth, or user accounts, which are not requested here.

### Tradeoffs
- API keys should not be used for large production systems.
- For real deployments, roles, user accounts, and token-based auth would replace this mechanism.

## Email Notification Flow

The system sends two types of emails whenever a new lead is created.

### 1. Prospect Confirmation Email
Sent to the prospect immediately after submission.

**Purpose:**
- Acknowledge receipt of their information.
- Inform them that an attorney will follow up.

### 2. Attorney Notification Email
Sent to the mapped attorney or a fallback helpdesk email.

**Mapping Logic:**
- A small in-memory dictionary maps known prospect emails to specific attorneys.
- If no match exists, the system uses a default helpdesk address.

### How Emails Are Sent
- SMTP configuration is loaded from environment variables:
  - SMTP_HOST  
  - SMTP_PORT  
  - SMTP_USER  
  - SMTP_PASSWORD  
  - SENDER_EMAIL  
- Uses standard `smtplib` with `starttls` for secure delivery.
- Gmail App Passwords are used instead of real passwords.

### Flow Summary
1. Lead stored in database.
2. Prospect email is sent.
3. Attorney email is sent.
4. API response returns immediately after both emails finish sending.

### Tradeoffs
- Email sending is synchronous to keep architecture simple.
- In production:
  - Emails should be moved to a background worker.
  - Retries should be added for temporary SMTP failures.
  - A dedicated email provider (SES, SendGrid) is recommended.


## Production Considerations

Although this project is intentionally lightweight, several improvements would be required for real-world deployment.

### Database
- **Current:** SQLite (simple, file-based, single-writer limitation)
- **Production:** PostgreSQL or MySQL
  - Supports multiple concurrent writes
  - Better reliability and scaling
  - Easier to run in containers or cloud environments

### Email Delivery
- **Current:** Direct SMTP via Gmail App Password
- **Production Recommendations:**
  - Use a cloud email provider such as AWS SES, SendGrid, Mailgun
  - Offload email sending to a background worker (Celery, RQ, or AWS SQS)
  - Add retry logic and dead-letter queue

### Authentication
- **Current:** Static API key for internal endpoints
- **Production:** 
  - User accounts with roles (Attorney, Admin)
  - Token-based authentication (OAuth2/JWT)
  - Secret rotation and centralized secret management

### Deployment
- Package application in Docker
- Run behind a load balancer (NGINX, AWS ALB)
- Use Gunicorn with multiple Uvicorn workers for scaling
- Configure health checks for container orchestration

### Observability
- Logging: structured logs with timestamps and lead IDs
- Metrics: track lead submissions, email success/failure, response times
- Tracing: minimal tracing for email and DB operations

### Rate Limiting & Abuse Protection
- Public endpoint `/public/leads` should have rate limiting (e.g., 20 req/min per IP)
- Validate resume_url more strictly (file size, type, domain)

### Security
- Move secrets to AWS Secrets Manager or GCP Secret Manager
- HTTPS enforced through load balancer
- Validate all external inputs rigorously

### Future Enhancements
- Add filtering/sorting to internal lead list
- Add pagination for large datasets
- Add event logs for each lead (status changes, timestamps)
- Create a simple UI dashboard using React/Vue for attorneys


## Summary

The Alma Lead Manager is a compact, assessment-friendly backend service designed to capture prospect information, notify attorneys, and support internal lead management with minimal overhead. It uses FastAPI for clean routing and validation, SQLite for simple persistence, and environment-driven SMTP configuration for email delivery. Internal operations are protected by a lightweight API key mechanism.

While intentionally simple, the architecture models real backend patterns:
- layered design (routers, services, models, schemas)
- request validation
- state transitions with enums
- authenticated internal endpoints
- email notifications triggered by domain events

This foundation can easily evolve into a production-ready system by replacing SQLite, introducing asynchronous email pipelines, adding proper authentication, and adopting cloud infrastructure. As it stands, the service fulfills all functional requirements clearly and efficiently while remaining easy to read, test, and extend.



