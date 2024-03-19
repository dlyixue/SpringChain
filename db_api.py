import os
import csv
import mysql.connector

def get_key(key):
    command = "./tmp/etcd-download-test/etcdctl get " + key
    get_key=os.system(command)
    return get_key

def put_key(key, value):
    command = "./tmp/etcd-download-test/etcdctl put " + key + " " + value
    get_key=os.system(command)
    return get_key

def exec(txn):
    # 修改状态数据库:
    try:
        cnx = mysql.connector.connect(user='root', password='123456', database='chain')
        print('连接成功！')
    except:
        print('something wrong!')
    user1 = 101
    user2 = 102
    value = 10
    # 连接MySQL数据库
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行查询语句
    query1 = '''update user set money = money - {} where id = {};
            '''.format(value, user1)
    query2 = '''update user set money = money + {} where id = {};
            '''.format(value, user2)
    print(query1,query2)
    cursor.execute(query1)
    cursor.execute(query2)
    # 关闭游标和数据库连接
    cursor.close()
    cnx.commit()
    return 0

def create_user(id, money):
    # 修改状态数据库:
    try:
        cnx = mysql.connector.connect(user='root', password='123456', database='chain')
        print('连接成功！')
    except:
        print('something wrong!')
    user = 100
    value = 10
    # 连接MySQL数据库
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行查询语句
    query1 = '''insert into user values ({},{});
            '''.format(user, value)
    print(query1)
    cursor.execute(query1)
    # 关闭游标和数据库连接
    cursor.close()
    cnx.commit()
    return 0