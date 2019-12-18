import json


def application(environ, start_response):

    response = None

    # Apply middleware
    middlewares = [AuthMiddleware]
    for middleware in middlewares:
        response = middleware().process_request(environ)

        if response is not None:
            break

    if response is None:
        path = environ['PATH_INFO']
        handler = get_handler_for_path(path)
        response = handler(environ)

    status_code = None
    for middleware in reversed(middlewares):
        status_code = middleware().process_response(response)

        if status_code is not None:
            break

    status_code = status_code or 200

    response_bytes = response.encode('utf-8')

    start_response(str(status_code), [
        ('Content-Length', str(len(response))),
        ('Content-Type', 'application/json'),
    ])
    return [response_bytes]


def parse_cookies(cookies_string):
    cookies = {}

    if cookies_string == '':
        return cookies

    cookie_parts = cookies_string.split('; ')
    for cookie_part in cookie_parts:
        k, v = cookie_part.split('=')
        cookies[k] = v
    return cookies


class AuthMiddleware:
    ALLOWED_USERS = (
        "Natasha",
        "Dale",
        "Ryan"
    )

    def process_request(self, request):
        raw_cookie_dough = request.get('HTTP_COOKIE', '')
        cookies = parse_cookies(raw_cookie_dough)
        auth = cookies.get('auth')
        if auth not in self.ALLOWED_USERS:
            return "Not Allowed"
        return None

    def process_response(self, response):
        if response == "Not Allowed":
            return 403
        return None


def get_handler_for_path(path):
    if path == "/":
        return root_handler
    else:
        return path_handler


def root_handler(request):
    return "I am (g)root"


def path_handler(request):
    path = request["PATH_INFO"]
    return f"Hello from {path}"
