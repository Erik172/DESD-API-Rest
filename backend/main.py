from flask import Flask
from flask_restful import Api

from resources import BlackDocumentsDetectorModel

app = Flask(__name__)
api = Api(app)
            
api.add_resource(BlackDocumentsDetectorModel, "/black-documents-detector")

if __name__ == "__main__":
    app.run(debug=True)