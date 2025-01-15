from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Asset, Portfolio, Date, Price, Amount
import pandas as pd
import io


class PortfolioAPITest(TestCase):
    def setUp(self):
        self.weights_data = {
            "Fecha": ["2023-01-01", "2023-01-01"],
            "activos": ["Activo 1", "Activo 2"],
            "portafolio 1": [0.6, 0.4],
            "portafolio 2": [0.8, 0.5]
        }
        self.prices_data = {
            "Dates": ["2023-01-01", "2023-01-02"],
            "Activo 1": [100, 102],
            "Activo 2": [200, 198]
        }

        self.weights_df = pd.DataFrame(self.weights_data)
        self.prices_df = pd.DataFrame(self.prices_data)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            self.weights_df.to_excel(writer, sheet_name="weights", index=False)
            self.prices_df.to_excel(writer, sheet_name="Precios", index=False)
        buffer.seek(0)

        self.mock_excel_file = SimpleUploadedFile(
            "test.xlsx",
            buffer.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        self.initial_total = 100000

    def test_api_upload(self):
        response = self.client.post('/portfolio/load-data', {
            'file': self.mock_excel_file,
            'initial_total': self.initial_total
        }, format='multipart')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Asset.objects.count(), 2)
        self.assertEqual(Portfolio.objects.count(), 2)
        self.assertEqual(Date.objects.count(), 2)
        self.assertEqual(Price.objects.count(), 4)
        self.assertEqual(Amount.objects.count(), 8)

        date = Date.objects.get(date="2023-01-02")
        self.assertEqual(str(date.date), "2023-01-02")
        asset = Asset.objects.get(name="Activo 1")
        self.assertEqual(str(asset.name), "Activo 1")
        portfolio = Portfolio.objects.get(name="portafolio 1")
        self.assertEqual(str(portfolio.name), "portafolio 1")
        # amount for initial_total 100000, Activo 1, 2023-01-02, portafolio 1
        # q0 = (w0 * it)/p0
        # amount = q0*pt
        # q0 = (0.6 * 100000)/100 = 600
        # amount = 600*102 = 61200
        amount = Amount.objects.get(
            date_id=date.id, asset_id=asset.id, portfolio_id=portfolio.id)
        self.assertEqual(amount.amount, 61200)
