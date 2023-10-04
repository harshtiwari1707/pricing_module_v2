
from django.contrib import admin
from .models import PricingConfiguration, DistanceBasePrice, TimeMultiplierFactor, WaitingCharges
from .forms import DistanceBasePriceInlineFormSet


class DistanceBasePriceInline(admin.TabularInline):
    model = DistanceBasePrice
    formset = DistanceBasePriceInlineFormSet
    extra = 7


class TimeMultiplierFactorInline(admin.TabularInline):
    model = TimeMultiplierFactor
    extra = 1


class WaitingChargesInline(admin.TabularInline):
    model = WaitingCharges
    extra = 1


@admin.register(PricingConfiguration)
class PricingConfigurationAdmin(admin.ModelAdmin):
    list_display = ('config_id', 'config_name', 'is_enabled')
    inlines = [DistanceBasePriceInline,
               TimeMultiplierFactorInline, WaitingChargesInline]
