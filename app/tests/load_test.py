from locust import HttpUser, TaskSet, task, between
from dotenv import load_dotenv
from fpdf import FPDF
import random
import string
import os

load_dotenv()

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("/api/v1/auth/login", json={
            "email": os.getenv("ADMIN_EMAIL"),
            "password": os.getenv("ADMIN_PASSWORD")
        })
        self.access_token = response.json().get("access_token")

    def generate_random_text(self, length):
        letters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(letters) for _ in range(length))

    def create_random_pdf(self, file_name: str, lines: int = 1000):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for _ in range(lines):
            random_text = self.generate_random_text(80)
            pdf.cell(200, 10, txt=random_text, ln=True, align='L')

        pdf.output(file_name)

    @task(1)
    def send_random_pdf(self):
        file_name = f"{self.generate_id()}.pdf"
        self.create_random_pdf(file_name)
        with open(file_name, 'rb') as f:
            self.client.post("/api/v1/desd", headers={"Authorization": f"Bearer {self.access_token}"}, files={"files": f}, data={"result_id": "test_result", "models": "inclinacion,rotacion,corte informacion"})
        os.remove(file_name)

    @task(2)
    def get_me(self):
        self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {self.access_token}"})

    @task(3)
    def get_users(self):
        self.client.get("/api/v1/users", headers={"Authorization": f"Bearer {self.access_token}"})

    @task(4)
    def get_models(self):
        self.client.get("/api/v1/models", headers={"Authorization": f"Bearer {self.access_token}"})

    @task(5)
    def get_results(self):
        self.client.get("/api/v1/results", headers={"Authorization": f"Bearer {self.access_token}"})

    def generate_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)