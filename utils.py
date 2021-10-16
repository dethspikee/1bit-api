from bottle import HTTPResponse


def create_response(body, status_code):
    response = HTTPResponse({'error': body}, status_code)
    response.set_header('Content-Type', 'application/json')
    return response
