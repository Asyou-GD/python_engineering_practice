import argparse
from typing import Any, Dict

def parse_args():
    parser = argparse.ArgumentParser(description='test')
    """
    位置参数 按照顺序给 -
    选项参数 不用按照顺序给 -- 可选
    """
    parser.add_argument('-p', '--port', required=True, type=str, help='Specify the port')
    parser.add_argument('-u', '--user', required=True, type=str, default='guest', help='Specify the user')
    parser.add_argument('-d', '--debug', action='store_false', help='Enable debug mode')
    # 将解析结果传递给 Arguments 类
    args = parser.parse_args()
    return args
args = parse_args()
print(args.port)