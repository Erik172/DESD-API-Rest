from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path, convert_from_bytes
from database import WorkStatus, sql_db
from ultralytics import YOLO
from PIL import Image
import pandas as pd
import pytesseract
import requests
import json
import os

class FolioDetector:
    def __init__(self):
        self.model_yolo = YOLO('models/folio-detectV1.pt')
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
        # self.trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")
        self.trocr_model = VisionEncoderDecoderModel.from_pretrained("models/customTrOCR/")
        self.report = pd.DataFrame(columns=['pagina', 'folio', 'reverso'])
        self.page = 1
        self.text1 = None
        self.text2 = None
        self.filename = None

    def detect_folio(self, pdf_file: str | bytes, result_id: str):
        work_status = WorkStatus.query.filter_by(result_id=result_id).first()
        self.filename = pdf_file.split('/')[-1]

        if isinstance(pdf_file, str):
            pages = convert_from_path(pdf_file, thread_count=os.cpu_count())
        else:
            pages = convert_from_bytes(pdf_file, thread_count=os.cpu_count())
        if len(pages) != work_status.total_files:
            work_status.total_files = len(pages)
            sql_db.session.commit()

        for i, page in enumerate(pages):
            is_reverse = None
            work_status.files_processed += 1
            work_status.percentage = work_status.files_processed / work_status.total_files * 100
            sql_db.session.commit()

            folio_box = self._yolo_detect(page)
            if folio_box is None:
                folio_text = None
            else:
                folio_image = self._crop_folio(page, folio_box)
                folio_text = self._ocr_folio(folio_image)

            if folio_text is None and self.page < i:
                self.text2 = pytesseract.image_to_string(page)
                is_reverse = self._is_reverse(self.text1, self.text2)

            self.text1 = pytesseract.image_to_string(page)
            
            self.page += 1
            self.report = pd.concat([self.report, pd.DataFrame({'pagina': [i + 1], 'folio': [folio_text], 'reverso': [is_reverse]})], ignore_index=True)

        self.report['archivo'] = self.filename
        self.save_report('report.csv')

    def _yolo_detect(self, image: Image.Image) -> dict | None:
        result = self.model_yolo(image)[0].tojson()
        result = json.loads(result)

        if len(result) == 0:
            return None
        else:
            return result[0]
        
    def _crop_folio(self, image: Image.Image, folio_box: dict) -> Image.Image:
        folio_box = folio_box['box']
        image = image.crop((folio_box['x1'], folio_box['y1'], folio_box['x2'], folio_box['y2']))
        # image.save(f'images/2/373-41786_{self.page}.jpg')
        return image
    
    def _ocr_folio(self, folio_image: Image.Image) -> int | None:
        pixel_values = self.processor(images=folio_image, return_tensors="pt").pixel_values
        generated_ids = self.trocr_model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        generated_text = generated_text.replace('.', '')
        try:
            folio_text = int(generated_text)
        except ValueError:
            print(generated_text)
            return None
        
        return folio_text

    def _is_reverse(self, text1: str, text2: str, model: str = 'llama3') -> str:
        prompt = f"""
            Respondeme con un Si o con un No si el texto2 es el reverso del texto1 o continuacion del texto1.
            Texto1: {text1}

            Texto2: {text2}
        """

        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post("http://localhost:11434/api/generate", json=data)

        return response.json()['response']
    
    def get_report(self):
        return self.report.to_dict(orient='records')
    
    def save_report(self, output_file: str):
        self.report.to_csv(output_file, index=False)