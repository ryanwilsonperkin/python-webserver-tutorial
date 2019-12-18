import socket
from .web_application import application

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


with socket.socket() as s:
    configure_socket(s)
    while True:
        conn, addr = s.accept()
        with conn:
            raw_request = load_raw_request(conn)
            environ = parse_request(raw_request)

            def start_response(status, headers):
                initial_response = HTTP_LINE_SEPARATOR.join([
                    f"HTTP/1.1 {status}",
                    *[f"{key}: {value}" for (key, value) in headers],
                    "",
                    ""
                ])
                initial_response_bytes = initial_response.encode("utf-8")
                conn.sendall(initial_response_bytes)

            response_chunks = application(environ, start_response)

            for chunk in response_chunks:
                conn.sendall(chunk)
