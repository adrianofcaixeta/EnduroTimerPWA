from flask import render_template, jsonify, send_from_directory, current_app, url_for
from app import app
import os
from datetime import datetime, timezone

# Configurações do PDF
PDF_FILENAME = 'enduro20250223.pdf'
PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'static', 'pdfs')
PDF_PATH = os.path.join(PDF_DIR, PDF_FILENAME)

# Configuração da data de liberação
USE_TEST_DATE = True  # Mude para False em produção

if USE_TEST_DATE:
    PDF_RELEASE_DATE = datetime(2023, 1, 1, tzinfo=timezone.utc)  # Data passada para testes
else:
    PDF_RELEASE_DATE = datetime(2025, 2, 23, tzinfo=timezone.utc)  # Data real de liberação

def is_pdf_available():
    return datetime.now(timezone.utc) >= PDF_RELEASE_DATE or USE_TEST_DATE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-pdf')
def download_route_pdf():
    if not is_pdf_available():
        return jsonify({'success': False, 'error': 'PDF not available yet'}), 403

    app.logger.info(f"Tentando acessar o PDF em: {PDF_PATH}")
    
    if os.path.exists(PDF_PATH):
        app.logger.info("PDF encontrado.")
        pdf_url = url_for('static', filename=f'pdfs/{PDF_FILENAME}')
        return jsonify({'success': True, 'path': pdf_url})
    else:
        app.logger.error(f"PDF não encontrado em {PDF_PATH}")
        return jsonify({'success': False, 'error': 'PDF file not found'}), 404

@app.route('/view-pdf')
def view_pdf():
    if not is_pdf_available():
        return jsonify({'error': 'PDF not available yet'}), 403

    app.logger.info(f"Tentando servir o PDF de: {PDF_PATH}")
    
    if os.path.exists(PDF_PATH):
        app.logger.info("PDF encontrado. Tentando servir.")
        pdf_url = url_for('static', filename=f'pdfs/{PDF_FILENAME}')
        return render_template('view_pdf.html', pdf_url=pdf_url)
    else:
        app.logger.error(f"PDF não encontrado em {PDF_PATH}")
        return jsonify({'error': 'PDF file not found'}), 404

@app.route('/check-pdf')
def check_pdf():
    now = datetime.now(timezone.utc)
    is_released = is_pdf_available()
    
    exists = os.path.exists(PDF_PATH)
    app.logger.info(f"Verificação do PDF: Existe: {exists}, Caminho: {PDF_PATH}, Liberado: {is_released}")
    
    return jsonify({
        'exists': exists,
        'is_released': is_released,
        'path': f'/static/pdfs/{PDF_FILENAME}' if is_released and exists else None,
        'release_date': PDF_RELEASE_DATE.isoformat(),
        'current_time': now.isoformat(),
        'test_mode': USE_TEST_DATE,
        'pdf_path': PDF_PATH
    })

@app.route('/debug-info')
def debug_info():
    return jsonify({
        'current_app.root_path': current_app.root_path,
        'PDF_DIR': PDF_DIR,
        'PDF_PATH': PDF_PATH,
        'PDF_exists': os.path.exists(PDF_PATH),
        'static_folder': app.static_folder,
        'static_url_path': app.static_url_path,
        'file_list': os.listdir(os.path.dirname(PDF_DIR))
    })