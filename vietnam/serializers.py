from adrf import serializers
from rest_framework import serializers as rest_serializers
from vietnam.models import (
    AdministrativeRegion, AdministrativeUnit, Province, District, Ward, UserAddress
)


class AdministrativeRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeRegion
        fields = "__all__"


class AdministrativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeUnit
        fields = "__all__"


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    ward = rest_serializers.CharField(source="ward_id", required=True)
    class Meta:
        model = UserAddress
        exclude = ["username"]

    async def acreate(self, validated_data):
        validated_data["username"] = self.context["request"].user.username
        ward = validated_data.get("ward_id")
        print(validated_data)
        ward = await Ward.objects.filter(code=ward).select_related("district", "district__province").afirst()
        if not ward:
            raise rest_serializers.ValidationError("Ward not found")
        validated_data["district"] = ward.district
        validated_data["province"] = ward.district.province
        return await super().acreate(validated_data)


class UserAddressDetailSerializer(serializers.ModelSerializer):
    province = rest_serializers.SerializerMethodField(method_name="get_province")
    district = DistrictSerializer()
    ward = WardSerializer()
    class Meta:
        model = UserAddress
        fields = "__all__"

    def get_province(self, obj):
        return ProvinceSerializer(obj.province).data
