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
BASEURL = os.environ['BASEURL'] if 'BASEURL' in os.environ else '/fuckthisproject'

@app.route(f'{BASEURL}/')
@cross_origin()
def hello():
  return f'''
  <form>
  <div>
    <label>Select file to upload</label>
    <input type="file">
  </div>
  <button type="submit">Convert</button>
  </form>
  <img src="" />
  <script>
  async function handleSubmit(event) {{
    console.log(event);
    event.preventDefault();
    const file = event.target[0].files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('eps', 0.4);
    formData.append('min_samples', 120);
    console.log(formData);
    await fetch('{BASEURL}/dbscan', {{
      method: 'POST',
      body: formData
    }});
    document.querySelector('img').setAttribute('src','{BASEURL}/uploads/'+file.name);
  }}
  document.querySelector('form').addEventListener('submit', handleSubmit);
  </script>
  '''

@app.route(f'{BASEURL}/uploads/<filename>')
@cross_origin()
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route(f'{BASEURL}/dbscan', methods=['POST'])
@cross_origin()
def upload_file():
  print(request.files)
  GIVEN_EPS = 0.3
  GIVEN_MIN_SAMPLES = 100
  if 'eps' in request.form:
    GIVEN_EPS = float(request.form['eps'])
    print(f'GIVEN_EPS = {GIVEN_EPS}')
  if 'min_samples' in request.form:
    GIVEN_MIN_SAMPLES = int(request.form['min_samples'])
    print(f'GIVEN_MIN_SAMPLES = {GIVEN_MIN_SAMPLES}')
  if 'file' not in request.files:
    return 'there is no file in form!'
  file = request.files['file']
  path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
  file.save(path)

  img = cv2.imread(path)
  Z = np.float32(img.reshape((-1,3)))
  db = DBSCAN(eps=GIVEN_EPS, min_samples=GIVEN_MIN_SAMPLES).fit(Z[:,:2])
  res2 = np.uint8(db.labels_.reshape(img.shape[:2]))

  cv2.imwrite(path, res2)
  return path

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(debug=True,host='0.0.0.0',port=port)
