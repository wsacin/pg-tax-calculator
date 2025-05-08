from decimal import Decimal, ROUND_UP


def quantized_decimal(value):
    """
    This is a way to format using 2 decimal places. Ideally
    we will bake something alike into a dataclass for brackets.
    """
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(Decimal("0.01"), rounding=ROUND_UP)
