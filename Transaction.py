import time
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class transaction:
    def __init__(self, sender_public_key, recipient_public_key, amount,_time_=int(time.time())):
        self.sender_public_key = sender_public_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount
        self.timestamp=_time_

    def sign_transaction(self, sender_private_key):
        # 使用发送者私钥对交易进行数字签名
        key = RSA.import_key(sender_private_key)
        h = SHA256.new(str(self).encode())
        signature = pkcs1_15.new(key).sign(h)
        return signature

    def verify_transaction(self, signature):
        # 使用发送者公钥验证交易的数字签名
        key = RSA.import_key(self.sender_public_key)
        h = SHA256.new(str(self).encode())

        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def get_str(self):
        #(*) is separator
        return str(self.sender_public_key)+"(*)"+str(self.recipient_public_key)+"(*)"+str(self.amount)+"(*)"+str(self.timestamp)

def str2Tran(str):
    strlist=str.split("(*)",4)
    if(len(strlist)<4):
        print(len(strlist))
        print(strlist)
    retTra=transaction(strlist[0],strlist[1],strlist[2],strlist[3])
    return retTra