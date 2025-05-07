from flask import jsonify
from waltax.blueprints import waltax


@waltax.route("/calculate", methods=["GET"])
def calculate(income, tax_year):
    return jsonify({"income": income, "tax_year": tax_year})
