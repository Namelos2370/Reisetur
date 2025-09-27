from celery import shared_task
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail

@shared_task
def send_whatsapp_message(to_number, message):
    """Send a WhatsApp message using Twilio (WhatsApp sandbox / WhatsApp Cloud)."""
    sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    from_number = getattr(settings, 'TWILIO_FROM_NUMBER', None)
    if not sid or not token or not from_number:
        # Twilio not configured
        return {'status': 'twilio_not_configured'}
    client = Client(sid, token)
    try:
        msg = client.messages.create(body=message, from_=from_number, to=to_number)
        return {'status': 'sent', 'sid': msg.sid}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

@shared_task
def send_email_notification(subject, body, recipient_list):
    send_mail(subject, body, None, recipient_list, fail_silently=False)
    return {'status': 'sent_email'}


@shared_task
def send_upcoming_reminders():
    """Find candidates with appointments in 24h or 2h and send reminders."""
    from django.utils import timezone
    from datetime import timedelta
    now = timezone.now()
    in_24 = now + timedelta(hours=24)
    in_2 = now + timedelta(hours=2)
    # candidates in next 24h (approx)
    qs_24 = Candidate.objects.filter(appointment_date__gte=now, appointment_date__lte=in_24)
    qs_2 = Candidate.objects.filter(appointment_date__gte=now, appointment_date__lte=in_2)
    sent = []
    for c in qs_24:
        try:
            if c.whatsapp:
                send_whatsapp_message.delay(c.whatsapp, f"Rappel: vous avez un rendez-vous prévu le {c.appointment_date:%Y-%m-%d %H:%M}. - Reisetür")
            send_email_notification.delay('Rappel rendez-vous', f'Bonjour {c.first_name}, ceci est un rappel pour votre rendez-vous le {c.appointment_date:%Y-%m-%d %H:%M}.', [c.email])
            sent.append(c.id)
        except Exception:
            pass
    for c in qs_2:
        try:
            if c.whatsapp:
                send_whatsapp_message.delay(c.whatsapp, f"Rappel urgent: votre rendez-vous est bientôt ({c.appointment_date:%Y-%m-%d %H:%M}). - Reisetür")
            send_email_notification.delay('Rappel urgent rendez-vous', f'Bonjour {c.first_name}, votre rendez-vous est imminent ({c.appointment_date:%Y-%m-%d %H:%M}).', [c.email])
            sent.append(c.id)
        except Exception:
            pass
    return {'sent': sent}


# WhatsApp Cloud API integration (Facebook / Meta)
import requests
from django.conf import settings

WHATSAPP_TEMPLATES = {
    'fr': {
        'application_received': 'Bonjour {first_name}, nous avons bien reçu votre candidature chez Reisetür.',
        'status_update': 'Bonjour {first_name}, le statut de votre dossier est maintenant: {status}.',
        'appointment_reminder': 'Rappel: votre rendez-vous est prévu le {date}.'
    },
    'de': {
        'application_received': 'Hallo {first_name}, Ihre Bewerbung bei Reisetür ist eingegangen.',
        'status_update': 'Hallo {first_name}, der Status Ihres Antrags ist jetzt: {status}.',
        'appointment_reminder': 'Erinnerung: Ihr Termin ist am {date}.'
    }
}

def send_whatsapp_cloud(phone_number, template_key, params=None):
    """Send a message via WhatsApp Cloud API using a simple text template (not registered template)."""
    token = getattr(settings, 'WHATSAPP_CLOUD_TOKEN', None)
    phone_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', None)
    if not token or not phone_id:
        return {'status':'not_configured'}
    headers = {'Authorization': f'Bearer {token}', 'Content-Type':'application/json'}
    # Build message text from templates (default to French)
    locale = params.get('locale','fr') if params else 'fr'
    template_text = WHATSAPP_TEMPLATES.get(locale, WHATSAPP_TEMPLATES['fr']).get(template_key, '')
    if params:
        template_text = template_text.format(**params)
    data = {
        'messaging_product': 'whatsapp',
        'to': phone_number.replace('whatsapp:',''),
        'type': 'text',
        'text': {'body': template_text}
    }
    url = f'https://graph.facebook.com/v16.0/{phone_id}/messages'
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        return {'status': r.status_code, 'response': r.text}
    except Exception as e:
        return {'status':'error', 'error': str(e)}
