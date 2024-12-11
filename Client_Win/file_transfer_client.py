import socket
import os
import sys
import time

# 配置
SERVER_HOST = '202.117.43.253'  # 服务器地址
BUFFER_SIZE = 1024         # 每次发送的数据大小
FILE_DIR = 'D:\\tmp\\'  # 要上传的文件路径


def send_file(filename, conn, start_pos):
    # 打开文件
    with open(filename, 'rb') as f:
        # 跳过已接收部分
        f.seek(start_pos)
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            conn.send(data)
    print(f"文件 {filename} 发送完毕.")

def start_client(filename, port):
    # 获取文件的名称
    file_basename = os.path.basename(filename)
    print(file_basename)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, port))
            
            # 发送文件名
            client_socket.send(file_basename.encode())

            # 获取已接收的文件大小
            received_size = int(client_socket.recv(BUFFER_SIZE).decode())

            print(f"从 {received_size} 字节开始继续发送...")

            # 打开文件并跳过已接收部分，继续发送
            send_file(filename, client_socket, received_size)
            
            print(f"文件 {filename} 发送完毕.")
            return 0
    except socket.error as e:
        print(f"Socket 错误: {e}. pcap {filename} 发送失败.")
        time.sleep(240)
        return -1
    except Exception as e:
        print(f"发生未知错误: {e}. pcap {filename} 发送失败.")
        time.sleep(240)
        return -1


def upload_files(file_dir, port, port_num):
    """读取文件夹并启动多个进程并行上传"""
    # 获取文件夹中的所有文件
    files = [os.path.join(file_dir, f) for f in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, f))]
    _i = 0
    while _i < len(files):
        if _i % port_num == 34000-port:
            _status = start_client(files[_i], port)
            _i+=_status
        _i+=1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example.py arg1 arg2")
        sys.exit(1)
    port = int(sys.argv[1])
    port_num = int(sys.argv[2])
    upload_files(FILE_DIR, port, port_num)
