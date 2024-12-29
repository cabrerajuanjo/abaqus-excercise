from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Price(models.Model):
    class Meta:
        unique_together = (('date', 'asset'),)

    date = models.DateField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.FloatField()


class Weight(models.Model):
    class Meta:
        unique_together = (('date', 'asset', 'portfolio'),)

    date = models.DateField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    weight = models.FloatField()
