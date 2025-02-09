from app import db
from app.models import ResultStatus

def update_result_status(id: int, **kwargs):
    result_status = ResultStatus.query.get(id)
    if result_status:
        for key, value in kwargs.items():
            setattr(result_status, key, value)
        db.session.commit()
        return result_status
    return None