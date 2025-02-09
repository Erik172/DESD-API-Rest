from pymongo import MongoClient
from config import Config
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class DatabaseService:
    def __init__(self):
        # Conectar a MongoDB
        self.mongo_client = MongoClient(Config.MONGO_URI)
        self.db = self.mongo_client.results
        self.results_collection = self.db.results
        
        # Conectar a PostgreSQL con SQLAlchemy
        self.engine = create_engine(Config.POSTGRES_URI)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine) # Reflejar las tablas existentes
        self.results_table = self.metadata.tables['result']
        self.result_status_table = self.metadata.tables['result_status']
        
        # Crear una sesión de SQLAlchemy
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def update_result_status(self, result_id: int, **kwargs):
        result = self.session.query(self.results_table).filter_by(collection_id=result_id).first()
        self.session.query(self.result_status_table).filter_by(result_id=result.id).update(kwargs)
        self.session.commit()
        
    def get_result_status(self, result_id: int):
        result = self.session.query(self.results_table).filter_by(collection_id=result_id).first()
        result_status = self.session.query(self.result_status_table).filter_by(result_id=result.id).first()
        return {
            'total_files': result_status.total_files,
            'total_files_processed': result_status.total_files_processed,
            'status': result_status.status
        }
    
    def close(self):
        self.mongo_client.close()
        self.session.close()
        
    def __del__(self):
        self.close()