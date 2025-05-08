import logging
from waltax.utils import quantized_decimal
from waltax.apis import TaxApiClient
from decimal import Decimal


logger = logging.Logger(__name__)


class TaxBracketRepository:

    def __init__(self, api_client=TaxApiClient):
        self._tax_api = api_client()

    def get_rates(self, year):
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
        # for now a fake call with no error handling
        return self._tax_api.get_rates(year)

    def _calculate_tax_delta(self, bracket_max, bracket_min, annual_income):
        if bracket_max is None:
            taxable_max = annual_income
        elif annual_income > bracket_max:
            taxable_max = bracket_max
        else:
            taxable_max = annual_income

        return taxable_max - bracket_min

    def calculate_rate(self, annual_income, year):
        logger.info("Start income: %.2f" % annual_income)

        brackets = self.get_rates(year)["tax_brackets"]

        payload = {
            "total_taxes_owed": Decimal("0.00"),
            "effective_rate": Decimal("0.00"),
        }

        if annual_income == 0:
            return payload

        payload["taxes_owed_per_bracket"] = {}

        remaining_income = Decimal(annual_income)
        quantized_income = Decimal(annual_income)

        for bracket in brackets:
            if remaining_income <= 0:
                break

            bracket_min = bracket.get("min")
            bracket_max = bracket.get("max")
            rate_key = bracket["rate"]
            rate = Decimal(rate_key)

            tax_delta = self._calculate_tax_delta(
                bracket_max, bracket_min, quantized_income
            )

            amount_owed = rate * tax_delta
            logger.info(f"Amount owed: %.2f" % amount_owed)

            payload["total_taxes_owed"] += amount_owed

            bracket_breakdown = {
                "min": quantized_decimal(bracket_min),
                "owed": quantized_decimal(amount_owed),
            }
            if bracket_max:
                bracket_breakdown["max"] = bracket_max
            payload["taxes_owed_per_bracket"][rate_key] = bracket_breakdown

            logger.info(f"Amount owed in this bracket: %.2f" % amount_owed)

            remaining_income -= tax_delta
            logger.info(f"Remaining taxable: %.2f" % remaining_income)

        # calculate effective_rate
        payload["effective_rate"] = quantized_decimal(
            payload["total_taxes_owed"] / quantized_income
        )

        # quantize
        payload["total_taxes_owed"] = quantized_decimal(payload["total_taxes_owed"])

        return payload
