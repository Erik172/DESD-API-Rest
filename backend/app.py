from flask import Flask
from flask_restful import Api
import sentry_sdk
import os

from resources import (
    TilDeV1,
    RoDeV1,
    CuDeV1,
    Audit
)

from resources import (
    Works,
    WorkEndPoint as Work
)

sentry_sdk.init(
    dsn="https://e9cca8077d072637f2c5934a3327536c@o4504133595365376.ingest.us.sentry.io/4507189202452480",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

api.add_resource(Works, "/works")
api.add_resource(Work, "/work/<string:work_id>", "/work/<string:work_id>/<string:document_id>")

api.add_resource(TilDeV1, "/tilde/v1")
api.add_resource(RoDeV1, "/rode/v1")
api.add_resource(CuDeV1, "/cude/v1")

api.add_resource(Audit, "/audit")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)