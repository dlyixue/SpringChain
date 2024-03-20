from Crypto.PublicKey import RSA
import db_api
class user:
    def __init__(self, _name, _balance=100.0):
        self.name=_name
        self.balance=_balance
        self.key_pair=RSA.generate(2048)
        db_api.create_user(self.name, self.getPublickey(), self.balance)

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