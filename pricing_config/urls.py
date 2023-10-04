from django.urls import path
from .views import calculate_total_price

app_name = 'pricing_config'

urlpatterns = [
    path('calculate_total_price/', calculate_total_price, name='calculate_total_price'),
]
