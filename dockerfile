# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system deps if needed later (kept minimal for now)
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first for better build caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY app ./app

# Env for uvicorn
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]