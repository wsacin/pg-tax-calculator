"""
API Clients that feed into repository layer.

Contains:

    * TaxApiClient -> Fetches tax rate brackets.
"""

from decimal import Decimal


class TaxApiClient:
    BASE_URL = "/tax-calculator/tax-year/{year}"

    def get_rates(self, year):
        # mock request.
        # This might serve as a contract test initiallyo.
        # return requests.get(self.BASE_URL.format(year=year))
        return {
            "tax_brackets": [
                {
                    "min": Decimal("0.00"),
                    "max": Decimal("50197.00"),
                    "rate": "0.15",
                },
                {
                    "min": Decimal("50197.00"),
                    "max": Decimal("100392.00"),
                    "rate": "0.205",
                },
                {
                    "min": Decimal("100392.00"),
                    "max": Decimal("155625.00"),
                    "rate": "0.26",
                },
                {
                    "min": Decimal("155625.00"),
                    "max": Decimal("221708.00"),
                    "rate": "0.29",
                },
                {
                    "min": Decimal("221708.00"),
                    "rate": "0.33",
                },
            ]
        }
