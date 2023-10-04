from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError


class DistanceBasePriceInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super(DistanceBasePriceInlineFormSet, self).clean()

        days_of_week = set()

        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                day_of_week = form.cleaned_data.get('day_of_week')

                if day_of_week:
                    if day_of_week in days_of_week:
                        raise ValidationError(
                            "Day Repeat : Each day of the week should be present exactly once.")
                    else:
                        days_of_week.add(day_of_week)
                else:
                    raise ValidationError(
                        "For each entry, you have to select a day of the week.")

        if len(days_of_week) < 7:
            raise ValidationError("Each day of week should be present. Add for remaining days of the week")
