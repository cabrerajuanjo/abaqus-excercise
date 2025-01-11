# from django.db import transaction
import pandas
from django.db import models
from itertools import chain
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from portfolio.models.models import Amount, Weight
from portfolio.filters import WeightFilter

from django.db.models import Prefetch

# Prefetch related data for optimization


def get(*, filters=None) -> QuerySet[Amount]:
    amounts = Amount.objects.select_related('date', 'portfolio', 'asset').filter(
        date__date__range=(
            filters['date__gt'],
            filters['date__lt']
        )
    )

    amounts_dataframe = pandas.DataFrame(amounts.values(
        'date__date', 'portfolio__name', 'amount'))
    print(amounts_dataframe)

    total_portfolio_value_t = amounts_dataframe.groupby(
        ['portfolio__name', 'date__date']
    ).sum()

    print(total_portfolio_value_t.to_string())

    return amounts
