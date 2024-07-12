from database import WorkStatus, sql_db
from flask_restful import Resource
from services import FolioDetector
from flask import request, jsonify
from database import get_database
import os

class Folio(Resource):
    db = get_database()
    
    def post(self):
        required_fields = ['result_id', 'files']
        for field in required_fields:
            if field not in request.form and field != 'files':
                return {"message": f"No {field} provided"}, 400
            elif field == 'files' and not request.files:
                return {"message": "No files provided"}, 400

        result_id = request.form['result_id']  
        files = request.files.getlist('files')

        work_status = WorkStatus(
            result_id=result_id, 
            status='in_progress',
            total_files=len(files),
            files_processed=0,
            percentage=0,
            folio=True,
        )
        sql_db.session.add(work_status)
        sql_db.session.commit()

        for file in files:
            file.save('temp/' + file.filename)
            folio_detector = FolioDetector()
            folio_detector.detect_folio('temp/' + file.filename, result_id)
            os.remove('temp/' + file.filename)

            work_status.total_files = len(files)
            work_status.files_processed += 1
            work_status.percentage = work_status.files_processed / work_status.total_files * 100
            sql_db.session.commit()

            try:
                collection = self.db[result_id]
                collection.insert_many(folio_detector.get_report())
            except Exception as e:
                work_status.status = 'failed'
                sql_db.session.commit()
                return {"message": "Failed to save results"}, 500
        
        work_status.total_files = len(files)
        work_status.status = 'completed'
        sql_db.session.commit()
            
        return {"message": "Processing completed successfully"}, 200