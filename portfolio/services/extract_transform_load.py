import os
import pandas
from portfolio.models.models import Asset, Price, Portfolio, Weight


def get_portfolios(portfolio_weights_sheet: pandas.DataFrame) -> set[str]:

    COLUMNS_TO_IGNORE_IN_WEIGHTS_SHEET = ('activos', 'Fecha')

    portfolios: set[str] = set([])
    for column in portfolio_weights_sheet.columns:
        if column not in COLUMNS_TO_IGNORE_IN_WEIGHTS_SHEET:
            portfolios.add(column)

    return portfolios


def get_assets(portfolio_weights_sheet: pandas.DataFrame, portfolio_prices_sheet: pandas.DataFrame) -> set[str]:
    COLUMNS_TO_IGNORE_IN_PRICES_SHEET = ('Dates')
    WEIGHTS_SHEET_ASSET_COLUMN_NAME = 'activos'
    assets: set[str] = set([])
    for column in portfolio_prices_sheet.columns:
        if column not in COLUMNS_TO_IGNORE_IN_PRICES_SHEET:
            assets.add(column)

    for asset in portfolio_weights_sheet[WEIGHTS_SHEET_ASSET_COLUMN_NAME]:
        assets.add(asset)

    return assets


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


def get_normalized_weights(portfolio_weights_sheet: pandas.DataFrame, portfolios, portfolio_entities, asset_entities) -> list[Weight]:
    portfolio_weights_sheet_as_dict = portfolio_weights_sheet.to_dict('records')
    weights: list[Weight] = []
    for weight_row in portfolio_weights_sheet_as_dict:
        for portfolio in portfolios:
            weight_entity = Weight(date=weight_row["Fecha"], asset=asset_entities[weight_row["activos"]], portfolio=portfolio_entities[portfolio], weight=weight_row[portfolio])
            weights.append(weight_entity)

    return weights

def get_normalized_prices(portfolio_prices_sheet: pandas.DataFrame, assets, asset_entities) -> list[Price]:
    portfolio_prices_sheet_as_dict = portfolio_prices_sheet.to_dict('records')
    prices: list[Price] = []
    for price_row in portfolio_prices_sheet_as_dict:
        for asset in assets:
            price_entity = Price(date=price_row["Dates"], asset=asset_entities[asset], price=price_row[asset])
            prices.append(price_entity)

    return prices 


def etl():
    file_path = os.environ['FILE_PATH_PORTFOLIO_DATA']
    WEIGHTS_SHEET_NAME = 'weights'
    PRICES_SHEET_NAME = 'Precios'
    portfolio_weights_sheet = pandas.read_excel(file_path, WEIGHTS_SHEET_NAME)
    portfolio_prices_sheet = pandas.read_excel(file_path, PRICES_SHEET_NAME)

    assets = get_assets(portfolio_weights_sheet, portfolio_prices_sheet)
    portfolios = get_portfolios(portfolio_weights_sheet)

    asset_entities: dict[str, Asset] = get_assets_entities(assets)
    portfolio_entities: dict[str, Portfolio] = get_portfolio_entities(portfolios)



    weights_entities = get_normalized_weights(portfolio_weights_sheet, portfolios, portfolio_entities, asset_entities)
    prices_entities = get_normalized_prices(portfolio_prices_sheet, assets, asset_entities)

    for asset in asset_entities.values():
        asset.save()
        
    for portfolio in portfolio_entities.values():
        portfolio.save()

    for weight in weights_entities:
        weight.save()

    for price in prices_entities:
        price.save()

    return assets
