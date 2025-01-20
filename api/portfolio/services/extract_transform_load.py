from django.db import transaction
import pandas
from portfolio.models import (
    Asset,
    Price,
    Portfolio,
    Date,
    Amount
)

SPREAD_SHEET_DATE_PRICE_COLUMN = 'Dates'
SPREAD_SHEET_DATE_WEIGHT_COLUMN = 'Fecha'
SPREAD_SHEET_ASSET_WEIGHT_COLUMN = 'activos'

PORTFOLIO_COLUMN_NAME = 'portfolio'
WEIGHT_COLUMN_NAME = 'weight'
ASSET_COLUMN_NAME = 'asset'
PRICE_COLUMN_NAME = 'price'
DATE_COLUMN_NAME = 'date'
QUANTITY_COLUMN_NAME = 'quantity'

WEIGHTS_SHEET_NAME = 'weights'
PRICES_SHEET_NAME = 'Precios'


def get_portfolios(portfolio_weights_sheet: pandas.DataFrame) -> set[str]:

    COLUMNS_TO_IGNORE_IN_WEIGHTS_SHEET = (
        SPREAD_SHEET_ASSET_WEIGHT_COLUMN, SPREAD_SHEET_DATE_WEIGHT_COLUMN
    )

    portfolios: set[str] = set([])
    for column in portfolio_weights_sheet.columns:
        if column not in COLUMNS_TO_IGNORE_IN_WEIGHTS_SHEET:
            portfolios.add(column)

    return portfolios


def get_assets(
    portfolio_weights_sheet: pandas.DataFrame,
    portfolio_prices_sheet: pandas.DataFrame,
) -> set[str]:
    COLUMNS_TO_IGNORE_IN_PRICES_SHEET = (SPREAD_SHEET_DATE_PRICE_COLUMN)
    WEIGHTS_SHEET_ASSET_COLUMN_NAME = SPREAD_SHEET_ASSET_WEIGHT_COLUMN
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
    for datetime in portfolio_prices_sheet[SPREAD_SHEET_DATE_PRICE_COLUMN].sort_values():
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
) -> pandas.DataFrame:
    normalized_weights = portfolio_weights_sheet.melt(
        id_vars=(SPREAD_SHEET_DATE_WEIGHT_COLUMN,
                 SPREAD_SHEET_ASSET_WEIGHT_COLUMN),
        value_vars=list(portfolios),
        var_name=PORTFOLIO_COLUMN_NAME,
        value_name=WEIGHT_COLUMN_NAME
    ).rename(columns={
        SPREAD_SHEET_ASSET_WEIGHT_COLUMN: ASSET_COLUMN_NAME,
        SPREAD_SHEET_DATE_WEIGHT_COLUMN: DATE_COLUMN_NAME
    })

    return normalized_weights


def get_normalized_prices(
    portfolio_prices_sheet: pandas.DataFrame,
    assets: set[str],
) -> pandas.DataFrame:
    normalized_prices = portfolio_prices_sheet.melt(
        id_vars=SPREAD_SHEET_DATE_PRICE_COLUMN,
        value_vars=list(assets),
        var_name=ASSET_COLUMN_NAME,
        value_name=PRICE_COLUMN_NAME
    ).rename(
        columns={SPREAD_SHEET_DATE_PRICE_COLUMN: DATE_COLUMN_NAME}
    ).sort_values(DATE_COLUMN_NAME)

    return normalized_prices


