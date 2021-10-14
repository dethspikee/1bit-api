from bottle import route, run, post, request, response, abort

from io import BytesIO
from PIL import UnidentifiedImageError
import base64

from converter import convert


@post('/convert')
def handle_conversion():
    width = request.params.get('width', '128')
    height = request.params.get('height', '64')
    threshold = request.params.get('threshold')

    try:
        image = request.files['file']
        b64_image = base64.b64encode(image.file.read())
        bytelist = convert(b64_image, (width, height), threshold)
    except UnidentifiedImageError:
        abort(422, 'Error processing file contents. Make sure you\'re sending valid image.')
    except KeyError:
        abort(422, "'file' key not found. Please provide image file.")

    return {'payload': bytelist}


run(host='localhost', port=8000, debug=True, reloader=True)
