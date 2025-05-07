from decimal import Decimal
from waltax.apis import TaxApiClient


class TaxBracketRepository:

    def __init__(self, api_client=TaxApiClient):
        self._tax_api = TaxApiClient()

    def get_rates(self, year):
        # for now a fake call with no error handling
        return self._tax_api.get_rates(year)

    def calculate_rate(self, annual_income, year):
        print(f"Start income: {annual_income}")

        brackets = self.get_rates(year)["tax_brackets"]

        print(f"Rates for 2022: {brackets}")
        """
        Response:

        {
            "total_taxes_owed": number,
            "taxes_owed_per_bracket": {
                min:,
                max:
                owed:
            }
        }
        """

        payload = {
            "total_taxes_owed": Decimal(0),
            "marginal_tax_rate": None,
            "taxes_owed_per_bracket": {},
        }
        for bracket in brackets:
            tax_min = Decimal(bracket.get("min", 0)) if "min" in bracket else None
            tax_max = Decimal(bracket.get("max", 0)) if "max" in bracket else None
            rate = Decimal(bracket["rate"])
            chunk = (
                annual_income if tax_max and annual_income <= tax_max else annual_income
            )

            amount_owed = rate * chunk

            payload["total_taxes_owed"] += amount_owed
            print(f"Amount owed: {amount_owed}")

            payload["taxes_owed_per_bracket"][Decimal(0.25)] = {
                "min": tax_min,
                "max": tax_max,
                "owed": amount_owed,
            }
            print(f"Amount owed in this bracket: {amount_owed}")

            annual_income -= chunk
            print(f"Remaining taxable: {annual_income}")

        return payload
