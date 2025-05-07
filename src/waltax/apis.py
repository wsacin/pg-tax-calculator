"""
API Clients that feed into repository layer.

Contains:

    * TaxApiClient -> Fetches tax rate brackets.
"""

import requests


class TaxApiClient:

    def get_rates(year):
        # mock request.
        # This might serve as a contract test initially.
        return {
            "tax_brackets": [
                {"min": 0, "max": 50197, "rate": 0.15},
                {"min": 50197, "max": 100392, "rate": 0.205},
                {"min": 100392, "max": 155625, "rate": 0.26},
                {"min": 155625, "max": 221708, "rate": 0.29},
                {"min": 221708, "rate": 0.33},
            ]
        }
