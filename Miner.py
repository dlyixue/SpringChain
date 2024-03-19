import hashlib
import time
import random

class miner:
    def __init__(self, difficulty=100):
        self.difficulty = difficulty

    def mine_block(self, transactions, previous_block_hash):
        # 挖掘一个新的区块
        timestamp = int(time.time())
        nonce = 0
        block_hash = ''

        while not self.is_valid_block():
            nonce += 1
            block_data = str(timestamp) + str(nonce) + str(transactions) + previous_block_hash
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()

        return Block(timestamp, nonce, transactions, previous_block_hash, block_hash)

    def is_valid_block(self):
        # 检查区块的哈希是否满足难度要求
        return random.randint(1,self.difficulty*1000000)==1