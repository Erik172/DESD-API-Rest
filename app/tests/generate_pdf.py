from fpdf import FPDF
import random
import string

def generate_random_text(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))

def create_random_pdf(file_name: str, lines: str = 1000):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Generar un texto aleatorio
    for _ in range(lines):  # Genera 10 líneas de texto aleatorio
        random_text = generate_random_text(80)  # 80 caracteres por línea
        pdf.cell(200, 10, txt=random_text, ln=True, align='L')

    # Guardar el archivo PDF
    pdf.output(file_name)

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

if __name__ == "__main__":
    create_random_pdf(generate_id() + ".pdf")
