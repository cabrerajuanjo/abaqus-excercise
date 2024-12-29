import os
import pandas


def etl():
    file_path = os.environ['FILE_PATH_PORTFOLIO_DATA']
    WEIGHTS_SHEET_NAME = 'weights'
    PRICES_SHEET_NAME = 'Precios'

    portfolio_weights = pandas.read_excel(file_path, WEIGHTS_SHEET_NAME)
    portfolio_prices = pandas.read_excel(file_path, PRICES_SHEET_NAME)
    return portfolio_prices
