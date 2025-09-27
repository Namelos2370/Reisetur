from django.shortcuts import render, redirect
from .models import Candidate
from .serializers import CandidateSerializer
from .permissions import IsAdminOrCreateOnly
import uuid

from .tasks import send_whatsapp_message, send_email_notification
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def candidate_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        objective = request.POST.get('objective')
        diploma = request.POST.get('diploma')

        c = Candidate.objects.create(
            first_name=first_name, last_name=last_name, email=email,
            whatsapp=whatsapp, objective=objective, diploma=diploma
        )
        # handle files
        if request.FILES.get('id_card'):
            c.id_card = request.FILES['id_card']
        if request.FILES.get('passport'):
            c.passport = request.FILES['passport']
        if request.FILES.get('diploma_file'):
            c.diploma_file = request.FILES['diploma_file']
        if request.FILES.get('cv'):
            c.cv = request.FILES['cv']
        c.save()
        # Dispatch async notifications (WhatsApp + email) if configured
        try:
            if c.whatsapp:
                send_whatsapp_message.delay(c.whatsapp, f"Bonjour {c.first_name}, votre candidature a bien été reçue par Reisetür.")
            send_email_notification.delay('Candidature reçue', f'Bonjour {c.first_name}, nous avons bien reçu votre candidature.', [c.email])
        except Exception:
            pass
        # generate access token for self-service if not exists
        if not c.access_token:
            c.access_token = uuid.uuid4().hex
            c.save()
        return render(request, 'thanks.html', {'candidate': c, 'access_token': c.access_token})
    return render(request, 'candidate_form.html')

# DRF viewset
from rest_framework import permissions
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all().order_by('-created_at')
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminOrCreateOnly]


def perform_create(self, serializer):
    instance = serializer.save()
    if not instance.access_token:
        import uuid
        instance.access_token = uuid.uuid4().hex
        instance.save()

# Admin API viewset for staff
class AdminCandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all().order_by('-created_at')
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        old = self.get_object()
        instance = serializer.save()
        # if status changed, you might trigger signals/tasks
        if old.status != instance.status:
            try:
                from .tasks import send_whatsapp_message, send_email_notification
                if instance.whatsapp:
                    send_whatsapp_message.delay(instance.whatsapp, f"Bonjour {instance.first_name}, le statut de votre dossier a changé: {instance.status}")
                send_email_notification.delay('Mise à jour dossier Reisetür', f'Bonjour {instance.first_name}, le statut de votre dossier est maintenant: {instance.status}', [instance.email])
            except Exception:
                pass

