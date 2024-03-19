import socket

HOST = 'sc_box1'
PORT = 12345

data_to_send = "Hello, this is the data to transfer!"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(data_to_send.encode("utf-8"))

print("Data sent to server successfully.")

