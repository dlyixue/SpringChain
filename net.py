import socket
import threading
import Block

def send_trades(host, port, trades):
    # 将交易列表转换为字符串
    trades_str = ",".join(trades)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # 连接到指定主机和端口
            client_socket.connect((host, port))

            # 发送交易数据
            client_socket.sendall(trades_str.encode("utf-8"))
            print("Trades sent successfully.")

        except Exception as e:
            print("Error sending trades:", str(e))

def receive_transactions(node):
    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定主机和端口
    host = '0.0.0.0'
    port = 24320
    server_socket.bind((host, port))
    # 监听连接
    server_socket.listen(5)

    while True:
        # 接受连接
        client_socket, address = server_socket.accept()
        print("Connection from", address)

        # 接收数据
        data = client_socket.recv(1024).decode("utf-8")
        # print("Received:", data)
        trades = data.split(',')
        # 将交易信息传入到node的pool中
        node.add_transactions_to_pool(trades)
        # 关闭连接
        client_socket.close()

def send_block(host, port, blocks):
    # 将区块列表序列化为字符串
    blocks_str = blocks
    try:
        # 创建套接字
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接到指定主机和端口
        client_socket.connect((host, port))

        # 发送区块数据
        client_socket.sendall(blocks_str.encode("utf-8"))
        print("Blocks sent successfully.")

        # 关闭套接字
        client_socket.close()
    except Exception as e:
        print("Error sending blocks:", str(e))

def receive_block(node):
    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定主机和端口
    host = '0.0.0.0'
    port =  24321
    server_socket.bind((host, port))

    # 监听连接
    server_socket.listen(5)

    while True:
        # 接受连接
        client_socket, address = server_socket.accept()
        print("Connection from", address)

        # 接收数据
        data = client_socket.recv(1024*10).decode("utf-8")
        print("Received:", data)

        # 处理接收到的数据，例如解析区块信息并执行相应操作
        block = Block.deserialize(data)
        node.receive_block(block)
        # 关闭连接
        client_socket.close()