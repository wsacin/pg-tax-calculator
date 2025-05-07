import pytest
from tests.conftest import FakeTaxApi
from waltax.repository import TaxBracketRepository
from decimal import Decimal, getcontext, ROUND_UP

"""
response_template = {
    "total_taxes_owed": Decimal,
    "taxes_owed_per_bracket": {
        "<rate>" {
            "min": Decimal,
            "max": Decimal,
            "owed": Decimal,
        },
    },
}
"""
getcontext().prec = 2
getcontext().rounding = ROUND_UP


class TestTaxBracketRepssitory:
    """
    Tests a few paths:
    1.  Happy path, where we calculate the income based
        on a successful request.
    2.  Catching random failure.
    3.  Catching existing error on "out of bounds" year.
    """

    @pytest.fixture
    def repository(self):
        return TaxBracketRepository(api_client=FakeTaxApi)

    @pytest.mark.parametrize(
        "income, year, expected",
        [
            (
                Decimal("50000.00"),
                2022,
                {
                    "total_taxes_owed": Decimal("7500.00"),
                    "effective_rate": Decimal("0.15"),
                    "taxes_owed_per_bracket": {
                        Decimal("0.15"): {
                            "min": Decimal("0.00"),
                            "max": Decimal("50197.00"),
                            "owed": Decimal("7500.00"),
                        },
                    },
                },
            ),
        ],
    )
    def test_calculate_rate(self, repository, income, year, expected):
        payload = repository.calculate_rate(income, year)

        assert payload["total_taxes_owed"] == expected["total_taxes_owed"]
        assert payload["effective_rate"] == expected["effective_rate"]

        expected_per_bracket = expected["taxes_owed_per_bracket"]
        for rate, bracket in payload["taxes_owed_per_bracket"].items():
            assert expected_per_bracket[rate]["min"] == bracket["min"]
            assert expected_per_bracket[rate]["max"] == bracket["max"]
            assert expected_per_bracket[rate]["owed"] == bracket["owed"]
