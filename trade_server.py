import trade
import net
import User
import time
import db_api
# 调用trade函数，自动生成交易，发送到另外两台主机xhc_sc1,xhc_sc2

hosts = ['xhc_sc1','xhc_sc2']
users = list()
user = User.user("root",1000000)
user.store_user()
num_users = 5
num_trades = 1000

for i in range(num_users):
    # Assuming you have some function to create users
    user = User.user("u"+str(i)) # You need to define create_user function
    user.store_user()
    users.append(user)

db_api.trans_db()
print("trans_db finally")
# 按批次生成
for i in range(num_trades):
    # Generate trades
    trades = trade.createtrade(users,1)
    print(users[0].balance,users[1].balance)
    # Send trades to each host
    for host in hosts:
        net.send_trades(host, 24320, trades)
    time.sleep(2)