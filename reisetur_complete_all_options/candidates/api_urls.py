from django.urls import path, include
from rest_framework import routers
from .views import CandidateViewSet, AdminCandidateViewSet
from .api_views import CandidateSelfView
from .gdpr_views import GDPRExportView, GDPRDeleteView

router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'admin/candidates', AdminCandidateViewSet, basename='admin-candidate')

urlpatterns = [
    path('', include(router.urls)),
    path('self/<str:token>/', CandidateSelfView.as_view(), name='candidate-self'),
    path('gdpr/export/<str:token>/', GDPRExportView.as_view(), name='gdpr-export'),
    path('gdpr/delete/<str:token>/', GDPRDeleteView.as_view(), name='gdpr-delete'),
]
