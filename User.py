from Crypto.PublicKey import RSA

class user:
    def __init__(self,name):
        self.name=name
        self.balance=0
        self.key_pair=RSA.generate(2048)

    def getPublickey(self):
        return self.key_pair.publickey().export_key().decode()
    
    def getPrivatekey(self):
        return self.key_pair.export_key().decode()
    
    def getbalance(self):
        return self.balance
    
    def setbalance(self,x):
        try:
            assert x>0,"your balance must be greater than zero!"
            self.balance=x
            return True
        except Exception as ex:
            print("NOT sufficient funds:",ex)
        return False

