from flask import Flask, send_file
from flask_restful import Api
import sentry_sdk
import os

from resources import (
    TilDe,
    RoDe,
    CuDe,
    DuDe,
    Audit
)

from resources import (
    Works,
    WorkEndPoint as Work,
    WorkExport
)

sentry_sdk.init(
    dsn="https://e9cca8077d072637f2c5934a3327536c@o4504133595365376.ingest.us.sentry.io/4507189202452480",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

api.add_resource(Works, "/works", "/works/<string:collection_name>")

api.add_resource(WorkExport, "/work/<string:work_id>/export")
api.add_resource(Work, "/work/<string:work_id>", "/work/<string:work_id>/<string:document_id>")

api.add_resource(TilDe, "/tilde")
api.add_resource(RoDe, "/rode")
api.add_resource(CuDe, "/cude")
api.add_resource(DuDe, "/dude/<string:dir_name>")

api.add_resource(Audit, "/audit")

@app.route("/descargar/<file_name>")
def download(file_name):
    route = f'exports/{file_name}.csv'
    return send_file(route, as_attachment=True, mimetype='csv')

if __name__ == "__main__":
    app.run(debug=F, host="0.0.0.0", port=5000)