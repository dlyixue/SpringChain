import json
import db_api
import Transaction
# change from hcy
# 定义区块类
class block:
    def __init__(self, index, prev_hash, transactions, hash, unconfirm_length):
        self.index = index  # 区块高度
        self.prev_hash = prev_hash # 前一个区块的哈希值
        self.transactions = []
        self.transactions.extend(transactions)# 包含的交易列表
        self.hash = hash   # 区块的哈希值
        self.unconfirm_length = unconfirm_length # 未验证的区块长度，根据最长链原则5-6个区块即可

    def validate_block(self, previous_block):
        if self.previous_hash != previous_block.hash:
            return False
        if self.hash != self.calculate_hash():
            return False
        return True

    def serialize(self):
        str_transactions = []
        for txn in self.transactions:
            str_transactions.append(txn.get_str())
        block_dict = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "transactions": str_transactions,
            "hash": self.hash,
            "unconfirm_length": self.unconfirm_length
        }
        block_string = json.dumps(block_dict)
        return block_string

def deserialize(block_string):
    serialized_block = json.loads(block_string)
    str_transactions = serialized_block["transactions"]
    transactions = []
    for txn in str_transactions:
        if(txn!=""):
            transactions.append(Transaction.str2Tran(txn))
    this_block = block(
        serialized_block["index"],
        serialized_block["prev_hash"],
        transactions,
        serialized_block["hash"],
        serialized_block["unconfirm_length"]
    )
    return this_block
    
def store_block(block):
    key = block.hash
    value = block.serialize()
    db_api.put_key(key,value)
    print("store block" + key + " " + value)