def get_quantities(
    initial_value: float,
    initial_date: str,
    prices_dataframe: pandas.DataFrame,
    weights_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    quantities_dataframe = prices_dataframe[
        prices_dataframe[DATE_COLUMN_NAME] == initial_date
    ].join(
        weights_dataframe.set_index(ASSET_COLUMN_NAME).drop(
            columns=(DATE_COLUMN_NAME)
        ), on=ASSET_COLUMN_NAME
    )

    quantities_dataframe[QUANTITY_COLUMN_NAME] = (
        initial_value*quantities_dataframe.weight)/quantities_dataframe.price

    return quantities_dataframe


def get_amounts(
    prices_dataframe: pandas.DataFrame,
    quantity_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    # TODO: calculate amouts here
    amounts = prices_dataframe.merge(
        quantity_dataframe.drop(
            columns=[DATE_COLUMN_NAME, PRICE_COLUMN_NAME]
        ), right_on=[ASSET_COLUMN_NAME], left_on=[ASSET_COLUMN_NAME]
    )
    return amounts


def get_price_entities(
    dates: dict[str, Date],
    portfolios: dict[str, Portfolio],
    assets: dict[str, Asset],
    prices_dataframe: pandas.DataFrame
) -> list[Price]:
    prices_entities: list[Price] = []
    for price in prices_dataframe.to_dict('records'):
        prices_entities.append(
            Price(
                date=dates[pandas.to_datetime(
                    price[DATE_COLUMN_NAME]).date()],
                asset=assets[price[ASSET_COLUMN_NAME]],
                price=price[PRICE_COLUMN_NAME]
            )
        )

    return prices_entities


def get_amounts_entities(
    dates: dict[str, Date],
    portfolios: dict[str, Portfolio],
    assets: dict[str, Asset],
    amounts_dataframe: pandas.DataFrame
) -> list[Amount]:
    amounts_entities: list[Amount] = []
    for amount in amounts_dataframe.to_dict('records'):
        amounts_entities.append(
            Amount(
                date=dates[pandas.to_datetime(
                    amount[DATE_COLUMN_NAME]).date()],
                asset=assets[amount[ASSET_COLUMN_NAME]],
                portfolio=portfolios[amount[PORTFOLIO_COLUMN_NAME]],
                amount=amount[PRICE_COLUMN_NAME]*amount[QUANTITY_COLUMN_NAME]
            )
        )

    return amounts_entities


def transaction_save(
    asset_entities: list[Asset],
    portfolio_entities: list[Portfolio],
    dates_entities: list[Date],
    price_entities: list[Price],
    amount_entities: list[Amount],
) -> None:
    for date in dates_entities:
        date.save()

    for asset in asset_entities:
        asset.save()

    for portfolio in portfolio_entities:
        portfolio.save()

    for price in price_entities:
        price.save()

    for amount in amount_entities:
        amount.save()


@transaction.atomic()
def execute(file, initial_total):
    # file_path = os.environ['FILE_PATH_PORTFOLIO_DATA']
    # file = file_path
    portfolio_weights_sheet = pandas.read_excel(file, WEIGHTS_SHEET_NAME)
    portfolio_prices_sheet = pandas.read_excel(file, PRICES_SHEET_NAME)

    assets = get_assets(portfolio_weights_sheet, portfolio_prices_sheet)
    portfolios = get_portfolios(portfolio_weights_sheet)
    dates = get_dates(portfolio_prices_sheet)

    asset_entities = get_assets_entities(assets)
    portfolio_entities = get_portfolio_entities(
        portfolios
    )
    dates_entities = get_date_entities(dates)

    weights_dataframe = get_normalized_weights(
        portfolio_weights_sheet,
        portfolios,
    )
    prices_dataframe = get_normalized_prices(
        portfolio_prices_sheet,
        assets,
    )
    quantities_dataframe = get_quantities(
        initial_total,
        str(dates[0]),
        prices_dataframe,
        weights_dataframe
    )
    amounts_dataframe = get_amounts(
        prices_dataframe,
        quantities_dataframe
    )

    price_entities = get_price_entities(
        dates_entities,
        portfolio_entities,
        asset_entities,
        prices_dataframe,
    )
    amount_entities = get_amounts_entities(
        dates_entities,
        portfolio_entities,
        asset_entities,
        amounts_dataframe,
    )

    transaction_save(
        list(asset_entities.values()),
        list(portfolio_entities.values()),
        list(dates_entities.values()),
        price_entities,
        amount_entities,
    )
