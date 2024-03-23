# flask-image-to-text

This is a simple web application built with Flask for performing Optical Character Recognition (OCR) on uploaded images. It utilizes the OCR.Space API for text recognition and ReportLab for generating PDFs containing the detected text.

## Features

- Upload an image containing text.
- Perform OCR on the uploaded image.
- Display detected text to the user.
- Generate a PDF containing the detected text for download.

## Dependencies

- Flask==2.1.1
- opencv-python==4.5.4.58
- requests==2.26.0
- reportlab==3.6.1

## Usage

1. Start the Flask server:

## Usage

1. Start the Flask server:
2. Open your web browser and go to [http://localhost:5000/]to access the application.
3. Upload an image containing text.
4. Click the "Submit" button to perform OCR.
5. View the detected text on the result page.
6. Optionally, download a PDF containing the detected text.
