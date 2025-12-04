### Docker Setup for Alma Lead Manager

#### Build and Run

docker build -t alma-lead-manager .
docker run -p 8000:8000 --env-file .env alma-lead-manager
