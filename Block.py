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