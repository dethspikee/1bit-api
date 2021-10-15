from bottle import route, run, post, request, response, abort

from io import BytesIO
from PIL import UnidentifiedImageError
import base64
import os

from converter import convert


@post('/convert')
def handle_conversion():
    threshold = request.params.get('threshold')

    try:
        image = request.files['file']
        b64_image = base64.b64encode(image.file.read())
        bytelist = convert(b64_image, threshold)
    except UnidentifiedImageError:
        abort(422, 'Error processing file contents. Make sure you\'re sending valid image.')
    except KeyError:
        abort(422, "'file' key not found. Please provide image file.")

    return {'payload': bytelist}


if os.environ.get('PROD'):
    run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get('PORT')))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)

