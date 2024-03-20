import trade
import net
import User
# 调用trade函数，自动生成交易，发送到另外两台主机xhc_sc1,xhc_sc2

hosts = ['xhc_sc1','xhc_sc2']
users = list()
num_users = 5
num_trades = 100

for i in range(num_users):
    # Assuming you have some function to create users
    user = User.user("u"+str(i)) # You need to define create_user function
    users.append(user)

# 按批次生成
for i in range(num_trades):
    # Generate trades
    trades = trade.createtrade(users,1)

    # Send trades to each host
    for host in hosts:
        net.send_trades(host, 24320, trades)