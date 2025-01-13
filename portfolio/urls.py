from django.urls import path
from portfolio.apis import PortfolioTotal, PortfolioWeight, PortfolioLoadData

# from . import views

urlpatterns = [
    path("weights", PortfolioWeight.as_view(), name="portfolio_data"),
    path("totals", PortfolioTotal.as_view(), name="portfolio_data"),
    path("load-data", PortfolioLoadData.as_view(), name="load-data"),
]
