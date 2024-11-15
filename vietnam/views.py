from asgiref.sync import sync_to_async
from adrf import viewsets, generics
from django.core.cache import cache
from rest_framework.response import Response

from vietnam.models import *
from vietnam.serializers import *


class CacheListView(generics.ListAPIView):
    async def alist(self, request, *args, **kwargs):
        cache_key = f"alist:cache:{request.path}"
        cached_data = await sync_to_async(cache.get)(cache_key)
        if cached_data:
            return Response(cached_data)
        response = await super().alist(request, *args, **kwargs)
        await sync_to_async(cache.set)(cache_key, response.data, 60 * 15)
        return response

class AdministrativeRegionList(viewsets.ViewSet, CacheListView):
    queryset = AdministrativeRegion.objects.all()
    serializer_class = AdministrativeRegionSerializer

class AdministrativeUnitList(viewsets.ViewSet, CacheListView):
    queryset = AdministrativeUnit.objects.all()
    serializer_class = AdministrativeUnitSerializer

class ProvinceList(viewsets.ViewSet, CacheListView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictList(viewsets.ViewSet, CacheListView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class WardList(viewsets.ViewSet, CacheListView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class UserAddressViewset(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user.username)
