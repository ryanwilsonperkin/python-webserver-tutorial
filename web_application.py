def application(request):
    path = request["PATH_INFO"]
    handler = get_handler_for_path(path)
    response = handler(request)
    return response


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
