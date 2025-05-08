"""
This module contains reusable pytest fixtures that
can be used throughout the whole project. This package
can be modularized depending on the domain needs.
"""

import json
from waltax.apis import TaxApiClient


def tax_brackets_2022_response():
    """
    This fixture represents the response.text that comes
    from a successfull request made to the API.
    """

    return json.dumps(
        {
            "tax_brackets": [
                {"min": 0.00, "max": 50197.00, "rate": 0.15},
                {
                    "min": 50197.00,
                    "max": 100392.00,
                    "rate": 0.205,
                },
                {"min": 100392.00, "max": 155625.00, "rate": 0.26},
                {"min": 155625.00, "max": 221708.00, "rate": 0.29},
                {"min": 221708.00, "rate": 0.33},
            ]
        }
    )


class FakeTaxApi(TaxApiClient):

    def get_rates(self, year):
        return tax_brackets_2022_response()
