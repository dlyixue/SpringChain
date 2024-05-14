import trade
import net
import User
import time
import db_api
# 调用trade函数，自动生成交易，发送到另外两台主机xhc_sc1,xhc_sc2

# 参数定义
Hosts = ['xhc_sc0','xhc_sc1','xhc_sc2','xhc_sc3']
users = list()
num_users = 5
num_trades = 100

# 状态数据库生成
for i in range(num_users):
    # Assuming you have some function to create users
    user = User.user("u"+str(i)) # You need to define create_user function
    user.store_user()
    users.append(user)
db_api.trans_db()
print("trans_db finally")

# todo：生成数据
# 逐条生成交易数据
# if 数据>10 & 当前周期结束
# 打包成区块,发送给primary(地址固定)
# 等接受replay请求，如果replay请求大于f+1
# 打包处理写一个区块