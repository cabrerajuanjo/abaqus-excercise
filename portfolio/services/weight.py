# from django.db import transaction
# import pandas
from django.db import models
from itertools import chain
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from portfolio.models.models import Weight, Price, Quantity, Portfolio, Date
from portfolio.filters import WeightFilter

from django.db.models import Prefetch

# Prefetch related data for optimization


def get(*, filters=None) -> QuerySet[Weight]:

    weight = Weight.objects.prefetch_related(
        Prefetch('portfolio'),
        Prefetch('asset')
    )

    # pit * cit # by date, by portfolio, by asset
    # sum(pit * cit) # by date, by portfolio

    dates = Date.objects.all()

    for date in dates:
        quantity_set = date.quantity_set.annotate(
            price=models.Value(None, output_field=models.CharField())
        ).values()
        price_set = date.price_set.annotate(
            quantity=models.Value(None, output_field=models.CharField()),
            portfolio_id=models.Value(None, output_field=models.CharField())
        ).values()

        quantity_dict_by_asset = {item['asset_id']: item for item in quantity_set}
        price_dict_by_asset = {item['asset_id']: item for item in price_set}

        quantity_price_union = []
        for key in quantity_dict_by_asset.keys() | price_dict_by_asset.keys():
            price = price_dict_by_asset.get(key, {}).get('price')
            quantity = quantity_dict_by_asset.get(key, {}).get('quantity')
            entry = {
                'date': date.date,
                'asset': key,
                'price': price,
                'quantity': quantity,
                'values': price*quantity,
            }
            print('entry', entry)
            quantity_price_union.append(entry)

        # for quantity_price in quantity_price_set:
            # print('quantity_price', quantity_price)
            # print('quantity-price:', quantity_price.date, quantity_price.quantity, quantity_price.price)
        # for quantity in quantity_set:
        #     print('date, quantity', date.date, quantity.quantity)
        # for price in price_set:
        #     print('date, price', date.date, price.price)

    # for quantity in quantities:
    #     price_set =\
    #         quantity.asset.price_set.filter(  # type: ignore[attr-defined]
    #             date__range=(
    #                 filters['date__gt'],
    #                 filters['date__lt']
    #             )
    #         )
    #     for price in price_set:
    #         print(
    #             f"Portfolio: {quantity.portfolio.name},\
    #             Asset: {quantity.asset.name},\
    #             Date: {price.date},\
    #             Quantity: {quantity.quantity},\
    #             Price: {price.price}"
    #         )

    return WeightFilter(filters, weight).qs
