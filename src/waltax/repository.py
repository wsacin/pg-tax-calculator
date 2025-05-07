from waltax.apis import TaxApiClient


class TaxBracketRepository:

    def __init__(self, api_client=TaxApiClient):
        self._tax_api = TaxApiClient()

    def get_rates(year):
        # for now a fake call with no error handling
        return self._tax_api.get(f"/tax-calculator/tax-year/{year}")

    def calculate_rate(self, annual_income, year):
        return "broken response"
