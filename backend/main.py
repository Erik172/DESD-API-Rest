from flask import Flask
from flask_restful import Api

from resources import (
    BlackDocumentsDetectorModel,
    TilDeV1,
    TilDeV2
)

app = Flask(__name__)
api = Api(app)
            
api.add_resource(BlackDocumentsDetectorModel, "/black-documents-detector")
api.add_resource(TilDeV1, "/tilde/v1")
api.add_resource(TilDeV2, "/tilde/v2")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)