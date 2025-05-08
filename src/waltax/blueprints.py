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


@waltax.route("/calculate", methods=["GET"])
def calculate():
    repository = TaxBracketRepository()

    # load/validate arguments
    # TODO:: parse request body and properly raise with status
    body = CalculatePayloadSchema().load(request.json)

    calculated_rates = repository.calculate_rate(body["income"], body["tax_year"])

    # validate calculation
    errors = BracketResponseSchema().validate(calculated_rates)

    if errors:
        # TODO: Treat validation error properly
        return jsonify(errors), 400

    return jsonify(calculated_rates), 200
