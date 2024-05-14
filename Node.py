import Block
import net
import db_api
import Transaction
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
# 定义节点类
class node:
    def __init__(self, name, private_key):
        self.name = name  # 节点名称
        self.private_key = private_key # 私钥
        self.chain = []  # 节点维护的区块链

    def get_block_by_index(self, index):
        return self.chain[index]
    
    def receive_block(self, new_block):
        # 接收其他节点广播的新区块并验证其有效性，如果有效就添加到自己的区块链中，并从交易池中删除已确认的交易
        index = new_block.index
        prev_hash = new_block.prev_hash
        transactions = new_block.transactions
        hash = new_block.hash
        self.chain.append(new_block)
        print(f"{self.name} accepted block {index} and updated its chain and pool.")
        
    def broadcast_block(self, new_block):
        # 将当前区块广播到其它区块
        block_string = new_block.serialize()
        for host in self.hosts:
            if host != self.host:
                net.send_block(host, 24321, block_string)
        return 0
    
    def sign_message(self, message):
        h = SHA256.new(message.encode('utf-8'))
        signature = pkcs1_15.new(self.private_key).sign(h)
        return signature

    def verify_message(self, message, signature, public_key):
        h = SHA256.new(message.encode('utf-8'))
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False