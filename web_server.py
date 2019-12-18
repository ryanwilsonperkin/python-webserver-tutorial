import socket

HOST = 'localhost'
PORT = 8000
MAX_REQUEST_BYTES = 1024


# Open a new socket on this computer
with socket.socket() as s:

    # Configure the socket to listen for connections on HOST:PORT
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Now listening for connections on http://{HOST}:{PORT}")

    # Process requests until we shut down the server
    while True:

        # Accept a new connection on this socket so we can read a request
        conn, addr = s.accept()
        with conn:

            # Read a request from the connection
            request_bytes = conn.recv(MAX_REQUEST_BYTES)
            request = request_bytes.decode('utf-8')

            # Print out the request
            print(request)

            # Write a response back on the same connection
            response = "Hello world"
            response_bytes = response.encode('utf-8')
            conn.sendall(response_bytes)
