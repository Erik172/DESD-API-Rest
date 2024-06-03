from flask import Flask
from flask_restful import Api
import os

from resources import DESD, DuDe

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

api.add_resource(DuDe, "/dude/<string:dir_name>")
api.add_resource(DESD, "/desd")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)