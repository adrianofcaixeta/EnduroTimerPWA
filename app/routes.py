from flask import render_template, jsonify, send_file, current_app
from app import app
import os
from datetime import datetime, timezone

# Configurações do PDF
PDF_FILENAME = 'enduro20250223.pdf'

# Configuração da data de liberação
USE_TEST_DATE = True  # Mude para False em produção
PDF_RELEASE_DATE = datetime(2023, 1, 1, tzinfo=timezone.utc) if USE_TEST_DATE else datetime(2025, 2, 23, tzinfo=timezone.utc)

def get_pdf_path():
    return os.path.join(app.root_path, 'static', 'pdfs', PDF_FILENAME)

def is_pdf_available():
    return datetime.now(timezone.utc) >= PDF_RELEASE_DATE or USE_TEST_DATE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-pdf')
def check_pdf():
    pdf_path = get_pdf_path()
    exists = os.path.exists(pdf_path)
    is_released = is_pdf_available()
    return jsonify({
        'exists': exists,
        'is_released': is_released,
    })

@app.route('/serve-pdf')
def serve_pdf():
    if not is_pdf_available():
        return jsonify({'error': 'PDF not available yet'}), 403
    pdf_path = get_pdf_path()
    if os.path.exists(pdf_path):
        return send_file(pdf_path, mimetype='application/pdf')
    return jsonify({'error': 'PDF file not found'}), 404

@app.route('/download-pdf')
def download_pdf():
    if not is_pdf_available():
        return jsonify({'success': False, 'error': 'PDF not available yet'}), 403
    pdf_path = get_pdf_path()
    if os.path.exists(pdf_path):
        return jsonify({'success': True, 'path': '/serve-pdf'})
    return jsonify({'success': False, 'error': 'PDF file not found'}), 404