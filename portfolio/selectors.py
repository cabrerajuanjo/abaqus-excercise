import pandas
from portfolio.models import Amount


def getWeights(*, filters=None):
    amounts = Amount.objects.select_related(
        'date', 'portfolio', 'asset'
    ).filter(
        date__date__range=(
            filters['date__gt'],
            filters['date__lt']
        )
    )

    if (not len(amounts)):
        return

    amounts_dataframe = pandas.DataFrame(
        amounts.values(
            'date__date', 'portfolio__name', 'amount', 'asset__name'
        )
    ).rename(columns={
        'date__date': 'date',
        'portfolio__name':  'portfolio',
        'asset__name':  'asset',
    })

    total_portfolio_value_t = amounts_dataframe.drop(
        columns='asset'
    ).groupby(
        ['portfolio', 'date'], as_index=False
    ).sum().rename(columns={'amount': 'total_amount'})

    weights = total_portfolio_value_t.merge(
        amounts_dataframe, on=['date', 'portfolio']
    )

    weights['weight'] = weights.amount / weights.total_amount

    return weights.to_dict('records')


def getTotals(*, filters=None):
    amounts = Amount.objects.select_related(
        'date', 'portfolio', 'asset'
    ).filter(
        date__date__range=(
            filters['date__gt'],
            filters['date__lt']
        )
    )

    if (not len(amounts)):
        return

    amounts_dataframe = pandas.DataFrame(amounts.values(
        'date__date', 'portfolio__name', 'amount', 'asset__name')
    ).rename(columns={
        'date__date': 'date',
        'portfolio__name':  'portfolio',
        'asset__name':  'asset',
    })

    total_portfolio_value_t = amounts_dataframe.drop(
        columns='asset'
    ).groupby(
        ['portfolio', 'date'], as_index=False
    ).sum().rename(columns={'amount': 'total_amount'})

    return total_portfolio_value_t.to_dict('records')
