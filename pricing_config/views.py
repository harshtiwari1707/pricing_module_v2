from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import PricingConfiguration, DistanceBasePrice, TimeMultiplierFactor, WaitingCharges


def calculate_total_price(request):
    if request.method == 'GET':
        total_distance_str = request.GET.get('total_distance', None)
        trip_time_str = request.GET.get('trip_time', None)
        waiting_time_str = request.GET.get('waiting_time', None)
        trip_date_str = request.GET.get('trip_date', None)

        # Check if any of the required parameters are missing
        if None in [total_distance_str, trip_time_str, waiting_time_str, trip_date_str]:
            return JsonResponse({'ERROR': 'Missing parameter values.'}, status=400)

        try:
            total_distance = float(total_distance_str)
            trip_time = float(trip_time_str)
            waiting_time = float(waiting_time_str)
            date_of_trip = datetime.strptime(trip_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'ERROR': 'Invalid parameter values.'}, status=400)

        try:
            config = PricingConfiguration.objects.get(is_enabled=True)
        except:
            return JsonResponse({"total_price": 0, "message": "No pricing configuration is active"}, status=200)

        day_of_week = date_of_trip.strftime('%a')
        distance_base_price = get_distance_base_price(
            config, total_distance, day_of_week)
        time_multiplier_factor = get_time_multiplier_factor(config, trip_time)
        waiting_charges = get_waiting_charges(config, waiting_time)

        total_price = distance_base_price + \
            (trip_time * time_multiplier_factor) + waiting_charges
        return JsonResponse({'total_price': total_price})
    else:
        return JsonResponse({'error': 'Invalid request method. Use GET method.'}, status=400)


def get_distance_base_price(config, total_distance, day_of_week):
    try:
        distance_base_price = DistanceBasePrice.objects.get(
            config=config,
            day_of_week=day_of_week
        )
        additional_distance_price = (total_distance - distance_base_price.base_distance_km) * \
            distance_base_price.additional_distance_price_per_km
        return distance_base_price.base_price + additional_distance_price
    except DistanceBasePrice.DoesNotExist:
        return 0 


def get_time_multiplier_factor(config, trip_time):
    try:
        time_multiplier_factor = TimeMultiplierFactor.objects.filter(
            config=config,
            after_duration_mins__lte=trip_time,
            till_duration_mins__gt=trip_time,
        ).order_by('till_duration_mins').first()

        if not time_multiplier_factor:
            time_multiplier_factor = TimeMultiplierFactor.objects.filter(
                config=config,
                after_duration_mins__lte=trip_time,
                till_duration_mins__isnull=True,
            ).first()

        if time_multiplier_factor:
            return time_multiplier_factor.multiplier_factor
        else:
            return 0  

    except TimeMultiplierFactor.DoesNotExist:
        return 0  


def get_waiting_charges(config, waiting_time):
    try:
        waiting_charges = WaitingCharges.objects.get(
            config=config
        )
        waiting_charges = (
            waiting_time - waiting_charges.initial_wait_min) * waiting_charges.price_per_min
        if waiting_charges < 0:
            return 0
        return waiting_charges
    except WaitingCharges.DoesNotExist:
        return 0  
