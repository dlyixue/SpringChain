import Miner
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
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# 主程序
# 1挖矿程序
# 挖矿，通知主程序挖矿结果
# 2主程序
# a.接收本节点挖矿结果，判断该结果是否之前已经被发布过，若没有被本节点或其他节点作为nonce发布过，则进入打包区块环节，并且奖励本节点账户100个单位BTC；否则抛弃这个挖矿结果。
# b.接收交易请求，存入本地交易池buff。
# c.接收其他节点发来的区块，先检验该区块是否合法（签名），若不合法则抛弃此区块；若合法，则保存此区块，顺序执行区块中所有交易并更新本地状态数据库，并从本地交易池删掉已被打包的交易。
# 注意，检查区块是否合法至少应包括  i) nonce合法（若采用随机决定则没有nonce）； ii)prevHash和前一区块的hash值是相等的； iii)交易的合法性（e.g. 超支）。
# d.打包区块，从交易池中选择一定数量的交易，构建区块并发送给其他节点

def mine_wrapper(miner, result_queue):
    while True:
        result_queue.put(miner.mine_block())

def receive_txn(node):
    net.receive_transactions(node)

def receive_block(node):
    net.receive_block(node)
    
if __name__ == "__main__":
    db_api.init_db()
    users = db_api.get_users()
    node = Node.node("n1",users['root'],users['u1'], "xhc_sc1" )
    miner = Miner.miner()
    node.create_genesis_block()
    result_queue = multiprocessing.Queue()

    # 启动子进程进行挖矿
    mining_process = multiprocessing.Process(target=mine_wrapper, args=(miner, result_queue))
    mining_process.start()
    # 线程接受交易
    transaction_thread = threading.Thread(target=receive_txn, args=(node,))
    transaction_thread.start()
    # 线程接受交易
    block_thread = threading.Thread(target=receive_block, args=(node,))
    block_thread.start()

    i = 10000000
    while i > 0:
        if not result_queue.empty():
            # 获取挖矿结果
            block_hash = result_queue.get()
            # 调用函数创建区块
            new_block = node.create_block(block_hash)
            node.pack_block(new_block)
            node.broadcast_block(new_block)
            node.confirm_block(new_block)
            print(i,"get block")
