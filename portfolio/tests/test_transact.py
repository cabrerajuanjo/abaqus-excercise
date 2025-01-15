from django.test import TestCase
from portfolio.models import Amount, Price, Asset, Portfolio, Date
from datetime import date


class ExecuteFunctionTest(TestCase):
    def setUp(self):
        self.asset = Asset.objects.create(name="TestAsset")
        self.portfolio = Portfolio.objects.create(name="TestPortfolio")
        self.dates = [
            Date.objects.create(date=date(2023, 1, 1)),
            Date.objects.create(date=date(2023, 1, 2)),
            Date.objects.create(date=date(2023, 1, 3)),
        ]

        self.prices = [
            Price.objects.create(
                date=self.dates[0],
                asset=self.asset,
                price=100
            ),
            Price.objects.create(
                date=self.dates[1],
                asset=self.asset,
                price=105
            ),
            Price.objects.create(
                date=self.dates[2],
                asset=self.asset,
                price=110
            ),
        ]

        self.amounts = [
            Amount.objects.create(
                date=self.dates[0],
                portfolio=self.portfolio,
                asset=self.asset,
                amount=5000
            ),
            Amount.objects.create(
                date=self.dates[1],
                portfolio=self.portfolio,
                asset=self.asset,
                amount=5050
            ),
            Amount.objects.create(
                date=self.dates[2],
                portfolio=self.portfolio,
                asset=self.asset,
                amount=5100
            ),
        ]

    def test_buy_transaction(self):
        self.client.post('/portfolio/transact', {
            "date": "2023-01-02",
            "portfolio": "TestPortfolio",
            "asset": "TestAsset",
            "operation": "BUY",
            "amount": 2000
        }, format='application/json')

        updated_amounts = Amount.objects.filter(
            portfolio=self.portfolio,
            asset=self.asset
        ).order_by("date__date")

        self.assertEqual(
            updated_amounts[1].amount,
            7050
        )

        self.assertAlmostEqual(
            updated_amounts[2].amount,
            7385.714,
            places=3
        )

    def test_sell_transaction(self):
        self.client.post('/portfolio/transact', {
            "date": "2023-01-02",
            "portfolio": "TestPortfolio",
            "asset": "TestAsset",
            "operation": "SELL",
            "amount": 1000
        }, format='application/json')

        updated_amounts = Amount.objects.filter(
            portfolio=self.portfolio, asset=self.asset
        ).order_by("date__date")

        self.assertEqual(
            updated_amounts[1].amount,
            4050
        )

        self.assertAlmostEqual(
            updated_amounts[2].amount,
            4242.857,
            places=3
        )
