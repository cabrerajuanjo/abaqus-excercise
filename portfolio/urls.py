from django.urls import path
from portfolio.apis import PortfolioData

# from . import views

urlpatterns = [
    path("v1/portfolio-data", PortfolioData.as_view(), name="portfolio_data"),
    path("v1/load-data", PortfolioData.as_view(), name="portfolio_data"),
]
