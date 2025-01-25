from datetime import datetime, date
from typing import Union
from collections import OrderedDict
from math import ceil
from portfolio.models import Date


class DateBasedPagination:
    DEFAULT_PAGE = 1
    DEFAULT_TAKEDATES = 20
    MAX_TAKEDATES = 50

    def __init__(
            self,
            page: Union[int, None],
            takeDates: Union[int, None],
            date__lt: Union[str, None],
            date__gt: Union[str, None]
    ):
        if (not page):
            page = self.DEFAULT_PAGE

        if (not takeDates):
            takeDates = self.DEFAULT_TAKEDATES

        if (takeDates > self.MAX_TAKEDATES):
            takeDates = self.MAX_TAKEDATES

        self.page = page
        self.take_dates = takeDates
        self.date__lt = date__lt or datetime.date(datetime.max)
        self.date__gt = date__gt or datetime.date(datetime.min)

    def get_date_limits(
        self
    ) -> tuple[str, str]:
        dates = Date.objects.filter(
            date__range=(
                self.date__gt,
                self.date__lt
            ),
        ).values()
        dates_cardinal = len(dates)
        self.page_cardinal = ceil(dates_cardinal / self.take_dates)

        # TODO: handle this better
        if (self.page > self.page_cardinal):
            return "", ""

        date_slice: list[str] = []
        lower_index = (self.page-1)*self.take_dates
        date_slice = dates[lower_index:lower_index+self.take_dates]
        self.dates_in_page = len(date_slice)

        return (date_slice[0]['date'], date_slice[len(date_slice)-1]['date'])

    def add_paginated_data(self, data):
        return OrderedDict(
            [
                ("page", self.page),
                ("datesInPage", self.dates_in_page),
                ("recordsInPage", len(data)),
                ("totalPages", self.page_cardinal),
                ("results", data),
            ]
        )
