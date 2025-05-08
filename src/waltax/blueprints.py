from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields
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

    # load/validate arguments
    # TODO:: parse request body and properly raise with status
    body = CalculatePayloadSchema().loads(request.data)
    income, tax_year = body["income"], body["tax_year"]

    try:
        calculated_rates = repository.calculate_rate(income, tax_year)
    except RuntimeError as ex:
        return jsonify({"error": ex.args[0].message}), 409

    # validate calculation
    errors = BracketResponseSchema().validate(calculated_rates)

    if errors:
        # TODO: Treat validation error properly
        return jsonify(errors), 400

    return jsonify(calculated_rates), 200
