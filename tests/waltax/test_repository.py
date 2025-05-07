import pytest
from tests.conftest import FakeTaxApi
from waltax.repository import TaxBracketRepository
from decimal import Decimal

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


class TestTaxBracketRepository:
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
                Decimal(50000.00),
                2022,
                {
                    "total_taxes_owed": Decimal(7500.00),
                    "marginal_rate": None,  # not sure yet
                    "taxes_owed_per_bracket": {
                        Decimal(0.25): {
                            "min": Decimal(0.00),
                            "max": Decimal(50197.00),
                            "owed": Decimal(7500.00),
                        },
                    },
                },
            ),
        ],
    )
    def test_calculate_rate(self, repository, income, year, expected):
        assert repository.calculate_rate(income, year) == expected
