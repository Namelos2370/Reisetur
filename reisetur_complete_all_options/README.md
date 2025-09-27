# Reisetür - Candidate Management Platform (Django)

This repository contains a minimal, deployable Django project ready to be extended for Reisetür.
It implements:
- Candidate model with file uploads (ID, passport, diploma, CV)
- Basic REST API endpoints (Django REST Framework)
- Simple frontend form (Django template) to submit a candidate
- Admin interface for staff to manage candidates
- Dockerfile and docker-compose for easy deployment

## Quickstart (development)
1. Copy `.env.example` to `.env` and adjust settings.
2. Build image and run with Docker Compose:
   ```
   docker-compose build
   docker-compose up
   ```
3. Run migrations and create superuser (inside container or locally):
   ```
   docker-compose run web python manage.py migrate
   docker-compose run web python manage.py createsuperuser
   ```
4. Visit:
   - Frontend form: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - API: http://localhost:8000/api/candidates/

## Files included
- Dockerfile, docker-compose.yml
- Django project `reisetur` and app `candidates`
- Example .env

This is a starting point. Extend with:
- Email/WhatsApp notifications (Twilio or WhatsApp Cloud API)
- Token-based auth / social auth
- Additional automations (Celery + Redis)
- GDPR features (data retention, consent logs, downloads encryption)


## Étape 1 — Authentification, worker et notifications (déjà ajoutés)
Ce commit ajoute :
- JWT (djangorestframework-simplejwt) pour sécuriser l'API.
  - Endpoints: /api/token/ , /api/token/refresh/
- OpenAPI + Swagger via drf-spectacular : /api/schema/ et /api/docs/
- Celery + Redis (scaffold) et une tâche d'exemple `send_whatsapp_message` et `send_email_notification`.
- docker-compose inclut désormais un service `redis` et `worker` pour Celery.
- Configuration S3 (optionnelle) via django-storages (activez `USE_S3=True` et remplissez les variables AWS dans .env).

### Commandes utiles
- Lancer tout (incluant redis) :
  ```
  docker-compose build
  docker-compose up
  ```
- Dans un autre terminal, migrer et créer admin si besoin :
  ```
  docker-compose run web python manage.py migrate
  docker-compose run web python manage.py createsuperuser
  ```
- Démarrer worker (le service `worker` est défini dans docker-compose, il se lance automatiquement avec `docker-compose up`).



## Production checklist (what's included & what you must do)
- Fill .env with SECRET_KEY, DB credentials, TWILIO credentials, AWS keys if using S3.
- Set DEBUG=False in production.
- Configure DJANGO_ALLOWED_HOSTS properly.
- Configure S3 bucket and set USE_S3=True for secure file storage (enable server-side encryption on bucket).
- Configure TLS termination (use nginx + certbot) and never expose admin over HTTP.
- Configure backups for Postgres and S3.
- Configure monitoring (Sentry) and logs (Filebeat / Cloudwatch).
- Review GDPR compliance:
  - Store consent timestamps (field `consent_timestamp`).
  - Implement export and delete endpoints for user data (right to be forgotten).
  - Keep logs of data access (not included).
- Configure rate-limiting and WAF if high traffic.

## How to run (development)
See previous instructions. For React frontend:
```
cd frontend
npm install
npm run build
# serve build files with nginx or static host
```


## Frontend SPA (React) - Notes
- The frontend is in `/frontend`. It uses the environment variable `REACT_APP_API_BASE` to call the backend (default empty -> same host).
- Endpoints used:
  - `POST /api/token/` - login (staff)
  - `POST /api/candidates/` - create candidate (public)
  - `GET /api/admin/candidates/` - staff-only list of candidates
- To run locally:
  ```
  cd frontend
  npm install
  npm start
  ```
- To build:
  ```
  npm run build
  # Copy the build to Django static folder or serve via nginx.
  ```


## Added features (full options implemented)
- GDPR endpoints:
  - `GET /api/gdpr/export/<token>/?format=json|csv` — export your data.
  - `POST /api/gdpr/delete/<token>/` — request deletion (soft delete).
- Audit logs recorded in `candidates.AuditLog`.
- Postman collection available at `docs/postman_collection.json` (includes JWT flows).
- Frontend SPA updated: login via access token, dashboard, upload progress, client-side validation.
- Files are encrypted on the server before saving using Fernet (set `FILE_ENCRYPTION_KEY` in .env).
- WhatsApp Cloud API integration with templates (FR/DE). Set `WHATSAPP_CLOUD_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID` in .env.

## Postman
Import `docs/postman_collection.json` into Postman and set `base_url` variable to `http://localhost:8000`.

