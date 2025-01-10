import os
from django.db import transaction
import pandas
from portfolio.models.models import Asset, Price, Portfolio, Weight, Quantity, Date

DATE_PRICE_COLUMN = 'Dates'
DATE_WEIGHT_COLUMN = 'Fecha'
ASSET_WEIGHT_COLUMN = 'activos'

WEIGHTS_SHEET_NAME = 'weights'
PRICES_SHEET_NAME = 'Precios'


def get_portfolios(portfolio_weights_sheet: pandas.DataFrame) -> set[str]:

    COLUMNS_TO_IGNORE_IN_WEIGHTS_SHEET = ('activos', 'Fecha')

    portfolios: set[str] = set([])
    for column in portfolio_weights_sheet.columns:
        if column not in COLUMNS_TO_IGNORE_IN_WEIGHTS_SHEET:
            portfolios.add(column)

    return portfolios


def get_assets(
    portfolio_weights_sheet: pandas.DataFrame,
    portfolio_prices_sheet: pandas.DataFrame,
) -> set[str]:
    COLUMNS_TO_IGNORE_IN_PRICES_SHEET = (DATE_PRICE_COLUMN)
    WEIGHTS_SHEET_ASSET_COLUMN_NAME = ASSET_WEIGHT_COLUMN
    assets: set[str] = set([])
    for column in portfolio_prices_sheet.columns:
        if column not in COLUMNS_TO_IGNORE_IN_PRICES_SHEET:
            assets.add(column)

    for asset in portfolio_weights_sheet[WEIGHTS_SHEET_ASSET_COLUMN_NAME]:
        assets.add(asset)

    return assets


def get_dates(
    portfolio_prices_sheet: pandas.DataFrame,
) -> list[str]:
    dates: list[str] = []
    for datetime in portfolio_prices_sheet[DATE_PRICE_COLUMN]:
        dates.append(pandas.to_datetime(datetime).date())
    return dates


def get_assets_entities(assets: set[str]) -> dict[str, Asset]:
    asset_entities: dict[str, Asset] = {}
    for asset in assets:
        asset_entities[asset] = Asset(name=asset)

    return asset_entities


def get_portfolio_entities(portfolios: set[str]) -> dict[str, Portfolio]:
    portfolio_entities: dict[str, Portfolio] = {}
    for portfolio in portfolios:
        portfolio_entities[portfolio] = Portfolio(name=portfolio)

    return portfolio_entities


def get_date_entities(dates: set[str]) -> dict[str, Date]:
    dates_entities: dict[str, Date] = {}
    for date in dates:
        dates_entities[date] = Date(date=date)

    return dates_entities


def get_normalized_weights(
    portfolio_weights_sheet: pandas.DataFrame,
    portfolios: set[str],
    portfolio_entities: dict[str, Portfolio],
    asset_entities: dict[str, Asset],
    date_entities: dict[str, Date],
) -> list[Weight]:
    portfolio_weights_sheet_as_dict = portfolio_weights_sheet.to_dict(
        'records')
    weights: list[Weight] = []
    for weight_row in portfolio_weights_sheet_as_dict:
        for portfolio in portfolios:
            weight_entity = Weight(
                date=date_entities[
                    pandas.to_datetime(weight_row[DATE_WEIGHT_COLUMN]).date()
                ],
                asset=asset_entities[weight_row[ASSET_WEIGHT_COLUMN]],
                portfolio=portfolio_entities[portfolio],
                weight=weight_row[portfolio]
            )
            weights.append(weight_entity)

    return weights


def get_normalized_prices(
    portfolio_prices_sheet: pandas.DataFrame,
    assets: set[str],
    asset_entities: dict[str, Asset],
    date_entities: dict[str, Date],
) -> list[Price]:
    portfolio_prices_sheet_as_dict = portfolio_prices_sheet.to_dict('records')
    prices: list[Price] = []
    for price_row in portfolio_prices_sheet_as_dict:
        for asset in assets:
            price_entity = Price(
                date=date_entities[
                    pandas.to_datetime(price_row[DATE_PRICE_COLUMN]).date()
                ],
                asset=asset_entities[asset],
                price=price_row[asset]
            )
            prices.append(price_entity)

    return prices


def get_quantities(
    initial_value: float,
    initial_date: str,
    dates: list[str],
    assets_entities: list[Asset],
    portfolios_entities: list[Portfolio],
    weights_entities: list[Weight],
    prices_entities: list[Price],
    date_entities: dict[str, Date],
) -> list[Quantity]:
    initial_quantities: list[Quantity] = []
    for weight in weights_entities:
        initial_price_for_asset = next(
            price for price in prices_entities
            if str(price.date.date) == initial_date and
            price.asset.name == weight.asset.name
        )
        initial_quantity = (initial_value*weight.weight) / \
            initial_price_for_asset.price
        initial_quantities.append(
            Quantity(
                date=weight.date,
                asset=weight.asset,
                portfolio=weight.portfolio,
                quantity=initial_quantity
            )
        )

    quantities: list[Quantity] = []
    for date in dates:
        for quantity in initial_quantities:
            # print(date)
            # print(quantity.quantity)
            quantities.append(
                Quantity(
                    date=date_entities[date],
                    asset=quantity.asset,
                    portfolio=quantity.portfolio,
                    quantity=quantity.quantity
                )
            )

    return quantities


def transaction_save(
    asset_entities: list[Asset],
    portfolio_entities: list[Portfolio],
    weight_entities: list[Weight],
    price_entities: list[Price],
    quantities_entities: list[Quantity],
    dates_entities: list[Date],
) -> None:
    for asset in asset_entities:
        asset.save()

    for portfolio in portfolio_entities:
        portfolio.save()

    for weight in weight_entities:
        weight.save()

    for price in price_entities:
        price.save()

    for quantity in quantities_entities:
        quantity.save()

    for date in dates_entities:
        date.save()


@transaction.atomic()
def execute():
    file_path = os.environ['FILE_PATH_PORTFOLIO_DATA']
    portfolio_weights_sheet = pandas.read_excel(file_path, WEIGHTS_SHEET_NAME)
    portfolio_prices_sheet = pandas.read_excel(file_path, PRICES_SHEET_NAME)

    assets = get_assets(portfolio_weights_sheet, portfolio_prices_sheet)
    portfolios = get_portfolios(portfolio_weights_sheet)
    dates = get_dates(portfolio_prices_sheet)

    asset_entities = get_assets_entities(assets)
    portfolio_entities = get_portfolio_entities(
        portfolios
    )
    dates_entities = get_date_entities(dates)

    weights_entities = get_normalized_weights(
        portfolio_weights_sheet,
        portfolios,
        portfolio_entities,
        asset_entities,
        dates_entities
    )
    prices_entities = get_normalized_prices(
        portfolio_prices_sheet,
        assets,
        asset_entities,
        dates_entities
    )

    quantities_entities = get_quantities(
        1000000000,
        '2022-02-15',
        dates,
        list(asset_entities.values()),
        list(portfolio_entities.values()),
        weights_entities,
        prices_entities,
        dates_entities
    )

    # print("quantities", quantities_entities)

    transaction_save(
        list(asset_entities.values()),
        list(portfolio_entities.values()),
        list(dates_entities.values()),
        weights_entities,
        prices_entities,
        quantities_entities,
    )

    return assets
