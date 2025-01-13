from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from flask import request
from app.models import Result, ResultStatusEnum, ResultStatus
from app import db, queue

class DESDResource(Resource):
    @jwt_required()
    def post(self):
        from app.tasks import process_desd_task  # Mover la importación aquí para evitar la circularidad

        required_fields = ['result_id', 'models']
        missing_fields = [field for field in required_fields if field not in request.form]

        if missing_fields:
            return {"message": f"No {', '.join(missing_fields)} provided"}, 400
        
        if 'files' not in request.files:
            return {"message": "No file part in the request"}, 400

        model_names = request.form.get('models').split(',')
        files = request.files.getlist('files')
        result_id = request.form.get('result_id')
        
        result = Result.query.filter_by(collection_id=result_id).first()
        if result:            
            result_status = ResultStatus.query.filter_by(result_id=result.id).first()
            
            if result_status:
                if result_status.status in [ResultStatusEnum.RUNNING, ResultStatusEnum.PENDING]:
                    return {"message": f"The result has status {result_status.status}"}, 422
                
                if result_status.status == ResultStatusEnum.COMPLETED:
                    result_status.models = ','.join(model_names)
                    result_status.status = ResultStatusEnum.PENDING
                    result_status.created_at = db.func.now()
                    result_status.last_updated_at = db.func.now()
                    db.session.commit()
            else:
                result_status = ResultStatus(
                    result_id=result.id,
                    status=ResultStatusEnum.PENDING,
                    total_files=len(files),
                    total_files_processed=0,
                    models=','.join(model_names),
                    last_updated_at=db.func.now()
                )
                db.session.add(result_status)
                db.session.commit()
        else:
            result = Result(
                collection_id=result_id, 
                user_id=current_user.id,
                created_at=db.func.now(),
                updated_at=db.func.now()
            )
            db.session.add(result)
            db.session.commit()

            result_status = ResultStatus(
                result_id=result.id,
                status=ResultStatusEnum.PENDING,
                total_files=len(files),
                total_files_processed=0,
                models=','.join(model_names),
                last_updated_at=db.func.now()
            )
            db.session.add(result_status)
            db.session.commit()

        # Leer el contenido de los archivos y convertirlos a binario
        file_contents = [(file.filename, file.read()) for file in files]

        # Aumentar el tiempo máximo permitido para la tarea a una semana
        job = queue.enqueue(process_desd_task, result_id, model_names, file_contents, job_timeout=604800)
        return {"message": "Processing started", "job_id": job.get_id()}, 202