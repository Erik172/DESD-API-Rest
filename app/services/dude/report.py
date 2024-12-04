from .base import DuDeBase

class DuDeReport(DuDeBase):
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