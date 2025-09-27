from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, AuditLog
from django.http import HttpResponse
import csv
import json
from django.utils import timezone

class GDPRExportView(APIView):
    permission_classes = []
    def get(self, request, token, format=None):
        # export candidate data as JSON or CSV based on query param ?format=csv
        try:
            c = Candidate.objects.get(access_token=token)
        except Candidate.DoesNotExist:
            return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'whatsapp': c.whatsapp,
            'objective': c.objective,
            'diploma': c.diploma,
            'status': c.status,
            'created_at': c.created_at.isoformat(),
            'appointment_date': c.appointment_date.isoformat() if c.appointment_date else None,
        }
        # log audit
        AuditLog.objects.create(candidate=c, action='export', performed_by='self', details='Exported via GDPR endpoint')
        fmt = request.query_params.get('format','json')
        if fmt == 'csv':
            # build CSV response
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = f'attachment; filename="candidate_{c.id}.csv"'
            writer = csv.writer(resp)
            writer.writerow(['field','value'])
            for k,v in data.items():
                writer.writerow([k, v])
            return resp
        else:
            return Response(data)

class GDPRDeleteView(APIView):
    permission_classes = []
    def post(self, request, token):
        # mark as deleted_at and remove personal files (best-effort)
        try:
            c = Candidate.objects.get(access_token=token)
        except Candidate.DoesNotExist:
            return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        # soft delete
        c.deleted_at = timezone.now()
        c.access_token = None
        c.save()
        # log
        AuditLog.objects.create(candidate=c, action='delete', performed_by='self', details='Deleted via GDPR endpoint')
        return Response({'status':'deleted'})
