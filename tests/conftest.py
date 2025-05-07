"""
This module contains reusable pytest fixtures that
can be used throughout the whole project. This package
can be modularized depending on the domain needs.
"""

import pytest

from waltax.apis import TaxApiClient
from decimal import Decimal


# @pytest.fixture
def tax_brackets_2022_response():
    return {
        "tax_brackets": [
            {
                "min": Decimal("0"),
                "max": Decimal("50197"),
                "rate": Decimal("0.15"),
            },
            {
                "min": Decimal("50197"),
                "max": Decimal("100392"),
                "rate": Decimal("0.205"),
            },
            {
                "min": Decimal("100392"),
                "max": Decimal("155625"),
                "rate": Decimal("0.26"),
            },
            {
                "min": Decimal("155625"),
                "max": Decimal("221708"),
                "rate": Decimal("0.29"),
            },
            {
                "min": Decimal("221708"),
                "rate": Decimal("0.33"),
            },
        ]
    }


@pytest.fixture
def error_response():
    pass


class FakeTaxApi(TaxApiClient):

    def get_rates(self, year):
        return tax_brackets_2022_response()
