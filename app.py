from bottle import run, post, request, abort

from io import BytesIO
from PIL import UnidentifiedImageError
import base64
import os

from utils import create_response
from converter import convert


@post('/convert')
def handle_conversion():
    threshold = request.params.get('threshold')

    try:
        image = request.files['file']
        b64_image = base64.b64encode(image.file.read())
        bytelist = convert(b64_image, threshold)
    except UnidentifiedImageError:
        return create_response('Error processing file contents. Make sure you\'re sending valid image', 422)
    except KeyError:
        return create_response('missing file', 422)

    return {'payload': bytelist}


@post('/encode64')
def encode_base64():
    try:
        image = request.files['file']
        b64_image = base64.b64encode(image.file.read()).decode('ascii')
    except KeyError:
        return create_response('missing file', 422)

    return {'payload': b64_image}


if os.environ.get('PROD'):
    run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get('PORT')))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)
