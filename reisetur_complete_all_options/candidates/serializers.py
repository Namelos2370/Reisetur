from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(read_only=True)
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ('created_at','access_token',)
