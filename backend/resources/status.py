from database import WorkStatus, sql_db
from flask_restful import Resource

class Status(Resource):
    def get(self, result_id: str = None):
        if result_id:
            work_status = self._get_work_status(result_id)
            if not work_status:
                return {"message": "Result not found"}, 404
            
            return self._serialize_work_status(work_status), 200
        else:
            work_statuses = WorkStatus.query.all()
            return [self._serialize_work_status(work_status) for work_status in work_statuses], 200
    
    def delete(self, result_id: str):
        work_status = self._get_work_status(result_id)
        if not work_status:
            return {"message": "Result not found"}, 404

        sql_db.session.delete(work_status)
        sql_db.session.commit()

        return {"message": "Result deleted successfully"}, 200

    def _get_work_status(self, result_id: str):
        return WorkStatus.query.filter_by(result_id=result_id).first()

    def _serialize_work_status(self, work_status):
        return {
            "result_id": work_status.result_id,
            "status": work_status.status,
            "files_processed": work_status.files_processed,
            "total_files": work_status.total_files,
            "percentage": work_status.percentage,
            "tilted": work_status.tilted,
            "rotation": work_status.rotation,
            "cut_information": work_status.cut_information,
            "duplicate": work_status.duplicate,
            "folio": work_status.folio,
            "start_time": work_status.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": work_status.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }