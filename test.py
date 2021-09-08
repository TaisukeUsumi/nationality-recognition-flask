import os

from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

from .prediction import Prediction

save_path = './static'
app = Flask(__name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        image_file = request.files["image_file"]
        image_path = os.path.join(save_path, secure_filename(image_file.filename))
        image_file.save(image_path)
        result, probability_list = Prediction.predict(image_path)
        return render_template('show_result.html', 
                                result=result,
                                chinese_probability=probability_list[0],
                                japanese_probability=probability_list[1],
                                korean_probability=probability_list[2])
    else:
        return render_template('upload.html')
