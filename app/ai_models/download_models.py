import gdown
import zipfile
import os

def download_customOCR():
    # Download the model
    url_sharing = 'https://drive.google.com/file/d/1PdYn97COqsCGUfj5-tXvfM1c9hESebp6/view?usp=sharing' 
    file_id = url_sharing.split('/')[-2]
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'app/models/customTrOCR.zip'
    
    if not os.path.exists(output):
        print('Downloading model...')
        gdown.download(url, output, quiet=False)
    
    # Unzip the model
    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall('models')
        
if __name__ == '__main__':
    download_customOCR()