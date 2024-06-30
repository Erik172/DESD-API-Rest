from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from database import sql_db

from resources import (
    DuDe,
    DESD,
    DESDStatus,
    Resultados,
    Export,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sql_db.init_app(app)
migrate = Migrate(app, sql_db)
api = Api(app)

with app.app_context():
    sql_db.create_all()

api.add_resource(Resultados, "/v1/resultados", "/v1/resultados/<string:collection_name>", endpoint="resultados")
api.add_resource(Export, "/v2/export/<string:resultado_id>", endpoint="export")

api.add_resource(DuDe, "/v1/dude/<string:dir_name>", endpoint="dude")

api.add_resource(DESD, "/v2/desd", endpoint="desd")
api.add_resource(DESDStatus, "/v2/desd/status", "/v2/desd/status/<string:result_id>", endpoint="desd_status")

@app.route("/v2/generate_id")
def generate_id():
    from src import generate_id
    return {"random_id": generate_id()}, 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)