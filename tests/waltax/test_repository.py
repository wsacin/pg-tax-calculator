import pytest
from tests.conftest import FakeTaxApi
from waltax.repository import TaxBracketRepository


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
            (50000, 2022, {"total_tax_owed": 7500}),
            (100000, 2022, {"total_tax_owed": 17739.17}),
        ],
    )
    def test_yearly_calculation(self, repository, income, year, expected):
        assert repository.calculate_rate(income, year) == expected
