from financial_planning.views import (
    RegularCostViewSet,
)


app_name = 'financial_planning'

router.register('regularcost', RegularCostViewSet)
