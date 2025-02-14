from app import db
from app.models import ResultStatus

def update_result_status(id: int, **kwargs):
    """
    Actualiza el estado de un resultado en la base de datos.

    Parámetros:
    id (int): El ID del estado del resultado a actualizar.
    **kwargs: Argumentos clave-valor que representan los campos y sus nuevos valores.

    Retorna:
    ResultStatus: El objeto ResultStatus actualizado si se encuentra, de lo contrario, None.
    """
    result_status = ResultStatus.query.get(id)
    if result_status:
        for key, value in kwargs.items():
            setattr(result_status, key, value)
        db.session.commit()
        return result_status
    return None