from django.db import transaction
from portfolio.models import (
    Asset,
    Price,
    Portfolio,
    Date,
    Amount
)


@transaction.atomic()
def execute():
    Asset.objects.all().delete()
    Price.objects.all().delete()
    Portfolio.objects.all().delete()
    Date.objects.all().delete()
    Amount.objects.all().delete()
