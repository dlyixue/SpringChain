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

def create_block(new_block_id, prev_block_):
    # 创建区块是检测是否被创建
    if db_api.get_key(new_block_id) != 0:
        print(f"This new block have been created ")
        return 0
        
    # 根据哈希值创建区块
    prev_block = prev_block_
    index = prev_block.index + 1
    prev_hash = prev_block.hash
    new_block =block.block(index, prev_hash, [], new_block_id)
    # 将新区块加入到链中
    return new_block
    
def pack_block(self, new_block):
    txn = Transaction.transaction(self.root_key, self.owner, 10)
    new_block.transactions.append(txn) # 激励
    new_block.transactions.extend(self.pool[:5])
    transactions = new_block.transactions
    for transaction in transactions:
        if transaction in self.pool:
            self.pool.remove(transaction)
    print("create " + new_block.serialize()) 