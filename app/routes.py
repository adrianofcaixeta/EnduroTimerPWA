from flask import render_template, jsonify, send_file
from app import app
from app.pdf_downloader import download_pdf
import os

PDF_URL = "https://exemplo.com/enduro_route.pdf"  # Substitua pela URL real

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-pdf')
def download_route_pdf():
    try:
        pdf_path = download_pdf(PDF_URL)
        return jsonify({'success': True, 'path': '/view-pdf'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/view-pdf')
def view_pdf():
    pdf_path = os.path.join(app.root_path, 'data', 'enduro_route.pdf')
    return send_file(pdf_path, mimetype='application/pdf')

@app.route('/check-pdf')
def check_pdf():
    pdf_path = os.path.join(app.root_path, 'data', 'enduro_route.pdf')
    if os.path.exists(pdf_path):
        return jsonify({'exists': True, 'path': '/view-pdf'})
    else:
        return jsonify({'exists': False})