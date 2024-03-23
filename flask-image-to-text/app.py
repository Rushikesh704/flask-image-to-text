from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import requests
import io
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and perform OCR."""
    # Retrieve the uploaded file
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    # Read the uploaded image using OpenCV
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    height, width, _ = img.shape

    # Perform OCR on the image
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    # Send image data to OCR.Space API for text recognition
    result = requests.post(url_api,
                           files={filename: file_bytes},
                           data={"apikey": "helloworld",
                                 "language": "eng"}) 
    if result.status_code == 200:
        # Parse JSON response to extract detected text
        result_json = result.json()
        parsed_results = result_json.get("ParsedResults")
        if parsed_results:
            text_detected = parsed_results[0].get("ParsedText")
            return render_template('result.html', text_detected=text_detected)
        else:
            error_message = "Image Size Should Be Less Than 1 Mb."
    else:
        error_message = f"Error {result.status_code} occurred during OCR."

    # Render error template if OCR fails
    return render_template('error.html', error_message=error_message)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    """Generate and download a PDF containing the detected text."""
    text_detected = request.form['text_detected']
    filename = "ocr_result.pdf"

    # Generate PDF using ReportLab
    pdf = canvas.Canvas(filename, pagesize=letter)
    pdf.drawString(100, 750, text_detected)
    pdf.save()

    # Send generated PDF as a file download
    return send_file(filename, as_attachment=True, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
