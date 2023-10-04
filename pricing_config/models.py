from django.db import models
from django.core.exceptions import ValidationError


class PricingConfiguration(models.Model):
    config_id = models.AutoField(primary_key=True)
    config_name = models.CharField(
        max_length=100, unique=True, help_text="Enter a unique name for this config.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(
        default=False, help_text="Only one configuration can be enabled at a time, If this is enabled others will be disabled.")

    def save(self, *args, **kwargs):
        # Disable other enabled configurations when saving this one as enabled
        if self.is_enabled:
            self.disable_other_configs()
        super().save(*args, **kwargs)

    def disable_other_configs(self):
        if self.pk:
            PricingConfiguration.objects.exclude(
                pk=self.pk).update(is_enabled=False)
        else:
            PricingConfiguration.objects.all().update(is_enabled=False)


class DistanceBasePrice(models.Model):
    dbp_id = models.AutoField(primary_key=True)
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ])
    base_distance_km = models.FloatField()
    base_price = models.FloatField()
    additional_distance_price_per_km = models.FloatField()

    def clean(self):
        if self.base_distance_km <= 0:
            raise ValidationError("Invalid Base distance : Base distance should be greater than 0.")
        if self.base_price <= 0:
            raise ValidationError("Invalid Base distance : Base price should be greater than 0.")
        if self.additional_distance_price_per_km <= 0:
            raise ValidationError(
                "Additional distance price should be greater than 0.")


class TimeMultiplierFactor(models.Model):
    tmf_id = models.AutoField(primary_key=True)
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    after_duration_mins = models.FloatField()
    till_duration_mins = models.FloatField(null=True, blank=True)
    multiplier_factor = models.FloatField()

    def clean(self):
        if self.after_duration_mins < 0:
            raise ValidationError("Invalid After duration : After duration should be non-negative.")
        if self.till_duration_mins and self.till_duration_mins < self.after_duration_mins:
            raise ValidationError(
                "Invalid Till duration : Till duration should be greater than or equal to after duration.")
        if self.multiplier_factor <= 0:
            raise ValidationError(
                "Invalid Multiplier factor : Multiplier factor should be greater than 0.")


class WaitingCharges(models.Model):
    wc_id = models.AutoField(primary_key=True)
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    initial_wait_min = models.IntegerField()
    price_per_min = models.FloatField()

    def clean(self):
        if self.initial_wait_min < 0:
            raise ValidationError("Invalid Initial wait time : Initial wait time should be non-negative.")
        if self.price_per_min < 0:
            raise ValidationError("Invalid Price per min : Price per min should be greater than 0.")
