from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import Candidate
import io

User = get_user_model()

class CandidateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        self.create_url = reverse('candidate-list')

    def test_create_candidate_anonymous(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'whatsapp': 'whatsapp:+237600000000',
            'objective': 'etudes'
        }
        resp = self.client.post(self.create_url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Candidate.objects.filter(email='test@example.com').exists())

    def test_admin_can_list(self):
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get(self.create_url)
        self.assertEqual(resp.status_code, 200)
