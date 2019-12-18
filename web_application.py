def application(environ, start_response):
    path = environ['PATH_INFO']
    handler = get_handler_for_path(path)
    response = handler(environ)
    response_bytes = response.encode('utf-8')

    start_response('200 OK', [
        ('Content-Length', str(len(response))),
        ('Content-Type', 'text/html'),
    ])
    return [response_bytes]


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
