from flask import request, send_file
from flask_restful import Resource
from werkzeug.utils import secure_filename
import os

class Upload(Resource):
    UPLOAD_FOLDER = 'temp'
    def post(self, folder_name: str = None):
        if folder_name:
            if not os.path.exists(f'temp/{folder_name}'):
                os.makedirs(f'temp/{folder_name}')
            self.UPLOAD_FOLDER = f'temp/{folder_name}'

        if 'file' not in request.files:
            return {"message": "No file part in the request"}, 400
        
        file = request.files['file']

        if file.filename == '':
            return {"message": "No file selected"}, 400
        
        if file and self._allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f'{self.UPLOAD_FOLDER}/{filename}')
            return {
                "message": "File uploaded successfully",
                "filename": filename
            }, 200
        
        return {"message": "Invalid file type"}, 400
        
    def _allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'pdf', 'tif', 'tiff'}

class Download(Resource):
    def get(self, file_name):
        """
        Retrieves a file with the given file_name.

        Args:
            file_name (str): The name of the file to retrieve.

        Returns:
            If the file exists, the file will be returned as an attachment with the mimetype 'csv'.
            If the file does not exist, a JSON response with a "File not found" message and a status code of 404 will be returned.
        """
        route = f'exports/{file_name}.csv'
        if os.path.exists(route):
            return send_file(route, as_attachment=True, mimetype='csv')
        return {"message": "File not found"}, 404