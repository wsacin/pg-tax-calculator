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
                50000,
                2022,
                {
                    "total_taxes_owed": Decimal(7500),
                    "marginal_rate": None,  # not sure yet
                    "taxes_owed_per_bracket": {
                        Decimal(0.25): {
                            "min": Decimal(0),
                            "max": Decimal(50197),
                            "owed": Decimal(7500),
                        },
                    },
                },
            ),
        ],
    )
    def test_calculate_rate(self, repository, income, year, expected):
        assert repository.calculate_rate(income, year) == expected
