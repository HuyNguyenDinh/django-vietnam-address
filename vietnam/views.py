from asgiref.sync import sync_to_async
from adrf import viewsets, generics
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from vietnam.models import *
from vietnam.serializers import *
from vietnam.repository import Repository


class CacheListView(generics.ListAPIView):
    async def alist(self, request, *args, **kwargs):
        cache_key = f"alist:cache:{request.get_full_path()}"
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "code": ["exact"],
        "name": ["exact"],
        "administrative_unit__id": ["exact"],
        "administrative_region__id": ["exact"],
    }

class DistrictList(viewsets.ViewSet, CacheListView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "code": ["exact"],
        "name": ["exact"],
        "administrative_unit_id": ["exact"],
        "province__code": ["exact"],
    }

class WardList(viewsets.ViewSet, CacheListView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "code": ["exact"],
        "name": ["exact"],
        "administrative_unit_id": ["exact"],
        "district__code": ["exact"],
    }


class UserAddressViewset(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ["retrieve", "aretrieve"]:
            qs = qs.select_related("province", "district", "ward")
        return qs.filter(username=self.request.user.username)
    
    def get_serializer_class(self):
        if self.action in ["retrieve", "aretrieve"]:
            return UserAddressDetailSerializer
        return super().get_serializer_class()
