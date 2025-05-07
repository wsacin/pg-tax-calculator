from flask import Flask
from waltax.blueprints import waltax
from decimal import getcontext

app = Flask(__name__)


app.register_blueprint(waltax)

if __name__ == "__main__":

    getcontext().prec = 2
    app.run("0.0.0.0")
