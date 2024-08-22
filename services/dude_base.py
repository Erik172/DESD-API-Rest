from database import WorkStatus, sql_db
from PIL import Image
import pytesseract
import hashlib
import re
import os

class DuDeBase:
    def __init__(self, data_dir: str):
        self.hash_map = {}
        self.duplicates = {}
        self.data_dir = data_dir
        self.result_id = data_dir.split('/')[-1]
        self.list_of_files = os.listdir(data_dir)
        self.work_status = WorkStatus.query.filter_by(result_id=self.result_id).first()

    def _get_hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    def _ocr_core(self, filename: str) -> str:
        text = pytesseract.image_to_string(Image.open(filename))
        return text
    
    def find_duplicates(self) -> None:
        if len(self.list_of_files) != self.work_status.total_files:
            self.work_status.total_files = len(self.list_of_files)
            sql_db.session.commit()

        for file in self.list_of_files:
            file_path = os.path.join(self.data_dir, file)
            text = self._ocr_core(file_path)

            if not text:
                self.duplicates.setdefault("texto_no_identificado", []).append(file)
                continue

            text_hash = self._get_hash(text)

            if text_hash in self.hash_map:
                self.duplicates.setdefault(self.hash_map[text_hash], []).append(file)
            else:
                self.hash_map[text_hash] = file

            self._update_work_status(self.work_status)

    def get_duplicates(self) -> dict:
        return self.duplicates

    def get_hash_map(self) -> dict:
        return self.hash_map
    
    def generate_report(self) -> list:
        report = []
        for key, value in self.get_duplicates().items():
            num_of_duplicates = len(value)
            page_number = self._extract_page_number(key)
            if page_number is not None:
                filename = key.replace(f'__pagina_{page_number}.png', '').replace(f'__pagina_{page_number}.jpg', '')
            else:
                filename = key

            document = {
                "archivo": filename,
                "duplicados": num_of_duplicates
            }

            if page_number is not None:
                document["pagina"] = page_number
            else:
                document["pagina"] = None

            for i, duplicate in enumerate(value):
                pege_number = self._extract_page_number(duplicate)
                if page_number is not None:
                    filename = duplicate.replace(f'__pagina_{pege_number}.png', '').replace(f'__pagina_{pege_number}.jpg', '')
                    document[f"duplicado[{i + 1}]"] = filename
                    document[f"duplicado[{i + 1}]_pagina"] = pege_number
                else:
                    document[f"duplicado[{i + 1}]"] = duplicate

            report.append(document)

        return report

    def _extract_page_number(self, filename: str) -> int:
        match = re.search(r'__pagina_(\d+)', filename)
        return int(match.group(1)) if match else None
    
    def _update_work_status(self, work_status):
        work_status.files_processed += 1
        work_status.percentage = (work_status.files_processed / work_status.total_files) * 100
        sql_db.session.commit()

