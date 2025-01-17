from django.urls import path
from portfolio.apis import (
    PortfolioTotal,
    PortfolioWeight,
    PortfolioLoadData,
    PortfolioTransact,
    PortfolioReset
)

# from . import views

urlpatterns = [
    path("weights", PortfolioWeight.as_view(), name="portfolio_data"),
    path("totals", PortfolioTotal.as_view(), name="portfolio_data"),
    path("load-data", PortfolioLoadData.as_view(), name="load-data"),
    path("transact", PortfolioTransact.as_view(), name="transact-amount"),
    path("reset", PortfolioReset.as_view(), name="reset"),
]
