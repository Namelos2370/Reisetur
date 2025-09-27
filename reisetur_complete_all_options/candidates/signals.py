from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Candidate
from .tasks import send_whatsapp_message, send_email_notification

@receiver(pre_save, sender=Candidate)
def candidate_pre_save(sender, instance, **kwargs):
    try:
        if instance.id:
            old = Candidate.objects.get(id=instance.id)
            instance._old_status = old.status
        else:
            instance._old_status = None
    except Candidate.DoesNotExist:
        instance._old_status = None

@receiver(post_save, sender=Candidate)
def candidate_post_save(sender, instance, created, **kwargs):
    if created:
        # send welcome notifications async
        try:
            if instance.whatsapp:
                send_whatsapp_message.delay(instance.whatsapp, f"Bonjour {instance.first_name}, votre candidature a bien été reçue par Reisetür.")
            send_email_notification.delay('Candidature reçue', f'Bonjour {instance.first_name}, nous avons bien reçu votre candidature.', [instance.email])
        except Exception:
            pass
    else:
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            # status changed -> notify
            try:
                if instance.whatsapp:
                    send_whatsapp_message.delay(instance.whatsapp, f"Bonjour {instance.first_name}, le statut de votre dossier a été mis à jour: {instance.status}")
                send_email_notification.delay('Mise à jour dossier Reisetür', f'Bonjour {instance.first_name}, le statut de votre dossier est maintenant: {instance.status}', [instance.email])
            except Exception:
                pass
