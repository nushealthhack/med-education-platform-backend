from flask import Flask, render_template, request
import math
import sys
import os
sys.prefix = 'C:/Users/randa/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages'
from ironpdf import *

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/upload-pdf', methods=["POST"])
def generate_document():
  if 'file' not in request.files:
    return 'No file part'

  file = request.files['file']
  print(file)
  if file.filename == '':
      return 'No selected file'

  # Handle the file, for example, save it to a folder
  file.save('uploads/' + file.filename)
  pdf = PdfDocument.FromFile("./uploads/" + file.filename)
  # Extract all pages to a folder as image files
  pdf.RasterizeToImageFiles(f"images/{file.filename}/{file.filename}*.png",DPI=96)

  return 'File uploaded successfully!'

@app.route('./get-folders')
def get_all_folders():
  items = os.listdir('./images')
  folders = [item for item in items if os.path.isdir(os.path.join(path, item))]
  return folders

    
if __name__ == '__main__':
    app.run(debug=True)