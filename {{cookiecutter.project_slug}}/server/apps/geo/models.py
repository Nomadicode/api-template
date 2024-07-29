from django.db import models
from django.contrib.gis.db import models as geomodels


# Create your models here.
class Continent(models.Model):
    name = models.CharField(max_length=24)
    iso_code = models.CharField(max_length=2)

    geo = geomodels.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    iso_code_2 = models.CharField(max_length=2)
    iso_code_3 = models.CharField(max_length=3)
    numeric_code = models.IntegerField()
    phone_code = models.CharField(max_length=15, null=True, blank=True)
    capital = models.ForeignKey("City", related_name="capital", on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey("Currency", related_name="country", on_delete=models.SET_NULL, null=True, blank=True)
    languages = models.ManyToManyField(to="Language", related_name="languages", blank=True)

    geo = geomodels.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"


class Visa(models.Model):
    class VisaType(models.Choices):
        pass

    destination = models.ForeignKey(Country, on_delete=models.CASCADE)
    origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    visa_type = models.IntegerField(choices=)


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    iso_code = models.CharField(max_length=5)    

    geo = geomodels.MultiPolygonField(null=True, blank=True)

    @property
    def slug(self):
        return f"{self.name},{self.country.name}"

    def __str__(self):
        return f"{self.name},{self.country.name}"


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=9)

    geo = geomodels.MultiPolygonField(null=True, blank=True)

    @property
    def slug(self):
        return f"{self.name},{self.region.name},{self.country.name}"
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "cities"


class Currency(models.Model):
    name = models.CharField(max_length=64)
    iso_code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    decimal_digits = models.IntegerField(default=2)
    decimal_separator = models.CharField(max_length=1, default=".")
    thousands_separator = models.CharField(max_length=1, default=",")
    symbol_left = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "currencies"


class Language(models.Model):
    name = models.CharField(max_length=128)
    native_name = models.CharField(max_length=256)
    alpha_2_code = models.CharField(max_length=4)