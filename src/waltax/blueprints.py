from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from waltax.repository import TaxBracketRepository


waltax = Blueprint("waltax", __name__, url_prefix="/waltax")


class CalculatePayloadSchema(Schema):
    income = fields.Integer()
    tax_year = fields.Int()


class TaxesOwedBreakdown(Schema):
    min = fields.Decimal()
    max = fields.Decimal()
    owed = fields.Decimal()


class BracketResponseSchema(Schema):
    total_taxes_owed = fields.Decimal()
    effective_rate = fields.Decimal()
    taxes_owed_per_bracket = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(TaxesOwedBreakdown),
    )


@waltax.route("/calculate_payable_taxes", methods=["GET"])
def calculate_payable_taxes():
    repository = TaxBracketRepository()

    # TODO::
    #   1.  parse request body and properly raise with status
    #   2.  move errors to an error_handler collection at
    #       the app creation level.
    #   3.  This is a GET with a body. We might either want to
    #       change the request method or move the arguments. It
    #       does look cleaner this way.
    #   4.  Improve decimal precision. Do we need float/double
    #       in the response?

    try:
        body = CalculatePayloadSchema().loads(request.data)
    except ValidationError as ex:
        return jsonify({"message": ex.args[0]}), 400

    income = body["income"]
    tax_year = body["tax_year"]

    try:
        calculated_rates = repository.calculate_rate(income, tax_year)
    except ValueError as ex:
        return jsonify({"message": ex.args[0]}), 409

    # validate calculation
    errors = BracketResponseSchema().validate(calculated_rates)

    if errors:
        # TODO: Treat validation error properly
        return jsonify(errors), 400

    return jsonify(calculated_rates), 200
