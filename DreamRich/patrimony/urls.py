from rest_framework import routers
from patrimony.views import (
    PatrimonyViewSet,
    ActiveViewSet,
    ArrearageViewSet,
    RealEstateViewSet,
    CompanyParticipationViewSet,
    EquipmentViewSet,
    LifeInsuranceViewSet,
    IncomeViewSet,
)


app_name = 'patrimony'

router = routers.DefaultRouter()
router.register('active', ActiveViewSet)
router.register('arrearage', ArrearageViewSet)
router.register('realestate', RealEstateViewSet)
router.register('companyparticipation', CompanyParticipationViewSet)
router.register('equipment', EquipmentViewSet)
router.register('lifeinsurance', LifeInsuranceViewSet)
router.register('income', IncomeViewSet)
router.register('', PatrimonyViewSet)

urlpatterns = router.urls
