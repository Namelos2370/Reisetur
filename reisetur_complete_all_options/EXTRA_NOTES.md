Extending this project:
- Add authentication to the API (Token or JWT) for admin endpoints.
- Implement notifications: use an async worker (Celery + Redis) to send emails and WhatsApp messages.
- GDPR: store consent timestamp, allow export/delete requests.
- Secure file storage: for production, use S3 or other encrypted storage.
- Use nginx + gunicorn behind TLS for production; configure allowed hosts and DEBUG=False.
