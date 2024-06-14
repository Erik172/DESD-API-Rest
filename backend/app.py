from flask import Flask, send_file
from flask_restful import Api
import os

from resources import (
    DuDe,
    DESD,
    Resultados,
    Export,
)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

api.add_resource(Resultados, "/v1/resultados", "/v1/resultados/<string:collection_name>")
api.add_resource(Export, "/v1/export/<string:resultado_id>")

api.add_resource(DuDe, "/v1/dude/<string:dir_name>")
api.add_resource(DESD, "/v1/desd")

@app.route("/descargar/<file_name>")
def download(file_name: str):
    """
    Download a file with the given file name.

    Args:
        file_name (str): The name of the file to be downloaded.

    Returns:
        If the file exists, the file will be downloaded as an attachment with the mimetype 'csv'.
        If the file does not exist, a 404 error message will be returned.
    """
    route = os.path.join(basedir, 'exports', f'{file_name}.csv')
    if os.path.exists(route):
        return send_file(route, as_attachment=True, mimetype='csv')
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)