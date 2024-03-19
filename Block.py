# change from hcy
# 定义区块类
class block:
    index = 0 # 区块高度
    prev_hash = "0" # 前一个区块的哈希值
    hash = "0" # 区块的哈希值
    transactions = [] # 包含的交易列表
    unconfirm_length = 0 # 未验证的区块长度，根据最长链原则5-6个区块即可
    
    def __init__(self, index, prev_hash, transactions, hash, unconfirm_length):
        self.index = index  
        self.prev_hash = prev_hash
        self.transactions.append(transactions)
        self.hash = hash  
        self.unconfirm_length = unconfirm_length

    def validate_block(self, previous_block):
        if self.previous_hash != previous_block.hash:
            return False
        if self.hash != self.calculate_hash():
            return False
        return True

    def serialize(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "hash": self.hash,
            "unconfirm_length": self.data
        }

    @staticmethod
    def deserialize(serialized_block):
        this_block = block(
            serialized_block["index"],
            serialized_block["previous_hash"],
            serialized_block["transactions"],
            serialized_block["hash"],
            serialized_block["unconfirm_length"]
        )
        return block