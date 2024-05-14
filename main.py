import Node
import Block
import Transaction
import User
import trade
import db_api
import multiprocessing
import threading
import net

import hashlib
import random
import time
import argparse
# 主程序--节点
# 接收定义参数,创建节点,
# 如果是primary节点：
#   接受Client消息，向Replica发送消息，
#   发送时添加数字签名，接收时验证数字签名
# prepare阶段:(每个阶段收发走不同端口吧)
#   接收pre-prepare消息，验证消息
#   发送prepare消息
# commit阶段:
#   接收prepare消息，如果收到2f条消息
#   发送commit消息
# replay阶段：
#   接受commit消息，如果收到2f条commit
#   执行事务
#   加入链中
#   发送replay给client
Hosts = ['xhc_sc0','xhc_sc1','xhc_sc2','xhc_sc3']
if __name__ == "__main__":
    # 解析参数
    parser = argparse.ArgumentParser(description="Start Node.")
    parser.add_argument('--node_name', type=int, help='node_name')
    args = parser.parse_args()
    node_name = args.node_name
    # 定义节点
    node = Node.node(node_name)
    if node_name == 0:
        print("This is primary node.")
        Request = net.get_request_message() # 获取请求 包括request和block_data
        