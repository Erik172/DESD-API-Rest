from PIL import Image
import pytesseract
import hashlib
import time
import re
import os
from typing import Dict, List, Optional
from services import DatabaseService

class SearchService:
    def __init__(self, data_dir: str, task_id: str):
        self.hash_map: Dict[str, str] = {}
        self.duplicates: Dict[str, List[str]] = {}
        self.data_dir = data_dir
        self.result_id = task_id
        self.list_of_files = os.listdir(data_dir)
        self.database_service = DatabaseService()

    def _get_hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    def _ocr_core(self, filename: str) -> str:
        try:
            text = pytesseract.image_to_string(Image.open(filename))
            return text
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            return ""

    def find_duplicates(self) -> None:
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

        
        total_files = self.database_service.get_result_status(self.result_id)['total_files']
        self.database_service.update_result_status(self.result_id, total_files_processed=total_files, status='COMPLETED')

    def get_duplicates(self) -> Dict[str, List[str]]:
        return self.duplicates

    def get_hash_map(self) -> Dict[str, str]:
        return self.hash_map

    def generate_report(self) -> List[Dict[str, Optional[str]]]:
        report = []
        for key, duplicates in self.duplicates.items():
            num_of_duplicates = len(duplicates)
            page_number = self._extract_page_number(key)
            filename = self._clean_filename(key, page_number)

            document = {
                "archivo": filename,
                "duplicados": num_of_duplicates,
                "pagina": page_number
            }

            for i, duplicate in enumerate(duplicates):
                duplicate_page_number = self._extract_page_number(duplicate)
                duplicate_filename = self._clean_filename(duplicate, duplicate_page_number)
                document[f"duplicado[{i + 1}]"] = duplicate_filename
                document[f"duplicado[{i + 1}]_pagina"] = duplicate_page_number

            report.append(document)

        return report

    def _clean_filename(self, filename: str, page_number: Optional[int]) -> str:
        if page_number is not None:
            return filename.replace(f'__pagina_{page_number}.png', '').replace(f'__pagina_{page_number}.jpg', '')
        return filename

    def _extract_page_number(self, filename: str) -> Optional[int]:
        match = re.search(r'__pagina_(\d+)', filename)
        return int(match.group(1)) if match else None

    def execute(self) -> List[Dict[str, Optional[str]]]:
        self.find_duplicates()
        return self.generate_report()