from django.db import models


# TODO: change ON_CASCADE for DO_NOTHING

class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"


class Asset(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}"


class Portfolio(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}"


class Price(models.Model):
    class Meta:
        unique_together = (('id', 'date', 'asset'),)

    date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.FloatField()


class Weight(models.Model):
    class Meta:
        unique_together = (('id', 'date', 'asset', 'portfolio'),)

    date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    weight = models.FloatField()


class Quantity(models.Model):
    class Meta:
        unique_together = (('id', 'date', 'asset', 'portfolio'),)

    date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Amount(models.Model):
    class Meta:
        unique_together = (('id', 'date', 'asset', 'portfolio'),)

    date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    amount = models.FloatField()
