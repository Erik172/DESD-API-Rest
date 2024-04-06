from flask import Flask
from flask_restful import Api, Resource
from dotenv import load_dotenv

from resources.black_documents import BlackDocumentsDetectorModel

load_dotenv()

app = Flask(__name__)
api = Api(app)
    
class TiltedDocumentsDetectorOCRScript(Resource):
    pass
            
api.add_resource(BlackDocumentsDetectorModel, "/black-documents-detector")

if __name__ == "__main__":
    app.run(debug=True)