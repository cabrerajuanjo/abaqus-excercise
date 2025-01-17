from django.urls import path
from portfolio.apis import (
    PortfolioTotal,
    PortfolioWeight,
    PortfolioLoadData,
    PortfolioTransact,
    PortfolioReset,
    PortfolioPortfolios,
    PortfolioAssets,
    PortfolioDates,
)

# from . import views

urlpatterns = [
    path("weights", PortfolioWeight.as_view(), name="portfolio_data"),
    path("totals", PortfolioTotal.as_view(), name="portfolio_data"),
    path("load-data", PortfolioLoadData.as_view(), name="load-data"),
    path("transact", PortfolioTransact.as_view(), name="transact-amount"),
    path("reset", PortfolioReset.as_view(), name="reset"),
    path("portfolios", PortfolioPortfolios.as_view(), name="portfolios"),
    path("assets", PortfolioAssets.as_view(), name="assets"),
    path("dates", PortfolioDates().as_view(), name="dates"),
]
