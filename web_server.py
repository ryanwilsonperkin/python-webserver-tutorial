import socket

HOST = 'localhost'
PORT = 8000
MAX_REQUEST_BYTES = 1024
HTTP_LINE_SEPARATOR = "\r\n"


def configure_socket(s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Now listening for connections on http://{HOST}:{PORT}")


def load_raw_request(conn):
    request_bytes = conn.recv(MAX_REQUEST_BYTES)
    return request_bytes.decode('utf-8')


def send_response(conn, response):
    response_bytes = response.encode('utf-8')
    conn.sendall(response_bytes)


def parse_header_line(line):
    key, value = line.split(':', maxsplit=1)
    key = 'HTTP_' + key.upper().replace('-', '_').replace(' ', '_')
    value = value.strip()
    return (key, value)


def parse_request(raw_request):
    """
    Parse an HTTP Request into a python dictionary. Requests look like this:

    GET / HTTP/1.1
    Accept: text/html
    Host: localhost:8000
    """
    request_line, *header_lines = raw_request.split(HTTP_LINE_SEPARATOR)
    method, path, protocol = request_line.split()
    headers = dict(
        parse_header_line(line)
        for line in header_lines
        if line
    )

    return {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SERVER_PROTOCOL': protocol,
        **headers
    }


def process_request(request):
    print(request)
    response_body = f"Hello from {request['PATH_INFO']}"
    response = HTTP_LINE_SEPARATOR.join([
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Content-Length: {len(response_body)}",
        "",
        response_body
    ])
    return response


with socket.socket() as s:
    configure_socket(s)
    while True:
        conn, addr = s.accept()
        with conn:
            raw_request = load_raw_request(conn)
            request = parse_request(raw_request)
            response = process_request(request)
            send_response(conn, response)
