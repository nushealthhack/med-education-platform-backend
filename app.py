from flask import Flask, render_template, request, send_from_directory
import math
import sys
import os
import base64
import json
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
  filename_list = file.filename.split(".")
  filename_list_without_extension = filename_list[:len(filename_list)-1]
  filename_without_extension = ".".join(filename_list_without_extension)
  # Extract all pages to a folder as image files
  pdf.RasterizeToImageFiles(f"images/{filename_without_extension}/{filename_without_extension}_*.png",DPI=96)

  return 'File uploaded successfully!'

@app.route('/get-folders')
def get_all_folders():
  items = os.listdir('./images')
  path_name = './images'
  folders = [item for item in items if os.path.isdir(os.path.join(path_name, item))]
  print(f'folders {folders}')
  return folders

@app.route('/get-images-folders')
def get_image_folders():
  param_value = request.args.get('folder')
  pathname = './images/' + param_value
  items = os.listdir(pathname)
  res = []
  for item in items:
    with open(pathname + '/' + item, "rb") as img_file:
      my_string = base64.b64encode(img_file.read()).decode("utf-8")
      res.append(my_string)
  return json.dumps({"success": 1, "images": res})


    
if __name__ == '__main__':
    app.run(debug=True)