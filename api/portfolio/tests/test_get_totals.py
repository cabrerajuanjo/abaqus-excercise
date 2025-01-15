from django.test import TestCase
from portfolio.models import Amount, Asset, Portfolio, Date
from datetime import date


class GetTotalsTest(TestCase):
    def setUp(self):
        self.asset1 = Asset.objects.create(name="Activo 1")
        self.asset2 = Asset.objects.create(name="Activo 2")
        self.portfolio1 = Portfolio.objects.create(name="portafolio 1")
        self.portfolio2 = Portfolio.objects.create(name="portafolio 2")
        self.dates = [
            Date.objects.create(date=date(2023, 1, 1)),
            Date.objects.create(date=date(2023, 1, 2)),
        ]

        self.amounts = [
            Amount.objects.create(
                date=self.dates[0], portfolio=self.portfolio1, asset=self.asset1, amount=1000
            ),
            Amount.objects.create(
                date=self.dates[0], portfolio=self.portfolio1, asset=self.asset2, amount=2000
            ),
            Amount.objects.create(
                date=self.dates[0], portfolio=self.portfolio2, asset=self.asset1, amount=3000
            ),
            Amount.objects.create(
                date=self.dates[0], portfolio=self.portfolio2, asset=self.asset2, amount=4000
            ),
            Amount.objects.create(
                date=self.dates[1], portfolio=self.portfolio1, asset=self.asset1, amount=1500
            ),
            Amount.objects.create(
                date=self.dates[1], portfolio=self.portfolio1, asset=self.asset2, amount=2500
            ),
            Amount.objects.create(
                date=self.dates[1], portfolio=self.portfolio2, asset=self.asset1, amount=3500
            ),
            Amount.objects.create(
                date=self.dates[1], portfolio=self.portfolio2, asset=self.asset2, amount=4500
            ),
        ]

    def test_get_weights_api(self):
        url = '/portfolio/totals'
        filters = {
            "date__gt": "2023-01-01",
            "date__lt": "2023-01-03",
        }
        expected_second_weight = {
            "date": "2023-01-02",
            "portfolio": "portafolio 1",
            "total_amount": 4000
        }

        response = self.client.get(url, data=filters)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertDictEqual(response.data[1], expected_second_weight)
