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

node1 = Node.node("n1")
node2 = Node.node("n2")

node1.create_genesis_block()
node2.create_genesis_block()

users = [User.user("u1"),User.user("u2")]
print(users)
trade.createtrade(users)