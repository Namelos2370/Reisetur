from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework import status

class CandidateSelfView(APIView):
    """Allow candidate to retrieve their own record via access_token"""
    permission_classes = []

    def get(self, request, token):
        try:
            c = Candidate.objects.get(access_token=token, deleted_at__isnull=True)
        except Candidate.DoesNotExist:
            return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CandidateSerializer(c)
        return Response(serializer.data)
