from django.urls import path
from portfolio.apis import PortfolioData

# from . import views

urlpatterns = [
    path("", PortfolioData.as_view(), name="portfolio_data"),
    path("load-data", PortfolioData.as_view(), name="load-data"),
]
