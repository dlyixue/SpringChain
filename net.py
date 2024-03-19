import socket

def start_server(host, port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
       server_socket.bind((host, port))
       server_socket.listen(1)

       print(f"Server listening on {host}:{port}")

       connection, client_address = server_socket.accept()

       with connection:
          print("Connection from", client_address)

          data = connection.recv(1024).decode("utf-8")
          print("Received:", data)



def start_client(host, port=12345, data_to_send="Hello, this is the data to transfer!"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       client_socket.connect((host, port))
       client_socket.sendall(data_to_send.encode("utf-8"))

    print("Data sent to server successfully.")


if __name__ == '__main__':
    StringData = "This is the StringData"
    start_server(host='0.0.0.0')
    start_client(host='xhc_ubuntu', data_to_send=StringData)