import re

class DuDeUtils:
    @staticmethod
    def _extract_page_number(filename: str) -> int:
        match = re.search(r'__pagina_(\d+)', filename)
        return int(match.group(1)) if match else None