import socket
import os
import sys

# Configuration
HOST = '0.0.0.0'  # listen to all network interfaces
BUFFER_SIZE = 1024  # the size of the data received each time
DEST_FOLDER = '/mnt/sdb1/../../../'  # file storage path

# create the file storage path
if not os.path.exists(DEST_FOLDER):
    os.makedirs(DEST_FOLDER)

def receive_file(conn, addr):
    print(f"连接来自: {addr}")
    
    # Received file name
    filename = conn.recv(BUFFER_SIZE).decode()
    file_path = os.path.join(DEST_FOLDER, filename)

    # Check whether some downloaded files exist
    received_size = 0
    if os.path.exists(file_path):
        received_size = os.path.getsize(file_path)
        print(f"发现部分文件，已接收 {received_size} 字节，继续接收...")

    # Tell the client where to proceed with the transfer
    conn.send(str(received_size).encode())

    with open(file_path, 'ab') as f:  # Open the file in append mode
        while True:
            try:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    print(f"客户端 {addr} 断开连接")
                    break
                f.write(data)
            except socket.error as e:
                print(f"发生网络错误: {e}")
                break
            except Exception as e:
                print(f"发生异常: {e}")
                break

    print(f"文件 {filename} 接收完毕.")

def start_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, port))
        server_socket.listen(5)
        print(f"服务器启动，监听 {HOST}:{port}")
        
        while True:
            conn, addr = server_socket.accept()
            # Enable TCP Keepalive
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            # Set the connection timeout period
            conn.settimeout(30)  # 设置超时30秒
            receive_file(conn, addr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)
