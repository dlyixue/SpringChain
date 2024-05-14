import os
import csv
import mysql.connector
import Transaction
import User
import subprocess
import db_api

def get_key(key):
    command = '''/tmp/etcd-download-test/etcdctl get {}'''.format(key)
    get_key=os.system(command)
    return get_key

def put_key(key, value):
    command = '''/tmp/etcd-download-test/etcdctl put B{} \'\'\'{}\'\'\''''.format(key,value)
    get_key=os.system(command)
    print(command)
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
    
    cursor.execute(query1)
    cursor.execute(query2)
    # 检查更新后的 amount 是否大于 0
    cursor.execute('SELECT amount FROM bank WHERE public_key = %s;', (user1,))
    updated_amount = cursor.fetchone()[0]
    if updated_amount <= 0:
        print('更新后的余额不足，请检查交易！')
        cnx.rollback()
        cursor.close()
        return -1
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
    query1 = '''Replace INTO bank (name, public_key, amount) VALUES ("{}","{}",{}) ;
            '''.format(name, user, value)
    print(query1)
    cursor.execute(query1)
    # 关闭游标和数据库连接
    cursor.close()
    cnx.commit()
    return 0

def get_users():
    try:
        cnx = mysql.connector.connect(user='root', password='123456', database='chain')
        print('连接成功！')
    except:
        print('something wrong!')

    users_key = {}
    # 连接MySQL数据库
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行查询语句
    query = 'SELECT name, public_key, amount FROM bank'
    cursor.execute(query)
    # 获取查询结果
    for (name, public_key, amount) in cursor:
        users_key[name] = public_key
    # 关闭游标和数据库连接
    cursor.close()
    return users_key

def drop_table(table_name):
    try:
        # 连接到数据库
        cnx = mysql.connector.connect(user='root', password='123456', database='chain')

        # 创建游标对象
        cursor = cnx.cursor()

        # 执行 SQL 语句
        drop_query = "DROP TABLE IF EXISTS " + table_name
        cursor.execute(drop_query)

        # 提交事务
        cnx.commit()
        print("Table 'bank' dropped successfully.")

    except Exception as e:
        print("Error dropping table:", str(e))

    finally:
        # 关闭游标和数据库连接
        cursor.close()
        cnx.close()

def trans_db():
    password = '123456'
    # 本地导出数据
    local_backup_path = './db/back_up.sql'
    export_command = f'/usr/bin/mysqldump -u root -p{password} chain bank > {local_backup_path}'
    subprocess.run(export_command, shell=True, check=True)

    # 远程传输备份文件到 xhc_sc1,xhc_sc2 节点
    remote_hosts = ['xhc_sc1', 'xhc_sc2']
    remote_path = '/SpringChain/db/back_up.sql'
    for remote_host in remote_hosts:
        remote_transfer_command = f'scp {local_backup_path} {remote_host}:{remote_path}'
        subprocess.run(remote_transfer_command, shell=True, check=True)

def init_db():
    password = '123456'
    # 删除表bank
    drop_table('bank')
    # 从备份文件恢复数据
    backup_path = './db/back_up.sql'
    restore_command = f'/usr/bin/mysql -u root -p{password} chain < {backup_path}'
    subprocess.run(restore_command, shell=True, check=True)