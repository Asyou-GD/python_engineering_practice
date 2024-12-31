import socket
from cryp import *
def udp_server():
    server_ip = "127.0.0.1"  # 本地IP地址
    server_port = 12345      # 监听端口

    # 创建UDP socket
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((server_ip, server_port))

    print(f"UDP服务器启动，正在监听 {server_ip}:{server_port}")

    while True:
        # 接收数据  # 缓冲区大小为1024字节
        data, client_address = udp_server_socket.recvfrom(1024)
        print(f"收到来自 {client_address} 的消息: {decrypt(data)}")

        # 发送响应
        response = input("请输入回复内容: ")
        udp_server_socket.sendto(enctypt(response), client_address)

if __name__ == "__main__":
    udp_server()
