import os
import requests
from flask import current_app

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        pdf_path = os.path.join(current_app.root_path, 'data', 'enduro_route.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        return pdf_path
    else:
        raise Exception("Falha ao baixar o PDF")