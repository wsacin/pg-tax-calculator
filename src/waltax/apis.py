"""
API Clients that feed into repository layer.

Contains:

    * TaxApiClient -> Fetches tax rate brackets.
"""

import time
import requests


class TaxApiClient:
    # TODO: Move this into a config, depending if it
    #       lives in the same docker net or not.
    HOST_URL = "http://localhost:5001/"
    ENDPOINT_PATH = "/tax-calculator/tax-year/{year}"
    BASE_URL = HOST_URL + ENDPOINT_PATH
    BACKOFF_STAGES = [0.2, 0.5, 1.5]

    def get_rates(self, year):
        """
        Calls the endpoint under BASE_URL. If request fails,
        backs off periodically until RuntimeError is raised.
        """
        base_url = self.BASE_URL.format(year=year)

        for t in self.BACKOFF_STAGES:
            response = requests.get(base_url)

            if response.status_code == 200:
                # let the repository randle serialization
                return response.text

            time.sleep(t)

        raise ValueError(
            f"Could not get response from {self.ENDPOINT_PATH.format(year=year)}"
        )
