
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

sql_db = SQLAlchemy()

def get_database():
    """
    Returns the MongoDB database object for the DESD application.

    Returns:
        pymongo.database.Database: The MongoDB database object.
    """
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return client["DESD"]

class WorkStatus(sql_db.Model):
    """
    Represents the work status of a task.

    Attributes:
        id (int): The unique identifier for the work status.
        result_id (str): The unique identifier for the result.
        status (str): The current status of the task.
        files_processed (int): The number of files processed.
        total_files (int): The total number of files to be processed.
        percentage (int): The percentage of completion.
        tilted (bool): Indicates if the task involves tilting.
        rotation (bool): Indicates if the task involves rotation.
        cut_information (bool): Indicates if the task involves cutting information.
        duplicate (bool): Indicates if the task involves duplicate detection.
        start_time (datetime): The timestamp when the task started.
        last_updated (datetime): The timestamp when the task was last updated.
    """
    id = sql_db.Column(sql_db.Integer, primary_key=True, autoincrement=True)
    result_id = sql_db.Column(sql_db.String(100), nullable=False, unique=True)
    status = sql_db.Column(sql_db.String(100), nullable=True, default="in_progress")
    files_processed = sql_db.Column(sql_db.Integer, nullable=True, default=0)
    total_files = sql_db.Column(sql_db.Integer, nullable=True, default=0)
    percentage = sql_db.Column(sql_db.Integer, nullable=True, default=0)
    tilted = sql_db.Column(sql_db.Boolean, nullable=True, default=False)
    rotation = sql_db.Column(sql_db.Boolean, nullable=True, default=False)
    cut_information = sql_db.Column(sql_db.Boolean, nullable=True, default=False)
    duplicate = sql_db.Column(sql_db.Boolean, nullable=True, default=False)
    folio = sql_db.Column(sql_db.Boolean, nullable=True, default=False)
    summary = sql_db.Column(sql_db.Text, nullable=True)
    start_time = sql_db.Column(sql_db.DateTime, nullable=True, default=sql_db.func.now())
    last_updated = sql_db.Column(sql_db.DateTime, nullable=True, default=sql_db.func.now(), onupdate=sql_db.func.now())

    def __repr__(self):
        return f"<WorkStatus {self.result_id}>"
