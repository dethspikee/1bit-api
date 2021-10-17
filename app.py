from bottle import run, post, request

from io import BytesIO
from PIL import UnidentifiedImageError
import base64
import os

from utils import create_response
from converter import convert, resize


@post('/convert')
def handle_conversion():
    threshold = request.params.get('threshold')

    try:
        image = request.files['file']
        b64_image = base64.b64encode(image.file.read())
        bytelist = convert(b64_image, threshold)
    except UnidentifiedImageError:
        return create_response({'error': 'Error processing file contents. Make\
            sure you\'re sending valid image'}, 422, 'application/json')
    except KeyError:
        return create_response({'error': 'missing file'}, 422, 'application/json')

    return {'payload': bytelist}


@post('/encode64')
def encode_base64():
    try:
        image = request.files['file']
        b64_image = base64.b64encode(image.file.read()).decode('ascii')
    except KeyError:
        return create_response({'error': 'missing file'}, 422, 'application/json')

    return {'payload': b64_image}


@post('/resize')
def resize_image():
    width = request.params.get('width')
    height = request.params.get('height')

    try:
        image = request.files['file']
        b64_image = resize(image.file, (int(width), int(height)))
    except KeyError:
        return create_response('missing file', 422, 'application/json')

    return create_response(b64_image, 200, 'application/octet-stream')


if os.environ.get('PROD'):
    run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get('PORT')))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)
