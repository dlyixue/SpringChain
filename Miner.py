import hashlib
import time
import random

class miner:
    def __init__(self, difficulty=100):
        self.difficulty = difficulty

    def mine_block(self):
        # 挖掘一个新的区块
        timestamp = int(time.time())
        block_hash = ""

        while not self.is_valid_block():
            block_hash = hashlib.sha256(str(timestamp).encode()).hexdigest()
        return block_hash

    def is_valid_block(self):
        # 检查区块的哈希是否满足难度要求
        return random.randint(1,self.difficulty*1000000)==1