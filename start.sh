#! /bin/bash
service mariadb restart
nohup /tmp/etcd-download-test/etcd > /SpringChain/etcd/out.log &