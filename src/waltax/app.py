from flask import Flask
from waltax.blueprints import waltax

app = Flask(__name__)


app.register_blueprint(waltax)

if __name__ == "__main__":
    app.run("0.0.0.0")
