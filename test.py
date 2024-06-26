import Miner
import Node
import Block
import Transaction
import User
import trade
import db_api

import hashlib
import random
import time
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

users = list()
u0=User.user ("root", 1000)
u1=User.user ("u1")
u2=User.user ("u2")
users.append(u1)
users.append(u2)

node1 = Node.node("n1",u1,u0.getPublickey())
node2 = Node.node("n2",u2,u0.getPublickey())

node1.create_genesis_block()
node2.create_genesis_block()

trades = trade.createtrade(users)
for txn in trades:
    node1.pool.append(Transaction.str2Tran(txn))
print(node1.pool)
b1 = node1.create_block("1")
node1.pack_block(b1)
b2 = node1.create_block("2")
b3 = node1.create_block("3")
b4 = node1.create_block("4")
b5 = node2.create_block("5")
b5.unconfirm_length = 4
b5.prev_hash = "4"
node1.receive_block(b5)
node1.confirm_block(node1.chain[-1])
node1.confirm_block(node1.chain[-1])