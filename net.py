import socket
import threading


def start_server(host, port=12345):
    def handle_client(connection, address):
        print("Connection from", address)
        data = connection.recv(1024).decode("utf-8")
        print("Received:", data)
        connection.sendall("Message received by server".encode("utf-8"))
        connection.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)

        print(f"Server listening on {host}:{port}")

        while True:
            connection, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(connection, address))
            client_handler.start()


def start_client(host, port=12345, data_to_send="Hello, this is the data to transfer!"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       client_socket.connect((host, port))
       client_socket.sendall(data_to_send.encode("utf-8"))

       print("Data sent to server successfully.")

       # 等待服务器响应
       response = client_socket.recv(1024).decode("utf-8")
       print("Server response:", response)


# if __name__ == '__main__':
#     StringData = "This is the StringData"
#     start_server(host='0.0.0.0')
#     start_client(host='xhc_ubuntu', data_to_send=StringData)
    
    
