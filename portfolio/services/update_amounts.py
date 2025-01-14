import pandas
from django.db import transaction
from django.core import exceptions
from django.db.models import Prefetch
from portfolio.models.models import (
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
    )

    prices = Price.objects.select_related(
        'date', 'asset'
    ).filter(
        date__date__gte=date,
        asset__name=asset
    )

    if not len(amounts) or not len(prices):
        raise exceptions.ValidationError("No data matches parameters provided")

    new_amount_for_date = amounts[0].amount + amount_delta
    new_quantity_from_date = new_amount_for_date / prices[0].price

    # Merge prices and amouts

    prices_dataframe = pandas.DataFrame(
        prices.values(
        )
    )

    print('new_amount_for_date', new_amount_for_date)
    print('new_cuantity_from_date', new_quantity_from_date)

    print('amounts')
    print(amounts.values())
    print('prices_dataframe')
    print(prices_dataframe)

    for amount in amounts:
        print('amount', amount.amount)
        # Calculate the new amount
        new_amount = prices_dataframe[
            prices_dataframe['date_id'] == amount.date_id
        ].iloc[0]['price'] * new_quantity_from_date



        print('new_amount', new_amount)
        amount.amount = new_amount
        amount.save()
