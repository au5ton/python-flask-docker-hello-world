from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = '/tmp'
ALLOWED_EXTENSIONS = set([''])

@app.route('/fuckthisproject')
@cross_origin()
def hello():
  return '''
  <form>
  <div>
    <label>Select file to upload</label>
    <input type="file">
  </div>
  <button type="submit">Convert</button>
  </form>
  <img src="" />
  <script>
  async function handleSubmit(event) {
    console.log(event);
    event.preventDefault();
    const file = event.target[0].files[0];
    const formData = new FormData();
    formData.append('file', file);
    console.log(formData);
    await fetch('/dbscan', {
      method: 'POST',
      body: formData
    });
    document.querySelector('img').setAttribute('src','/uploads/'+file.name);
  }
  document.querySelector('form').addEventListener('submit', handleSubmit);
  </script>
  '''

@app.route('/fuckthisproject/uploads/<filename>')
@cross_origin()
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/fuckthisproject/dbscan', methods=['POST'])
@cross_origin()
def upload_file():
  print(request.files)
  if 'file' not in request.files:
    return 'there is no file in form!'
  file = request.files['file']
  path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
  file.save(path)

  img = cv2.imread(path)
  Z = np.float32(img.reshape((-1,3)))
  db = DBSCAN(eps=0.3, min_samples=100).fit(Z[:,:2])
  res2 = np.uint8(db.labels_.reshape(img.shape[:2]))

  cv2.imwrite(path, res2)
  return path

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(debug=True,host='0.0.0.0',port=port)
