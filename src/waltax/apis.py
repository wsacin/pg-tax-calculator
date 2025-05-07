"""
API Clients that feed into repository layer.

Contains:

    * TaxApiClient -> Fetches tax rate brackets.
"""

import requests
from decimal import Decimal


class TaxApiClient:
    BASE_URL = "/tax-calculator/tax-year/"

    def get_rates(self, year):
        # mock request.
        # This might serve as a contract test initially.
        return {
            "tax_brackets": [
                {"min": Decimal(0), "max": Decimal(50197), "rate": Decimal(0.15)},
                {"min": Decimal(50197), "max": Decimal(100392), "rate": Decimal(0.205)},
                {"min": Decimal(100392), "max": Decimal(155625), "rate": Decimal(0.26)},
                {"min": Decimal(155625), "max": Decimal(221708), "rate": Decimal(0.29)},
                {"min": Decimal(221708), "rate": Decimal(0.33)},
            ]
        }
