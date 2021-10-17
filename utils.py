from bottle import HTTPResponse


def create_response(body, status_code, content_type):
    response = HTTPResponse(body, status_code)
    response.set_header('Content-Type', content_type)
    return response
