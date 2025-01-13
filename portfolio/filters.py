import django_filters
from portfolio.models.models import Weight


class WeightFilter(django_filters.FilterSet):
    class Meta:
        model = Weight
        fields = {
            'date': ['lt', 'gt']
        }
