import logging
from waltax.utils import quantized_decimal
from waltax.apis import TaxApiClient
from decimal import Decimal
from marshmallow import Schema, fields


logger = logging.Logger(__name__)


class TaxBracketSchema(Schema):
    max = fields.Decimal()
    min = fields.Decimal()
    rate = fields.Method(serialize="load_rate", deserialize="load_rate")

    def load_rate(self, obj):
        return str(obj)


class TaxYearSchema(Schema):
    tax_brackets = fields.List(fields.Nested(TaxBracketSchema))


class TaxBracketRepository:

    ALLOWED_YEARS = [2019, 2020, 2021, 2022]

    def __init__(self, api_client=TaxApiClient):
        self._tax_api = api_client()

    def _validate_year(self, year):
        if year not in self.ALLOWED_YEARS:
            raise ValueError(f"The year {year} is not supported.")

    def _calculate_tax_delta(self, bracket_max, bracket_min, annual_income):
        if bracket_max and annual_income > bracket_max:
            taxable_max = bracket_max
        else:
            taxable_max = annual_income

        return taxable_max - bracket_min

    def _build_bracket_breakdown(self, bracket, annual_income):
        bracket_min = bracket.get("min")
        bracket_max = bracket.get("max")
        rate = Decimal(bracket["rate"])

        tax_delta = self._calculate_tax_delta(bracket_max, bracket_min, annual_income)

        amount_owed = rate * tax_delta

        logger.info(f"Amount owed: %.2f" % amount_owed)

        bracket_breakdown = {
            "min": quantized_decimal(bracket_min),
            "owed": quantized_decimal(amount_owed),
        }
        if bracket_max:
            bracket_breakdown["max"] = bracket_max

        return bracket_breakdown, tax_delta

    def get_rates(self, year):
        """
        Calls API to get tax brackets for specific year.
        """
        self._validate_year(year)
        rates_content = self._tax_api.get_rates(year)
        rates = TaxYearSchema().loads(rates_content)

        return rates

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

            rate_key = bracket["rate"]
            bracket_breakdown, tax_delta = self._build_bracket_breakdown(
                bracket, annual_income
            )
            owed_in_bracket = bracket_breakdown["owed"]

            payload["total_taxes_owed"] += owed_in_bracket
            payload["taxes_owed_per_bracket"][rate_key] = bracket_breakdown

            logger.info(f"Amount owed in this bracket: %.2f" % owed_in_bracket)

            remaining_income -= tax_delta
            logger.info(f"Remaining taxable: %.2f" % remaining_income)

        # calculate effective_rate
        payload["effective_rate"] = quantized_decimal(
            payload["total_taxes_owed"] / quantized_income
        )

        # quantize
        payload["total_taxes_owed"] = quantized_decimal(payload["total_taxes_owed"])

        return payload
