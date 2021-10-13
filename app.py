from bottle import route, run, post, request, response, abort

from PIL import UnidentifiedImageError

from converter import convert


@post('/convert')
def handle_conversion():
    width = request.params.get('width', '128')
    height = request.params.get('height', '64')


    try:
        image = request.files['file']
        bytelist = convert(image.file, (width, height))
    except UnidentifiedImageError:
        abort(422, 'Error processing file contents. Make sure you\'re sending valid image.')
    except KeyError:
        abort(422, "'file' key not found. Please provide image file.")


    return {'payload': bytelist}


run(host='localhost', port=8000, debug=True, reloader=True)
