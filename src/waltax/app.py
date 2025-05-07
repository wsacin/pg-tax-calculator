from flask import Flask
from waltax.blueprints import waltax

app = Flask(__name__)


app.register_blueprint(waltax)


if __name__ == "__main__":
    # whatever other config/setup to be done later
    app.run(host="0.0.0.0")
