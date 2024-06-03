from flask import Flask, send_file
from flask_restful import Api
import os

from resources import (
    DuDe,
    DESD
)

from resources import (
    Works,
    WorkEndPoint as Work,
    WorkExport
)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'temp')

api.add_resource(Works, "/works", "/works/<string:collection_name>")

api.add_resource(WorkExport, "/work/<string:work_id>/export")
api.add_resource(Work, "/work/<string:work_id>", "/work/<string:work_id>/<string:document_id>")


api.add_resource(DuDe, "/dude/<string:dir_name>")
api.add_resource(DESD, "/desd")

@app.route("/descargar/<file_name>")
def download(file_name):
    route = f'exports/{file_name}.csv'
    return send_file(route, as_attachment=True, mimetype='csv')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)