import pandas
from django.db import transaction
from django.core import exceptions
from django.db.models import Prefetch
from portfolio.models import (
    Amount, Price
)

# TODO: put this constant in a common place
SELL_CHOICE = "SELL"


@transaction.atomic
def execute(date, portfolio, asset, operation, amount_delta) -> None:
    if amount_delta == 0:
        return

    if operation == SELL_CHOICE:
        amount_delta *= -1

    amounts = Amount.objects.select_related(
        'date', 'portfolio', 'asset'
    ).filter(
        date__date__gte=date,
        portfolio__name=portfolio,
        asset__name=asset
    ).order_by("date__date")

    prices = Price.objects.select_related(
        'date', 'asset'
    ).filter(
        date__date__gte=date,
        asset__name=asset
    ).order_by("date__date")

    if not len(amounts) or not len(prices):
        return

    new_amount_for_date = amounts[0].amount + amount_delta
    # TODO: error if new_amount_for_date < 0 because theres no sufficient amount to sell
    if new_amount_for_date < 0:
        new_amount_for_date = 0

    new_quantity_from_date = new_amount_for_date / prices[0].price
    prices_dataframe = pandas.DataFrame(
        prices.values()
    )

    for amount in amounts:
        new_amount = prices_dataframe[
            prices_dataframe['date_id'] == amount.date_id
        ].iloc[0]['price'] * new_quantity_from_date
        amount.amount = new_amount
        amount.save()
