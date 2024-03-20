import os
import csv
import mysql.connector
import Transaction

def get_key(key):
    command = "/tmp/etcd-download-test/etcdctl get " + key
    get_key=os.system(command)
    return get_key

def put_key(key, value):
    command = "/tmp/etcd-download-test/etcdctl put " + key + " " + value
    get_key=os.system(command)
    return get_key

def exec(txn):
    print(txn)
    # 修改状态数据库:
    try:
        cnx = mysql.connector.connect(user='root', password='123456', database='chain')
        print('连接成功！')
    except:
        print('something wrong!')
    user1 = txn.sender_public_key
    user2 = txn.recipient_public_key
    value = txn.amount
    # 连接MySQL数据库
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行查询语句
    query1 = '''update bank set amount = amount - {} where public_key = "{}";
            '''.format(value, user1)
    query2 = '''update bank set amount = amount + {} where public_key = "{}";
            '''.format(value, user2)
    print(query1,query2)
    cursor.execute(query1)
    cursor.execute(query2)
    # 关闭游标和数据库连接
    cursor.close()
    cnx.commit()
    return 0

def create_user(name,public_key, money):
    # 修改状态数据库:
    try:
        cnx = mysql.connector.connect(user='root', password='123456', database='chain')
        print('连接成功！')
    except:
        print('something wrong!')
    user = public_key
    value = money
    # 连接MySQL数据库
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行查询语句
    query1 = '''insert into bank values ("{}","{}",{});
            '''.format(name, user, value)
    print(query1)
    cursor.execute(query1)
    # 关闭游标和数据库连接
    cursor.close()
    cnx.commit()
    return 0