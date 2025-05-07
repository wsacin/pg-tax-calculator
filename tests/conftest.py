"""
This module contains reusable pytest fixtures that
can be used throughout the whole project. This package
can be modularized depending on the domain needs.
"""

import pytest


from waltax.apis import TaxApiClient


@pytest.fixture
def tax_brackets_2022_response():
    return {
        "tax_brackets": [
            {"min": 0, "max": 50197, "rate": 0.15},
            {"min": 50197, "max": 100392, "rate": 0.205},
            {"min": 100392, "max": 155625, "rate": 0.26},
            {"min": 155625, "max": 221708, "rate": 0.29},
            {"min": 221708, "rate": 0.33},
        ]
    }


@pytest.fixture
def error_response():
    pass


class FakeTaxApi(TaxApiClient):

    def get_rates(self, year):
        return tax_brackets_2022_response()
