from django.contrib import admin

from portfolio.models import (
    Price,
    Amount,
    Date,
    Portfolio,
    Asset
)

admin.site.register(Price)
admin.site.register(Amount)
admin.site.register(Date)
admin.site.register(Portfolio)
admin.site.register(Asset)
