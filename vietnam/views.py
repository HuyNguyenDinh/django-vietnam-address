from adrf import viewsets, generics
from vietnam.models import *
from vietnam.serializers import *

class AdministrativeRegionList(viewsets.ModelViewSet):
    queryset = AdministrativeRegion.objects.all()
    serializer_class = AdministrativeRegionSerializer


class AdministrativeUnitList(viewsets.ModelViewSet):
    queryset = AdministrativeUnit.objects.all()
    serializer_class = AdministrativeUnitSerializer

class ProvinceList(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictList(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class WardList(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer