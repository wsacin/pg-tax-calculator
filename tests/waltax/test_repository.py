import pytest
from tests.conftest import FakeTaxApi
from waltax.repository import TaxBracketRepository
from decimal import Decimal


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

    def test_get_rates(self):
        """
        Test that the rates are correctly parsed to Decimal.
        """
        pass

    @pytest.mark.parametrize(
        "income, year, expected",
        [
            (
                Decimal("0.00"),
                2022,
                {
                    "total_taxes_owed": Decimal("0.00"),
                    "effective_rate": Decimal("0.00"),
                },
            ),
            (
                Decimal("50000.00"),
                2022,
                {
                    "total_taxes_owed": Decimal("7500.00"),
                    "effective_rate": Decimal("0.15"),
                    "taxes_owed_per_bracket": {
                        "0.15": {
                            "min": Decimal("0.00"),
                            "max": Decimal("50197.00"),
                            "owed": Decimal("7500.00"),
                        },
                    },
                },
            ),
            (
                Decimal("100000.00"),
                2022,
                {
                    "total_taxes_owed": Decimal("17739.17"),
                    "effective_rate": Decimal("0.18"),
                    "taxes_owed_per_bracket": {
                        "0.15": {
                            "min": Decimal("0.00"),
                            "max": Decimal("50197.00"),
                            "owed": Decimal("7529.55"),
                        },
                        "0.205": {
                            "min": Decimal("50197.00"),
                            "max": Decimal("100392.00"),
                            "owed": Decimal("10209.62"),
                        },
                    },
                },
            ),
            (
                Decimal("1234567.00"),
                2022,
                {
                    "total_taxes_owed": Decimal("385587.65"),
                    "effective_rate": Decimal("0.32"),
                    "taxes_owed_per_bracket": {
                        "0.15": {
                            "min": Decimal("0.00"),
                            "max": Decimal("50197.00"),
                            "owed": Decimal("7529.55"),
                        },
                        "0.205": {
                            "min": Decimal("50197.00"),
                            "max": Decimal("100392.00"),
                            "owed": Decimal("10289.98"),
                        },
                        "0.26": {
                            "min": Decimal("100392.00"),
                            "max": Decimal("155625.00"),
                            "owed": Decimal("14360.58"),
                        },
                        "0.29": {
                            "min": Decimal("155625.00"),
                            "max": Decimal("221708.00"),
                            "owed": Decimal("19164.07"),
                        },
                        "0.33": {
                            "min": Decimal("221708.00"),
                            "owed": Decimal("334243.47"),
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

        if not "taxes_owed_per_bracket" in expected:
            assert payload == expected
        else:
            owed_per_bracket = payload["taxes_owed_per_bracket"]
            for rate, bracket in expected["taxes_owed_per_bracket"].items():
                assert bracket["min"] == owed_per_bracket[rate]["min"]
                assert bracket["owed"] == owed_per_bracket[rate]["owed"]

                if not "max" in bracket:
                    assert "max" not in owed_per_bracket
