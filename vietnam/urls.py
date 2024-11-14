from adrf.routers import DefaultRouter
from vietnam.views import *

router = DefaultRouter()

router.register('administrative_region', AdministrativeRegionList, basename='administrative_region')
router.register('administrative_unit', AdministrativeUnitList, basename='administrative_unit')
router.register('province', ProvinceList, basename='province')
router.register('district', DistrictList, basename='district')
router.register('ward', WardList, basename='ward')
urlpatterns = router.urls