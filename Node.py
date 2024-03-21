import Block
import net
import db_api
import Transaction
# 定义节点类
class node:
    def __init__(self, name, root, user, host):
        self.root_key = root # 发送用于激励 
        self.name = name  # 节点名称
        self.owner = user # 拥有者
        self.chain = []  # 节点维护的区块链
        self.pool = []  # 节点收集的交易池
        self.hosts = ['xhc_sc1','xhc_sc2']
        self.host = host

    def get_block_by_index(self, index):
        return self.chain[index]

    def get_block_by_hash(self, hash):
        for i in self.chain:
            if i.hash == hash:
                return i
        return None
    
    def create_genesis_block(self):
        # 创建创世区块并添加到区块链中
        genesis_block = Block.block(0, "0" * 64, [], "0" * 64, 0)
        self.chain.append(genesis_block)
        Block.store_block(genesis_block)
        print(f"{self.name} created the genesis block: \n{genesis_block}")
    
    def create_block(self, new_block_id):
        # 创建区块是检测是否被创建
        if db_api.get_key(new_block_id) != 0:
            print(f"This new block have been created ")
            return 0
        
        # 根据哈希值创建区块
        prev_block = self.chain[-1]
        index = prev_block.index + 1
        prev_hash = prev_block.hash
        unconfirm_length = prev_block.unconfirm_length + 1
        new_block = Block.block(index, prev_hash, [], new_block_id, unconfirm_length)
        # 将新区块加入到链中
        self.chain.append(new_block)
        return new_block
        
    def receive_block(self, new_block):
        # 接收其他节点广播的新区块并验证其有效性，如果有效就添加到自己的区块链中，并从交易池中删除已确认的交易
        index = new_block.index
        prev_hash = new_block.prev_hash
        transactions = new_block.transactions
        hash = new_block.hash

        # 如果新区块有效，就添加到自己的区块链中，并从交易池中删除已确认的交易
        self.chain.append(new_block)
        for transaction in transactions:
            if transaction in self.pool:
                self.pool.remove(transaction)
        self.confirm_block(new_block)
        print(f"{self.name} accepted block {index} and updated its chain and pool.")
        
    def broadcast_block(self, new_block):
        # 将当前区块广播到其它区块
        block_string = new_block.serialize()
        for host in self.hosts:
            if host != self.host:
                net.send_block(host, 24321, block_string)
        return 0
    
    def pack_block(self, new_block):
        txn = Transaction.transaction(self.root_key, self.owner, 10)
        new_block.transactions.append(txn) # 激励
        new_block.transactions.extend(self.pool[:5])
        transactions = new_block.transactions
        for transaction in transactions:
            if transaction in self.pool:
                self.pool.remove(transaction)
        print("create " + new_block.serialize())
        
    def confirm_block(self, new_block):
        if new_block.unconfirm_length < 4:
            return 0
        # 找到最开始的未confirm的块
        tar_block = new_block
        while tar_block.unconfirm_length > 0:
            tar_block.unconfirm_length = tar_block.unconfirm_length - 1
            prev = tar_block.prev_hash
            print(tar_block.hash,tar_block.unconfirm_length)
            tar_block = self.get_block_by_hash(prev)
        if tar_block.hash == "0"*64:
            return 0
        # 处理交易
        # 更新状态数据库
        transactions = tar_block.transactions
        for txn in transactions:
            db_api.exec(txn)
        Block.store_block(tar_block)
        return 0
    
    def add_transactions_to_pool(self, trades):
        # 将传入的交易列表添加到交易池中
        for txn in trades:
            # print(txn)
            self.pool.append(Transaction.str2Tran(txn))