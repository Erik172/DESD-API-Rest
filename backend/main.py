from flask import Flask
from flask_restful import Api

from resources import (
    TilDeV1,
    TilDeV1Remote,
    TilDeV2
)

app = Flask(__name__)
api = Api(app)
            
api.add_resource(TilDeV1, "/tilde/v1")
api.add_resource(TilDeV1Remote, "/tilde/v1/remote")
api.add_resource(TilDeV2, "/tilde/v2")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)