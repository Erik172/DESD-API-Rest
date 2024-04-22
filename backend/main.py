from flask import Flask
from flask_restful import Api

from resources import (
    TilDeV1,
    RoDeV1,
    Audit
)

app = Flask(__name__)
api = Api(app)
            
api.add_resource(TilDeV1, "/tilde/v1")

api.add_resource(RoDeV1, "/rode/v1")

api.add_resource(Audit, "/audit")

if __name__ == "__main__":
    app.run(debug=Fa, host="0.0.0.0", port=5000)