from django.db import models

class AdministrativeRegion(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    code_name_en = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'administrative_regions'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['name_en']),
        ]

    def __str__(self):
        return self.name


class AdministrativeUnit(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    full_name_en = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    short_name_en = models.CharField(max_length=255, null=True, blank=True)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    code_name_en = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'administrative_units'

    def __str__(self):
        return self.full_name or 'Administrative Unit'


class Province(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    full_name_en = models.CharField(max_length=255, null=True, blank=True)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, blank=True)
    administrative_region = models.ForeignKey(AdministrativeRegion, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'provinces'
        indexes = [
            models.Index(fields=['administrative_region']),
            models.Index(fields=['administrative_unit']),
        ]

    def __str__(self):
        return self.name


class District(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    full_name_en = models.CharField(max_length=255, null=True, blank=True)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    province = models.ForeignKey(Province, db_column='province_code', on_delete=models.SET_NULL, null=True, blank=True)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'districts'
        indexes = [
            models.Index(fields=['province']),
            models.Index(fields=['administrative_unit']),
        ]

    def __str__(self):
        return self.name


class Ward(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    full_name_en = models.CharField(max_length=255, null=True, blank=True)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    district = models.ForeignKey(District, db_column='district_code', on_delete=models.SET_NULL, null=True, blank=True)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'wards'
        indexes = [
            models.Index(fields=['district']),
            models.Index(fields=['administrative_unit']),
        ]

    def __str__(self):
        return self.name


class UserAddress(models.Model):
    username = models.CharField(max_length=40)
    province = models.ForeignKey(Province, db_column='province_code', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, db_column='district_code', on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, db_column='ward_code', on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=40, null=True, blank=True)
