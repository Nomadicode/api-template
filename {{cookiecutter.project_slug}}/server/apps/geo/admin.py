from django.contrib import admin

from apps.geo.models import City, Continent, Country, Currency, Region


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_region_name', 'get_country_code', )

    @admin.display(description='Region Name', ordering='region__name')
    def get_region_name(self, obj):
        return obj.region.name

    @admin.display(description='Country Code', ordering='country__iso_code_3')
    def get_country_code(self, obj):
        return obj.country.iso_code_3

admin.site.register(City, CityAdmin)


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', )

admin.site.register(Continent, ContinentAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code_2', 'iso_code_3', )

admin.site.register(Country, CountryAdmin)



class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'symbol', )

admin.site.register(Currency, CurrencyAdmin)



class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'get_country_code', )

    @admin.display(description='Country Code', ordering='country__iso_code_3')
    def get_country_code(self, obj):
        return obj.country.iso_code_3

admin.site.register(Region, RegionAdmin)
