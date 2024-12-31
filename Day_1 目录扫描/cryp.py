import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import base64

# 生成随机密钥
# key = get_random_bytes(16)  # AES密钥必须是16/24/32字节
# 固定的字符串
password = "LOVERLSS"
# 通过 SHA-256 将密码转换为 32 字节的密钥（适合 AES-256）
key = SHA256.new(password.encode('utf8')).digest()



def enctypt(message:str):

    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_EAX)
    # 加密消息
    message = message.encode('utf8')
    ciphertext, tag = cipher.encrypt_and_digest(message)
    data ={
        'ciphertext':base64.b64encode(ciphertext).decode(),
        'nonce':base64.b64encode(cipher.nonce).decode()
    }
    return json.dumps(data).encode('utf8')
# 打印加密结果


def decrypt(data:bytes):
    data = json.loads(data.decode('utf8'))
    # 解密
    cipher = AES.new(key, AES.MODE_EAX, nonce=base64.b64decode(data['nonce']))
    plaintext = cipher.decrypt(base64.b64decode(data['ciphertext']))
    return plaintext.decode('utf8')

help = """
base64 是一种编码方式，可以将二进制数据编码成可显示和传输的字符串。
它常用于需要在文本环境（如 HTTP、JSON）中存储或传输二进制数据。
"""
# print(decrypt(enctypt(help)))
