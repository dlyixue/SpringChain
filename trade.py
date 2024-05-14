import Transaction
import User
import Miner
import random

def createtrade(users, numOfTrade=10):
    trades=list()
    n=len(users)
    if n <=1:
        return trades
    for num in range(numOfTrade):
        u1=random.randint(1,n)
        u2=random.randint(1,n)
        if u2==u1:
            u2==(u1+1)%n +1
        tmp_amount=random.uniform(0.0,20.0)
        _,tra=trade(users[u1-1],users[u2-1],tmp_amount)
        if tra!=None:
            trades.append(tra.get_str())
    return trades

def trade(sender,receiver,amount):
    try:
        assert amount>0
    except Exception as ex:
        print("Invalid trade!")
        return False,None
    tra=Transaction.transaction(sender.getPublickey(),receiver.getPublickey(),amount)
    sign=tra.sign_transaction(sender.getPrivatekey())
    if tra.verify_transaction(sign):
        if(sender.setbalance(sender.getbalance()-amount)):
            receiver.setbalance(receiver.getbalance()+amount)
            print("Trade Create successfully!")
            return True,tra
    print("Sender's balance has NOT sufficient funds.")
    return False,None