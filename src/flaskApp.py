from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Welcome to the Image Conversion App</h1>
    <p>Use the following routes:</p>
    <ul>
        <li><b>/convert</b> (POST) - Convert an image to another format. Available formats: PNG, JPEG, BMP, GIF.</li>
        <li><b>/fetch</b> (GET) - Fetch data from a public API and display it.</li>
    </ul>
    '''


@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files or 'output_format' not in request.form:
        return jsonify({'error': 'Image file and output format are required'}), 400

    image_file = request.files['image']
    output_format = request.form['output_format'].upper()

    if output_format not in ['PNG', 'JPEG', 'BMP', 'GIF']:
        return jsonify({'error': 'Unsupported output format'}), 400

    image = Image.open(image_file)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=output_format)
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype=f'image/{output_format.lower()}', as_attachment=True,
                     download_name=f'converted_image.{output_format.lower()}')


@app.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from the provided URL'}), 400

    return {"response_text": response.text}


if __name__ == '__main__':
    app.run(debug=True)
