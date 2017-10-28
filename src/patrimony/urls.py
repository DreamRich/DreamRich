from rest_framework import routers
from patrimony.views import (
    PatrimonyViewSet,
    ActiveViewSet,
    ActiveManagerViewSet,
    ArrearageViewSet,
    RealEstateViewSet,
    CompanyParticipationViewSet,
    EquipmentViewSet,
    LifeInsuranceViewSet,
    IncomeViewSet,
    ActiveTypeViewSet,
)


app_name = 'patrimony'  # pylint: disable=invalid-name

router = routers.DefaultRouter()  # pylint: disable=invalid-name
router.register(r'^active', ActiveViewSet)
router.register(r'^active_type', ActiveTypeViewSet)
router.register(r'^active_manager', ActiveManagerViewSet)
router.register(r'^arrearage', ArrearageViewSet)
router.register(r'^realestate', RealEstateViewSet)
router.register(r'^companyparticipation', CompanyParticipationViewSet)
router.register(r'^equipment', EquipmentViewSet)
router.register(r'^lifeinsurance', LifeInsuranceViewSet)
router.register(r'^income', IncomeViewSet)
router.register(r'', PatrimonyViewSet)

urlpatterns = router.urls
