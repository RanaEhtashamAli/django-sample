from .views import PatientViewSet, PatientVisitViewSet, PatientPrescriptionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'visits', PatientVisitViewSet, basename='visit')
router.register(r'prescriptions', PatientPrescriptionViewSet, basename='prescription')
urlpatterns = router.urls

