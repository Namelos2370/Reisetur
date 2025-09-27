IMPORTANT:
- This codebase was modified with new models/fields (access_token, AuditLog, consent fields).
- You must run Django migrations after pulling this code:
    docker-compose run web python manage.py makemigrations
    docker-compose run web python manage.py migrate
- If you already have production data, review migrations before applying.
