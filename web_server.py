import socket

HOST = 'localhost'
PORT = 8000
MAX_REQUEST_BYTES = 1024


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


with socket.socket() as s:
    configure_socket(s)
    while True:
        conn, addr = s.accept()
        with conn:
            request = load_request(conn)
            print(request)
            response = "Hello World"
            send_response(conn, response)
