import requests
import sys

def create_user(username: str, password: str) -> None:
    url = f"http://localhost:5000/api/v1/user"
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        print("User created successfully.")
    else:
        print(response.status_code)
        print(response.text)
        try:
            error_message = response.json().get("error")
        except requests.exceptions.JSONDecodeError:
            error_message = response.text
        print("Failed to create user.")
        print("Error:", error_message)
        sys.exit(1)

def login(username: str, password: str) -> str:
    url = f"http://localhost:5000/api/v1/auth"
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Login successful.")
        print("Token:", token)
    else:
        print(response.status_code)
        print(response.text)
        sys.exit(1)
    
    return token
    

def predict(task_id, file_paths, token):
    url = f"http://localhost:5000/api/v1/worker"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    files = [('files', (file_path, open(file_path, 'rb'))) for file_path in file_paths]
    models = 'cude,rode,legibility'
    data = {'models': models}
    
    response = requests.post(url, files=files, data=data, headers=headers)
    
    if response.status_code == 202:
        print("Task enqueued successfully.")
        print("Task ID:", response.json().get("task_id"))
    else:
        try:
            error_message = response.json().get("error")
        except requests.exceptions.JSONDecodeError:
            error_message = response.text
        print("Failed to enqueue task.")
        print("Error:", error_message)

if __name__ == '__main__':
    file_paths = [
        'D:\\bomberos\\data\\IMG_BUENAS.pdf',  # Cambia esto a la ruta de tus archivos
    ]
    create_user('erik', 'erik')
    token = login('erik', 'erik')
    # predict(None, file_paths, token)
