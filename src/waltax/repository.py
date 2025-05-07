from decimal import Decimal
from waltax.apis import TaxApiClient


class TaxBracketRepository:

    def __init__(self, api_client=TaxApiClient):
        self._tax_api = api_client()

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
            "total_taxes_owed": Decimal,
            "effective_rate": Decimal,
            "taxes_owed_per_bracket": {
                <rate>: {
                    min:  Decimal,
                    max:  Decimal,
                    owed: Decimal,
                }
            }
        }
        """

        payload = {
            "total_taxes_owed": Decimal(0.00),
            "effective_rate": None,
            "taxes_owed_per_bracket": {},
        }
        total_income = annual_income
        for bracket in brackets:

            tax_min = bracket.get("min")

            if annual_income <= 0:
                break

            tax_max = bracket.get("max")
            rate = Decimal(bracket["rate"])
            chunk = (
                annual_income if tax_max and annual_income <= tax_max else annual_income
            )

            amount_owed = rate * chunk

            payload["total_taxes_owed"] += amount_owed
            print(f"Amount owed: {amount_owed}")

            payload["taxes_owed_per_bracket"][rate] = {
                "min": tax_min,
                "max": tax_max,
                "owed": amount_owed,
            }
            print(f"Amount owed in this bracket: {amount_owed}")

            annual_income -= chunk
            print(f"Remaining taxable: {annual_income}")

        # calculate effective_rate
        payload["effective_rate"] = payload["total_taxes_owed"] / total_income

        return payload
