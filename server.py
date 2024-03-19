import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

def handle_client(connection, address):
    print("Connection from", address)
    data = connection.recv(1024).decode("utf-8")
    print("Received:", data)
    connection.sendall("Message received by server".encode("utf-8"))
    connection.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        connection, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(connection, address))
        client_handler.start()

