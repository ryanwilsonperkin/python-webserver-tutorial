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


def load_request(conn):
    request_bytes = conn.recv(MAX_REQUEST_BYTES)
    return request_bytes.decode('utf-8')


def send_response(conn, response):
    response_bytes = response.encode('utf-8')
    conn.sendall(response_bytes)


def process_request(request):
    print(request)
    response_body = "Hello World"
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
            request = load_request(conn)
            response = process_request(request)
            send_response(conn, response)
