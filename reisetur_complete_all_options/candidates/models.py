from django.db import models

STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('validated', 'Validated'),
    ('rejected', 'Rejected'),
]

class Candidate(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=50, blank=True)
    objective = models.CharField(max_length=200, blank=True)
    diploma = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Consent & appointment
    consent = models.BooleanField(default=False)
    consent_timestamp = models.DateTimeField(null=True, blank=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Token for candidate self-access (UUID or random string)
    access_token = models.CharField(max_length=64, blank=True, null=True, unique=True)

    id_card = models.FileField(upload_to='documents/id_cards/', null=True, blank=True)
    passport = models.FileField(upload_to='documents/passports/', null=True, blank=True)
    diploma_file = models.FileField(upload_to='documents/diplomas/', null=True, blank=True)
    cv = models.FileField(upload_to='documents/cvs/', null=True, blank=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('export', 'Export'),
        ('delete', 'Delete'),
        ('status_change', 'Status change'),
        ('create', 'Create'),
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='audit_logs', null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    performed_by = models.CharField(max_length=200, blank=True, null=True)  # could be user or system
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.candidate} - {self.timestamp}"
