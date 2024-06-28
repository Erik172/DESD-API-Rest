from flask import Flask, send_file
from flask_restful import Api
from flask_migrate import Migrate
from database import sql_db
import os

from resources import (
    DuDe,
    DESD,
    DESDStatus,
    Resultados,
    Export,
)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sql_db.init_app(app)
migrate = Migrate(app, sql_db)
api = Api(app)

with app.app_context():
    sql_db.create_all()

api.add_resource(Resultados, "/v1/resultados", "/v1/resultados/<string:collection_name>")
api.add_resource(Export, "/v1/export/<string:resultado_id>")

api.add_resource(DuDe, "/v1/dude/<string:dir_name>")
api.add_resource(DESD, "/v1/desd")
api.add_resource(DESDStatus, "/v1/desd/status/<string:result_id>")

@app.route("/v1/generate_id")
def generate_id():
    """
    Generates a random ID.

    Returns:
        A dictionary containing the generated random ID.
    """
    from src import generate_id
    return {"random_id": generate_id()}, 200

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