import socket
from cryp import *
def udp_client():
    server_ip = "127.0.0.1"  # 服务器IP地址
    server_port = 12345      # 服务器端口
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"UDP客户端启动，目标服务器为 {server_ip}:{server_port}")

    while True:
        # 输入要发送的消息
        message = input("请输入要发送的消息: ")
        client_socket.sendto(enctypt(message), (server_ip, server_port))

        # 接收服务器响应
        data, server_address = client_socket.recvfrom(1024)
        print(f"收到来自服务器的消息: {decrypt(data)}")

if __name__ == "__main__":
    udp_client()
