import base64
import json
import re

from Crypto.Cipher import AES
from Crypto.Hash import SHA256, SHAKE128
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from typing import *
from Crypto.Util.Padding import pad, unpad
import os


class AES_MODE_EAS:
    def __init__(self):
        self.key, self.nonce = self.get_keys_nonce()
        # 生成随机盐值（16 字节）
        # self.salt = os.urandom(32)
        self.salt = b"\xc7i9\x8f7\xfe!\xa0\x96F\x1e\xcc\xdf\xd1o\r'\xaf\xfe5\xbf`\x0b\xad\x10\x83\xd2\x7f\xe0\xcc\r\xf8"
        self.hash = ['28b4f8acd8bbb1da188da14a146fe5743e67298e4f008f923ae7bddf198faf7a',
                     '729bfbb40e78b2bbdd1ce6253aa34ef63c5aa6a003f598c7fee8a9602b02e8fa']

    @staticmethod
    def get_keys_nonce():
        def fixed() -> (bytes, bytes):
            # 密钥（必须是 16/24/32 字节）
            key = b'sixteen byte key'
            # 固定的 nonce
            fixed_nonce = b'fixednonce1236+'  # 必须是 16 字节）
            return key, fixed_nonce

        def random():
            # 生成随机密钥
            key = get_random_bytes(16)  # AES密钥必须是16/24/32字节
            # 生成随机nonce
            nonce = get_random_bytes(16)  # 必须是 16 字节
            return key, nonce

        def sha_hash():
            # 固定的字符串
            password = "LOVERLSS"
            # 通过 SHA-256 将密码转换为 32 字节的密钥（适合 AES-256）
            key = SHA256.new(password.encode('utf8')).digest()

            password = "GD_Asyou"
            # 通过 SHA-256 将密码转换为 32 字节的密钥（适合 AES-256）
            nonce = SHA256.new(password.encode('utf8')).digest()

            key = base64.b64encode(key).decode()
            nonce = base64.b64encode(nonce).decode()
            return key, nonce

        key, nonce = sha_hash()

        return key, nonce

    def encrypt(self, message: str, Pr=False):
        if not isinstance(self.key, bytes):
            self.key = base64.b64decode(self.key)
        if not isinstance(self.nonce, bytes):
            self.nonce = base64.b64decode(self.nonce)
        if not isinstance(message, bytes):
            message = message.encode('utf8')

        data_with_salt = self.salt + message
        # 创建AES加密器
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)

        ciphertext, tag = cipher.encrypt_and_digest(pad(data_with_salt, AES.block_size))
        ciphertext = base64.b64encode(ciphertext).decode()
        return ciphertext

    # 打印加密结果

    def decrypt(self, data):
        if not isinstance(self.key, bytes):
            self.key = base64.b64decode(self.key)
        if not isinstance(self.nonce, bytes):
            self.nonce = base64.b64decode(self.nonce)
        if not isinstance(data, bytes):
            data = base64.b64decode(data)

        # 解密
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
        plaintext = cipher.decrypt(data)
        decrypted_data = unpad(plaintext, AES.block_size)
        return decrypted_data[len(self.salt):].decode('utf8')

    def get_hash(self):
        user = self.encrypt('x')
        passwd = self.encrypt('x')
        host = self.encrypt('x:x', True)
        database = self.encrypt('x')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@{host}/{database}'
        return SHA256.new(SQLALCHEMY_DATABASE_URI.encode('utf8')).hexdigest()

    # 接收方
    def verify_integrity(self, data):
        provided_hash = self.hash
        # 计算接收到的数据的哈希值
        if not isinstance(data, bytes):
            data = data.encode('utf8')

        calculated_hash = SHA256.new(data).hexdigest()
        # digest()  32字节bytes
        # hexdigest 64长度字符串 获取哈希值的十六进制表示
        # 比较两个哈希值
        print([single_hash == calculated_hash for single_hash in provided_hash])
        if sum([single_hash == calculated_hash for single_hash in provided_hash]) > 0:
            print("数据完整，未被篡改")
            return True
        else:
            print("数据已被篡改或发生错误")
            return False

    def process_config(self, str):
        Sql_connect = re.search(r'mysql\+pymysql://(.*?):(.*?)@', str, re.S)

        pre_fix_index = len(Sql_connect.group())

        data = Sql_connect.groups()
        length = len(data[0])

        user = self.decrypt(data[0])
        passwd = self.decrypt(data[1])
        host = self.decrypt(str[pre_fix_index:pre_fix_index + length])
        database = self.decrypt(str[pre_fix_index + length + 1:])

        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@{host}/{database}'
        return SQLALCHEMY_DATABASE_URI


if __name__ == '__main__':
    aes_crypt = AES_MODE_EAS()
    sql_connect = 'mysql+pymysql://0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XcjqfvecveJ9VTUU8tDYC6:0yHHdeaqv6Pd' \
                  'XELCbo/GOBx+0sLCMzvsBzg2bC+f37XppfijRP/jG+BYWkQmBoux@' \
                  '0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XCjqv6Ga+9WK1lbnARN460/0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37Xbkq3EAaKhX9FXVUspCYS+'
    if aes_crypt.verify_integrity(sql_connect):
        print(aes_crypt.process_config(sql_connect))
    print(SHA256.new('mysql+pymysql://0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XahLvvecveJ9VTUU8tDYC6:0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XppfijRP/jG+BYWkQmBoux@0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XCjqv6Ga+9WK1lbnARN460/0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37Xbkq3EAaKhX9FXVUspCYS+'.encode()).hexdigest())
