from django.test import TestCase
from django.urls import reverse
from .models import PricingConfiguration, DistanceBasePrice, TimeMultiplierFactor, WaitingCharges


class CalculateTotalPriceTestCase(TestCase):
    def setUp(self):
        self.config = PricingConfiguration.objects.create(
            config_name='Test Config', is_enabled=True
        )
        self.distance_base_price = DistanceBasePrice.objects.create(
            config=self.config, day_of_week='Fri', base_distance_km=12, base_price=60, additional_distance_price_per_km=3
        )
        self.time_multiplier_factor = TimeMultiplierFactor.objects.create(
            config=self.config, after_duration_mins=30, till_duration_mins=60, multiplier_factor=2
        )
        self.waiting_charges = WaitingCharges.objects.create(
            config=self.config, initial_wait_min=8, price_per_min=1.5
        )

    def test_calculate_total_price(self):
        url = reverse('pricing_config:calculate_total_price')
        data = {
            'total_distance': 25,
            'trip_time': 65,
            'waiting_time': 20,
            'trip_date': '2023-10-04',
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_price', response.json())
        self.assertEqual(response.json()['total_price'], 165)

    def test_invalid_date_format(self):
        url = reverse('pricing_config:calculate_total_price')
        data = {
            'total_distance': 25,
            'trip_time': 65,
            'waiting_time': 20,
            'trip_date': '2023/10/04',   # Invalid date format
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid parameter values.')

    def test_invalid_request_method(self):
        url = reverse('pricing_config:calculate_total_price')
        response = self.client.post(url)  # Use POST method for invalid request
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'],
                         'Invalid request method. Use GET method.')
