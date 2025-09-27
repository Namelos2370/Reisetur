from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','objective','status','created_at')
    list_filter = ('status','created_at')
    search_fields = ('first_name','last_name','email','whatsapp')
